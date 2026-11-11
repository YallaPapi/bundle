"""Local Bundle analytics. Bundle access is GET-only; publishing is untouched."""
from __future__ import annotations

import argparse
import bisect
import concurrent.futures
import json
import logging
from logging.handlers import RotatingFileHandler
import socket
import sqlite3
import threading
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import requests

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'dashboard' / 'data'
DB = DATA / 'analytics.sqlite3'
TZ = timezone(timedelta(hours=7))
PORT = 8876
LOG = logging.getLogger('bundle.analytics')


def stamp(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)


def iso(value):
    return value.astimezone(timezone.utc).isoformat()


def day(value):
    return stamp(value).astimezone(TZ).date().isoformat()


class Store:
    def __init__(self, path=DB):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.db = sqlite3.connect(path, timeout=30)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('PRAGMA busy_timeout=30000')
        self.db.executescript('''
            CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS accounts(
              id TEXT PRIMARY KEY, team_id TEXT, team TEXT, username TEXT, created_at TEXT,
              active INTEGER DEFAULT 1, fetch_error TEXT DEFAULT '');
            CREATE TABLE IF NOT EXISTS profiles(
              id TEXT PRIMARY KEY, account_id TEXT, observed_at TEXT, followers REAL, following REAL);
            CREATE INDEX IF NOT EXISTS profiles_account ON profiles(account_id,observed_at);
            CREATE TABLE IF NOT EXISTS posts(
              id TEXT PRIMARY KEY, account_id TEXT, team_id TEXT, status TEXT, scheduled_at TEXT,
              published_at TEXT, attempted_at TEXT, permalink TEXT, error_code TEXT, error TEXT,
              analytics_error TEXT DEFAULT '');
            CREATE INDEX IF NOT EXISTS posts_account ON posts(account_id,published_at);
            CREATE TABLE IF NOT EXISTS post_snapshots(
              id TEXT PRIMARY KEY, post_id TEXT, observed_at TEXT, views REAL,
              likes REAL, comments REAL, shares REAL, saves REAL);
            CREATE INDEX IF NOT EXISTS snapshots_post ON post_snapshots(post_id,observed_at);
            CREATE TABLE IF NOT EXISTS daily(
              account_id TEXT, day TEXT, followers REAL, follower_change REAL, views_gain REAL,
              views_covered INTEGER, views_expected INTEGER, PRIMARY KEY(account_id,day));
            CREATE INDEX IF NOT EXISTS daily_day ON daily(day);
            CREATE TABLE IF NOT EXISTS audience(
              account_id TEXT PRIMARY KEY, observed_at TEXT, data TEXT, error TEXT DEFAULT '');
            CREATE TABLE IF NOT EXISTS post_totals(
              post_id TEXT PRIMARY KEY, snapshot_id TEXT, observed_at TEXT,
              views REAL, impressions REAL, reach REAL, likes REAL, comments REAL, shares REAL, saves REAL);
        ''')
        additions = {
            'profiles': {'profile_views': 'REAL', 'impressions': 'REAL', 'reach': 'REAL',
                         'likes': 'REAL', 'comments': 'REAL', 'post_count': 'REAL'},
            'post_snapshots': {'impressions': 'REAL', 'reach': 'REAL'},
            'posts': {'external_id': 'TEXT', 'title': 'TEXT', 'caption': 'TEXT'},
            'daily': {**{f'{field}_gain': 'REAL' for field in ('likes', 'comments', 'shares', 'saves')},
                      **{f'{field}_covered': 'INTEGER' for field in ('likes', 'comments', 'shares', 'saves')}},
        }
        for table, columns in additions.items():
            existing = {r[1] for r in self.db.execute(f'PRAGMA table_info({table})')}
            for column, kind in columns.items():
                if column not in existing:
                    self.db.execute(f'ALTER TABLE {table} ADD COLUMN {column} {kind}')
        self.db.commit()
        if not self.get('post_totals_migrated'):
            self.db.execute('''INSERT OR IGNORE INTO post_totals
                SELECT post_id,id,observed_at,views,impressions,reach,likes,comments,shares,saves
                FROM (SELECT *,ROW_NUMBER() OVER(PARTITION BY post_id ORDER BY observed_at DESC,id DESC) n
                  FROM post_snapshots) WHERE n=1''')
            self.set('post_totals_migrated', True)

    def close(self):
        self.db.close()

    def get(self, key, default=None):
        row = self.db.execute('SELECT value FROM meta WHERE key=?', (key,)).fetchone()
        return json.loads(row[0]) if row else default

    def set(self, key, value):
        self.db.execute('INSERT OR REPLACE INTO meta VALUES(?,?)', (key, json.dumps(value)))
        self.db.commit()

    def claim(self, now):
        self.db.execute('BEGIN IMMEDIATE')
        until = self.get('running_until')
        if until and stamp(until) > now:
            self.db.rollback()
            return False
        self.db.execute('INSERT OR REPLACE INTO meta VALUES(?,?)',
                        ('running_until', json.dumps(iso(now + timedelta(hours=2)))))
        self.db.commit()
        return True

    def release(self):
        self.set('running_until', None)

    def accounts(self, teams):
        self.db.execute('UPDATE accounts SET active=0')
        for team in teams:
            for a in team.get('socialAccounts', []):
                if a.get('type') != 'INSTAGRAM' or a.get('deletedAt'):
                    continue
                self.db.execute('''INSERT INTO accounts(id,team_id,team,username,created_at,active)
                  VALUES(?,?,?,?,?,1) ON CONFLICT(id) DO UPDATE SET
                  team_id=excluded.team_id,team=excluded.team,username=excluded.username,active=1''',
                  (a['id'], team['id'], team['name'], a.get('username') or a['id'], a.get('createdAt')))
        self.db.commit()

    def profiles(self, account_id, items):
        for item in items:
            if not item.get('createdAt') or item.get('deletedAt'):
                continue
            self.db.execute('''INSERT OR REPLACE INTO profiles
                 (id,account_id,observed_at,followers,following,profile_views,impressions,reach,likes,comments,post_count)
                 VALUES(?,?,?,?,?,?,?,?,?,?,?)''',
                            (item['id'], account_id, iso(stamp(item['createdAt'])),
                             item.get('followers'), item.get('following'), item.get('views'),
                             item.get('impressions'), item.get('impressionsUnique'), item.get('likes'),
                             item.get('comments'), item.get('postCount')))
        self.db.commit()

    def posts(self, team_id, items):
        for p in items:
            for association in p.get('socialAccounts', []):
                a = association.get('socialAccount', {})
                if a.get('type') != 'INSTAGRAM':
                    continue
                aid = association['socialAccountId']
                if not self.db.execute('SELECT 1 FROM accounts WHERE id=?', (aid,)).fetchone():
                    continue
                err = p.get('errorsVerbose', {}).get('INSTAGRAM') or {}
                error = err.get('errorMessage') or p.get('errors', {}).get('INSTAGRAM') or ''
                posted = p['status'] == 'POSTED' and association.get('externalPostId') and not error
                published = p.get('postedDate') or p.get('postDate') if posted else None
                self.db.execute('''INSERT INTO posts(id,account_id,team_id,status,scheduled_at,
                  published_at,attempted_at,permalink,error_code,error,external_id,title,caption)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                  ON CONFLICT(id) DO UPDATE SET account_id=excluded.account_id,status=excluded.status,
                  scheduled_at=excluded.scheduled_at,published_at=excluded.published_at,
                  attempted_at=excluded.attempted_at,permalink=excluded.permalink,
                  error_code=excluded.error_code,error=excluded.error,external_id=excluded.external_id,
                  title=excluded.title,caption=excluded.caption''',
                  (p['id'], aid, team_id, p['status'], p.get('postDate'), published,
                   p.get('postedDate'), (p.get('externalData', {}).get('INSTAGRAM') or {}).get('permalink', ''),
                   err.get('code', ''), error, association.get('externalPostId'),
                   p.get('title') or '', (p.get('data', {}).get('INSTAGRAM') or {}).get('text') or ''))
        self.db.commit()

    def post_metrics(self, post_id, items):
        for item in items:
            if not item.get('createdAt') or item.get('deletedAt'):
                continue
            self.db.execute('''INSERT OR REPLACE INTO post_snapshots
               (id,post_id,observed_at,views,likes,comments,shares,saves,impressions,reach)
               VALUES(?,?,?,?,?,?,?,?,?,?)''',
                (item['id'], post_id, iso(stamp(item['createdAt'])), item.get('views'),
                 item.get('likes'), item.get('comments'), item.get('shares'), item.get('saves'),
                 item.get('impressions'), item.get('impressionsUnique')))
            self.db.execute('''INSERT INTO post_totals VALUES(?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(post_id) DO UPDATE SET snapshot_id=excluded.snapshot_id,
                observed_at=excluded.observed_at,views=excluded.views,impressions=excluded.impressions,
                reach=excluded.reach,likes=excluded.likes,comments=excluded.comments,
                shares=excluded.shares,saves=excluded.saves
                WHERE excluded.observed_at>=post_totals.observed_at''',
                (post_id,item['id'],iso(stamp(item['createdAt'])),item.get('views'),item.get('impressions'),
                 item.get('impressionsUnique'),item.get('likes'),item.get('comments'),item.get('shares'),item.get('saves')))
        self.db.commit()

    def audience(self, account_id, items, error=''):
        if __package__:
            from .metrics import parse_audience
        else:
            from metrics import parse_audience
        newest = max((i for i in items if i.get('createdAt') and i.get('raw')),
                     key=lambda i: stamp(i['createdAt']), default=None)
        if newest:
            self.db.execute('INSERT OR REPLACE INTO audience VALUES(?,?,?,?)',
                            (account_id, iso(stamp(newest['createdAt'])), json.dumps(parse_audience(newest['raw'])), error))
        else:
            self.db.execute('''INSERT INTO audience VALUES(?,NULL,NULL,?)
                 ON CONFLICT(account_id) DO UPDATE SET error=excluded.error''',
                 (account_id, error or 'No raw analytics snapshots returned'))
        self.db.commit()

    def rebuild(self, now):
        cutoff = (now.astimezone(TZ).date() - timedelta(days=90)).isoformat()
        profile_days = {}
        for row in self.db.execute('SELECT * FROM profiles ORDER BY observed_at'):
            profile_days[(row['account_id'], day(row['observed_at']))] = row['followers']
        post_dates = defaultdict(list)
        identities = {}
        for p in self.db.execute('''SELECT p.id,p.account_id,p.published_at,p.external_id,t.observed_at
              FROM posts p LEFT JOIN post_totals t ON t.post_id=p.id WHERE p.published_at IS NOT NULL'''):
            identity = (p['account_id'], p['external_id'] or p['id'])
            old = identities.get(identity)
            if old is None or (p['observed_at'] or '', p['id']) > (old['observed_at'] or '', old['id']):
                identities[identity] = dict(p)
        canonical_ids = {p['id'] for p in identities.values()}
        for p in identities.values():
            post_dates[p['account_id']].append(day(p['published_at']))
        for dates in post_dates.values():
            dates.sort()
        observed = {}
        for s in self.db.execute('''SELECT s.*,p.account_id,p.published_at FROM post_snapshots s
                 JOIN posts p ON p.id=s.post_id WHERE p.published_at IS NOT NULL
                 ORDER BY s.post_id,s.observed_at'''):
            if s['post_id'] not in canonical_ids:
                continue
            observed[(s['post_id'], day(s['observed_at']))] = dict(s)
        gains = defaultdict(list)
        previous = {}
        for (pid, d), s in sorted(observed.items()):
            old = previous.get(pid)
            values = {}
            for field in ('views', 'likes', 'comments', 'shares', 'saves'):
                value = None
                if s[field] is not None and old and old[field] is not None:
                    gap = stamp(s['observed_at']) - stamp(old['observed_at'])
                    consecutive = datetime.fromisoformat(d).date() - datetime.fromisoformat(day(old['observed_at'])).date() == timedelta(days=1)
                    delta = s[field] - old[field]
                    if consecutive and timedelta(0) < gap <= timedelta(hours=36) and delta >= 0:
                        value = delta
                elif s[field] is not None and not old and day(s['published_at']) == d:
                    value = s[field]
                values[field] = value
            if d >= cutoff:
                gains[(s['account_id'], d)].append(values)
            previous[pid] = s
        keys = {key for key in profile_days if key[1] >= cutoff} | set(gains)
        for aid, d in keys:
            prev_day = (datetime.fromisoformat(d).date() - timedelta(days=1)).isoformat()
            follower = profile_days.get((aid, d))
            prev = profile_days.get((aid, prev_day))
            net = follower - prev if follower is not None and prev is not None else None
            def changes(field):
                return [v[field] for v in gains.get((aid, d), []) if v[field] is not None]
            values = changes('views')
            expected = bisect.bisect_right(post_dates[aid], d)
            other = [sum(changes(f)) if changes(f) else None for f in ('likes', 'comments', 'shares', 'saves')]
            covered = [len(changes(f)) for f in ('likes', 'comments', 'shares', 'saves')]
            self.db.execute('''INSERT OR REPLACE INTO daily
                (account_id,day,followers,follower_change,views_gain,views_covered,views_expected,
                 likes_gain,comments_gain,shares_gain,saves_gain,likes_covered,comments_covered,shares_covered,saves_covered)
                 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                 (aid, d, follower, net, sum(values) if values else None, len(values), expected, *other, *covered))
        self.db.commit()

    def prune(self, now):
        cutoff = iso(now - timedelta(days=90))
        self.db.execute('''DELETE FROM post_snapshots WHERE observed_at < ? AND id NOT IN
          (SELECT id FROM (SELECT id,ROW_NUMBER() OVER(PARTITION BY post_id ORDER BY observed_at DESC,id DESC) n
            FROM post_snapshots WHERE observed_at < ?) WHERE n=1)''', (cutoff, cutoff))
        self.db.commit()
        self.db.execute('PRAGMA optimize')


def report(store, now=None, days=30, group='All'):
    now = now or datetime.now(timezone.utc)
    since = (now.astimezone(TZ).date() - timedelta(days=days - 1)).isoformat()
    accounts = [dict(r) for r in store.db.execute('SELECT * FROM accounts ORDER BY username COLLATE NOCASE')]
    profiles = {}
    for r in store.db.execute('SELECT * FROM profiles ORDER BY observed_at'):
        profiles[r['account_id']] = dict(r)
    latest_views = {}
    for r in store.db.execute('SELECT * FROM post_totals'):
        latest_views[r['post_id']] = dict(r)
    per_post = defaultdict(list)
    for p in store.db.execute('SELECT * FROM posts'):
        per_post[p['account_id']].append(dict(p))
    daily = [dict(r) for r in store.db.execute('SELECT * FROM daily WHERE day>=? ORDER BY day', (since,))]
    daily_by_account = defaultdict(list)
    for d in daily:
        daily_by_account[d['account_id']].append(d)
    groups = sorted({a['team'].split('-')[0] if '-' in a['team'] else 'Other' for a in accounts})
    for a in accounts:
        profile = profiles.get(a['id'])
        a['group'] = a['team'].split('-')[0] if '-' in a['team'] else 'Other'
        a['followers'] = profile['followers'] if profile else None
        a['profile_updated'] = profile['observed_at'] if profile else None
        a['stale'] = not profile or now - stamp(profile['observed_at']) > timedelta(hours=36)
        published = [p for p in per_post[a['id']] if p['published_at']]
        a['published_posts'] = len(published)
        views = [latest_views[p['id']]['views'] for p in published
                 if p['id'] in latest_views and latest_views[p['id']]['views'] is not None]
        a['video_views'] = sum(views) if views else None
        a['posts_with_metrics'] = len(views)
        gains = [d['views_gain'] for d in daily_by_account[a['id']] if d['views_gain'] is not None]
        a['view_gains'] = sum(gains) if gains else None
        metrics = daily_by_account[a['id']]
        a['follower_change'] = sum(d['follower_change'] or 0 for d in metrics) if any(d['follower_change'] is not None for d in metrics) else None
        attempts = [p for p in per_post[a['id']] if p['status'] in ('POSTED', 'ERROR')]
        latest = max(attempts, key=lambda p: stamp(p['attempted_at'] or p['scheduled_at']), default=None)
        a['last_post_status'] = latest['status'] if latest else None
        a['last_post_at'] = latest['attempted_at'] or latest['scheduled_at'] if latest else None
        a['last_error'] = latest['error'] if latest and latest['status'] == 'ERROR' else ''
        a['status'] = 'Removed' if not a['active'] else (
            'Reconnect' if latest and latest['status'] == 'ERROR' and '190' in latest['error_code'] else (
                'Post error' if latest and latest['status'] == 'ERROR' else (
                    'Data issue' if a['fetch_error'] else ('Stale data' if a['stale'] else 'OK'))))
    chosen = [a for a in accounts if a['active'] and (group == 'All' or a['group'] == group)]
    ids = {a['id'] for a in chosen}
    series = defaultdict(list)
    for d in daily:
        if d['account_id'] in ids:
            series[d['day']].append(d)
    chart = []
    known_followers = {}
    for r in store.db.execute('''SELECT account_id,followers FROM (
        SELECT account_id,followers,ROW_NUMBER() OVER(PARTITION BY account_id ORDER BY day DESC) n
        FROM daily WHERE day<? AND followers IS NOT NULL) WHERE n=1''', (since,)):
        if r['account_id'] in ids:
            known_followers[r['account_id']] = r['followers']
    current_date = datetime.fromisoformat(since).date()
    while current_date <= now.astimezone(TZ).date():
        ds = current_date.isoformat()
        ds_rows = series[ds]
        for r in ds_rows:
            if r['followers'] is not None:
                known_followers[r['account_id']] = r['followers']
        def total(field):
            values = [r[field] for r in ds_rows if r[field] is not None]
            return sum(values) if values else None
        chart.append({'day': ds, 'followers': sum(known_followers.values()) if known_followers else None,
                      'follower_change': total('follower_change'), 'profile_coverage': len(known_followers),
                      'profile_observed': sum(r['followers'] is not None for r in ds_rows), 'views_gain': total('views_gain'),
                      'views_covered': sum(r['views_covered'] for r in ds_rows),
                      'views_expected': sum(r['views_expected'] for r in ds_rows)})
        current_date += timedelta(days=1)
    active = [a for a in chosen if a['active']]
    last = store.get('last_completed')
    running_until = store.get('running_until')
    result = {'summary': {'accounts': len(active), 'accounts_with_profile': sum(a['followers'] is not None for a in active),
             'followers': sum(a['followers'] or 0 for a in active), 'video_views': sum(a['video_views'] or 0 for a in chosen),
             'view_gains': sum(a['view_gains'] or 0 for a in chosen), 'needs_attention': sum(a['status'] != 'OK' for a in active),
             'published_posts': sum(a['published_posts'] for a in chosen),
             'posts_with_metrics': sum(a['posts_with_metrics'] for a in chosen),
             'stale_accounts': sum(a['stale'] for a in active)},
            'accounts': chosen, 'series': chart, 'groups': groups,
            'sync': {'last_completed': last, 'last_attempt': store.get('last_attempt'),
                     'errors': store.get('sync_errors', []), 'progress': store.get('progress', ''),
                     'running': bool(running_until and stamp(running_until) > now),
                     'next_due': iso(stamp(last) + timedelta(hours=24)) if last else None},
            'storage': {'bytes': store.path.stat().st_size, 'detailed_days': 90}, 'timezone': 'Asia/Bangkok'}
    if __package__:
        from .metrics import extend_report
    else:
        from metrics import extend_report
    extended = extend_report(store, result, now, days)
    last_attempt = store.get('last_attempt')
    if last_attempt:
        extended['sync']['next_due'] = iso(stamp(last_attempt) + timedelta(hours=1 if store.get('sync_errors') else 24))
    return extended


class BundleClient:
    def __init__(self, key=None):
        if key is None:
            key = next((line.split('=', 1)[1].strip().strip('\"').strip("'")
                        for line in (ROOT / '.env').read_text().splitlines()
                        if line.startswith('BUNDLE_SOCIAL_API_KEY=')), '')
        if not key:
            raise RuntimeError('BUNDLE_SOCIAL_API_KEY is missing from .env')
        self.key = key
        self.local = threading.local()

    def get(self, path, params=None):
        if not path.startswith('/api/v1/'):
            raise ValueError('Only documented Bundle API paths are allowed')
        if not hasattr(self.local, 'session'):
            self.local.session = requests.Session()
            self.local.session.headers.update({'x-api-key': self.key, 'User-Agent': 'Bundle-local-analytics/1.0'})
        for attempt in range(3):
            try:
                response = self.local.session.get('https://api.bundle.social' + path, params=params,
                                                 timeout=(15, 90), allow_redirects=False)
            except (requests.Timeout, requests.ConnectionError):
                if attempt == 2:
                    raise RuntimeError('Bundle connection failed after 3 GET attempts') from None
                time.sleep(2 ** (attempt + 1))
                continue
            if 200 <= response.status_code < 300:
                return response.json()
            if response.status_code in (408, 425, 429, 500, 502, 503, 504) and attempt < 2:
                try:
                    delay = min(float(response.headers.get('Retry-After', '0')), 60)
                except ValueError:
                    delay = 0
                time.sleep(max(2 ** (attempt + 1), delay))
                continue
            raise RuntimeError(f'Bundle HTTP {response.status_code}: {response.text[:300].replace(self.key, "[redacted]")}')

    def items(self, path, **params):
        offset = 0
        items = []
        while True:
            page = self.get(path, {**params, 'limit': 100, 'offset': offset})
            items.extend(page['items'])
            if len(items) >= page['total']:
                return items
            if not page['items']:
                raise RuntimeError('Bundle pagination stopped before its reported total')
            offset += 100


def sync(path=DB, client=None):
    store = Store(path)
    now = datetime.now(timezone.utc)
    if not store.claim(now):
        store.close()
        return {'skipped': True, 'reason': 'A sync is already running'}
    errors = []
    try:
        store.set('last_attempt', iso(now))
        store.set('progress', 'Finding Instagram accounts…')
        client = client or BundleClient()
        teams = client.items('/api/v1/team/')
        store.accounts(teams)
        active = [dict(r) for r in store.db.execute('SELECT * FROM accounts WHERE active=1')]

        def collect(a):
            result = {'account': a}
            try:
                result['profiles'] = client.get('/api/v1/analytics/social-account',
                    {'teamId': a['team_id'], 'platformType': 'INSTAGRAM'})['items']
            except Exception as exc:
                result['profile_error'] = str(exc)
            try:
                result['posts'] = client.items('/api/v1/post/', teamId=a['team_id'])
            except Exception as exc:
                result['posts_error'] = str(exc)
            try:
                result['audience'] = client.get('/api/v1/analytics/social-account/raw',
                    {'teamId': a['team_id'], 'platformType': 'INSTAGRAM'}).get('items', [])
            except Exception as exc:
                result['audience_error'] = str(exc)
            return result

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            for n, result in enumerate(pool.map(collect, active), 1):
                a = result['account']
                problems = [f'{a["username"]}: {result[k]}' for k in ('profile_error', 'posts_error') if k in result]
                errors.extend(problems)
                if 'profiles' in result:
                    store.profiles(a['id'], result['profiles'])
                if 'posts' in result:
                    store.posts(a['team_id'], result['posts'])
                store.audience(a['id'], result.get('audience', []), result.get('audience_error', ''))
                store.db.execute('UPDATE accounts SET fetch_error=? WHERE id=?', ('; '.join(problems), a['id']))
                store.set('progress', f'Account history {n}/{len(active)}')
                if n % 20 == 0:
                    LOG.info('Account history %s/%s', n, len(active))
        post_ids = [r[0] for r in store.db.execute('''SELECT p.id FROM posts p JOIN accounts a ON a.id=p.account_id
                    WHERE p.published_at IS NOT NULL AND a.active=1 ORDER BY p.id''')]
        batches = [post_ids[i:i + 20] for i in range(0, len(post_ids), 20)]

        def post_batch(ids):
            collected = []
            page = 1
            while True:
                result = client.get('/api/v1/analytics/post/bulk',
                                    {'postIds': ids, 'platformType': 'INSTAGRAM', 'page': page, 'limit': 20})
                collected.extend(result['results'])
                if page >= result['pagination']['totalPages']:
                    return collected
                page += 1

        def safe_batch(ids):
            try:
                return post_batch(ids), None
            except Exception as exc:
                return [], str(exc)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            for n, (results, error) in enumerate(pool.map(safe_batch, batches), 1):
                if error:
                    errors.append(f'Post batch {n}: {error}')
                for result in results:
                    pid = result['postId']
                    if result.get('error'):
                        errors.append(f'Post {pid}: {result["error"]}')
                    else:
                        store.post_metrics(pid, result.get('items', []))
                    store.db.execute('UPDATE posts SET analytics_error=? WHERE id=?', (result.get('error') or '', pid))
                store.set('progress', f'Post analytics {min(n * 20, len(post_ids))}/{len(post_ids)}')
                if n % 10 == 0:
                    LOG.info('Post analytics %s/%s', min(n * 20, len(post_ids)), len(post_ids))
        finished = datetime.now(timezone.utc)
        store.set('progress', 'Updating daily graphs…')
        automation = {'status': 'not_configured', 'message': 'Recipe comment-to-DM funnel and signup tracking are not configured.'}
        if active:
            try:
                flows = client.get('/api/v1/automations', {'teamId': active[0]['team_id'], 'limit': 1, 'offset': 0})
                automation['status'] = 'available' if 'total' in flows else 'not_configured'
            except Exception as exc:
                automation['status'] = 'not_enabled' if 'HTTP 404' in str(exc) else 'unavailable'
        store.set('automation_status', automation)
        store.rebuild(finished)
        store.prune(finished)
        store.set('last_completed', iso(finished))
        store.set('sync_errors', errors)
        store.set('progress', f'Updated {len(active)} accounts · {len(post_ids)} published posts')
        result = {'accounts': len(active), 'published_posts': len(post_ids), 'errors': errors,
                  'completed_at': iso(finished)}
        LOG.info('Sync completed: %s accounts, %s posts, %s source errors', len(active), len(post_ids), len(errors))
        return result
    except Exception as exc:
        errors.append(str(exc))
        store.set('sync_errors', errors)
        store.set('progress', 'Sync failed; previously saved data is preserved')
        LOG.exception('Analytics sync failed')
        return {'error': str(exc)}
    finally:
        store.release()
        store.close()


def due(store, now):
    last = store.get('last_attempt')
    if not last:
        return True
    delay = timedelta(hours=1 if store.get('sync_errors') else 24)
    return now - stamp(last) >= delay


def serve():
    def scheduler():
        while True:
            try:
                store = Store()
                needed = due(store, datetime.now(timezone.utc))
                store.close()
                if needed:
                    sync()
            except Exception:
                LOG.exception('Daily analytics loop failed')
            time.sleep(60)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        def send(self, status, content, kind='application/json'):
            self.send_response(status)
            self.send_header('Content-Type', kind + '; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            self.wfile.write(content if isinstance(content, bytes) else content.encode('utf-8'))

        def allowed(self):
            return self.headers.get('Host') in (f'127.0.0.1:{PORT}', f'localhost:{PORT}')

        def do_GET(self):
            if not self.allowed():
                self.send(403, '{}')
                return
            parsed = urlparse(self.path)
            if parsed.path == '/':
                self.send(200, (Path(__file__).with_name('index.html')).read_bytes(), 'text/html')
            elif parsed.path == '/metrics.js':
                self.send(200, Path(__file__).with_name('metrics.js').read_bytes(), 'text/javascript')
            elif parsed.path == '/help.js':
                self.send(200, Path(__file__).with_name('help.js').read_bytes(), 'text/javascript')
            elif parsed.path == '/api/report':
                params = parse_qs(parsed.query)
                try:
                    days = min(max(int(params.get('days', ['30'])[0]), 1), 3650)
                    store = Store()
                    try:
                        data = report(store, days=days, group=params.get('group', ['All'])[0])
                    finally:
                        store.close()
                    self.send(200, json.dumps(data))
                except Exception:
                    LOG.exception('Report failed')
                    self.send(500, '{"error":"Could not load saved analytics"}')
            else:
                self.send(404, '{}')

        def do_POST(self):
            origin = self.headers.get('Origin')
            if (not self.allowed() or self.headers.get('X-Dashboard') != '1' or
                    origin not in (None, f'http://127.0.0.1:{PORT}', f'http://localhost:{PORT}')):
                self.send(403, '{}')
                return
            if self.path != '/api/sync':
                self.send(404, '{}')
                return
            threading.Thread(target=sync, daemon=True).start()
            self.send(202, '{"started":true}')

    server = ThreadingHTTPServer(('127.0.0.1', PORT), Handler, bind_and_activate=False)
    server.allow_reuse_address = False
    if hasattr(socket, 'SO_EXCLUSIVEADDRUSE'):
        server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
    server.server_bind()
    server.server_activate()
    threading.Thread(target=scheduler, daemon=True).start()
    LOG.info('Dashboard serving at http://127.0.0.1:%s', PORT)
    server.serve_forever()


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(DATA / 'dashboard.log', maxBytes=512_000, backupCount=2, encoding='utf-8')
    logging.basicConfig(level=logging.INFO, handlers=[handler], format='%(asctime)s %(levelname)s %(message)s')
    parser = argparse.ArgumentParser(description='Local Bundle analytics dashboard')
    parser.add_argument('command', choices=['serve', 'sync', 'status'], default='serve', nargs='?')
    args = parser.parse_args()
    if args.command == 'serve':
        serve()
    elif args.command == 'sync':
        print(json.dumps(sync(), indent=2))
    else:
        store = Store()
        try:
            print(json.dumps(report(store)['sync'], indent=2))
        finally:
            store.close()


if __name__ == '__main__':
    main()
