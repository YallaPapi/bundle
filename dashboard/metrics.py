"""Derived analytics with explicit scopes, nullable values and source periods."""
import json
import statistics
from collections import defaultdict
from datetime import datetime, timedelta, timezone

TZ = timezone(timedelta(hours=7))
PROFILE_FIELDS = ('profile_views', 'impressions', 'reach', 'likes', 'comments', 'post_count', 'following')
ENGAGEMENT = ('likes', 'comments', 'shares', 'saves')


def timestamp(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)


def local_day(value):
    return timestamp(value).astimezone(TZ).date().isoformat()


def known_sum(values):
    values = [v for v in values if isinstance(v, (int, float))]
    return sum(values) if values else None


def ratio(numerator, denominator, multiplier=100):
    return numerator / denominator * multiplier if numerator is not None and denominator is not None and denominator > 0 else None


def breakdown(payload):
    result = defaultdict(float)
    if not isinstance(payload, dict):
        return {}
    for item in payload.get('data', []):
        for b in item.get('total_value', {}).get('breakdowns', []):
            for r in b.get('results', []):
                if isinstance(r.get('value'), (int, float)):
                    result[' / '.join(map(str, r.get('dimension_values', [])))] += r['value']
    return dict(result)


def parse_audience(raw):
    if not isinstance(raw, dict):
        return {}
    demographics = raw.get('demographics') or {}
    output = {}
    for source, name in [('follower_demographics', 'followers'), ('engaged_audience_demographics', 'engaged')]:
        payload = demographics.get(source) or {}
        output[name] = {dimension: breakdown(payload.get(dimension)) for dimension in ('country', 'city', 'age', 'gender')}
    output['age_gender'] = breakdown(demographics.get('follower_demographics_age_gender'))
    counts = demographics.get('follows_and_unfollows_by_follow_type') or {}
    output['follows'] = counts.get('follows')
    output['unfollows'] = counts.get('unfollows')
    online = raw.get('onlineFollowers') or {}
    observations = [v for item in online.get('data', []) for v in item.get('values', [])
                    if v.get('end_time') and isinstance(v.get('value'), dict)]
    newest = max(observations, key=lambda v: timestamp(v['end_time']), default=None)
    output['online'] = {'at': newest['end_time'], 'hours': newest['value']} if newest else None
    # The docs name these fields but do not define their contents. Do not guess a daily schema.
    output['daily_reach_payload_present'] = bool(raw.get('reachTimeSeries'))
    output['reach_split_payload_present'] = bool(raw.get('reachByFollowType'))
    return output


def performance(rows):
    result = {'posts': len(rows)}
    for field in ('views', 'impressions', 'reach', *ENGAGEMENT):
        result[field] = known_sum(r.get(field) for r in rows)
        result[field + '_coverage'] = sum(r.get(field) is not None for r in rows)
    view_values = [r['views'] for r in rows if r.get('views') is not None]
    result['average_views'] = statistics.mean(view_values) if view_values else None
    result['median_views'] = statistics.median(view_values) if view_values else None
    matched = [r for r in rows if r.get('views') is not None and r['views'] > 0 and
               all(r.get(f) is not None for f in ENGAGEMENT)]
    result['engagement_rate'] = ratio(known_sum(sum(r[f] for f in ENGAGEMENT) for r in matched),
                                      known_sum(r['views'] for r in matched))
    result['engagement_rate_coverage'] = len(matched)
    for field in ('likes', 'comments', 'shares', 'saves'):
        matched_field = [r for r in rows if r.get(field) is not None and r.get('views') is not None and r['views'] > 0]
        result[field + '_per_1000'] = ratio(known_sum(r[field] for r in matched_field),
                                           known_sum(r['views'] for r in matched_field), 1000)
    return result


def extend_report(store, data, now, days):
    accounts = {a['id']: a for a in data['accounts']}
    ids = set(accounts)
    since = (now.astimezone(TZ).date() - timedelta(days=days - 1)).isoformat()
    first = datetime.fromisoformat(since).replace(tzinfo=TZ)
    profiles = {}
    history = []
    for r in store.db.execute('SELECT * FROM profiles ORDER BY observed_at'):
        if r['account_id'] in ids:
            r = dict(r)
            profiles[r['account_id']] = r
            history.append(r)
    profile_metrics = {'coverage': {}, 'period': 'Rolling 30 days; followers/following/post count are latest snapshots'}
    for field in PROFILE_FIELDS:
        profile_metrics[field] = known_sum(r[field] for r in profiles.values())
        profile_metrics['coverage'][field] = sum(r[field] is not None for r in profiles.values())
    data['profile_metrics'] = profile_metrics
    for aid, a in accounts.items():
        for field in PROFILE_FIELDS:
            a[field] = profiles[aid][field] if aid in profiles else None
            a['profile_' + field] = a[field]
    snapshots = {}
    for r in store.db.execute('SELECT * FROM post_totals'):
        snapshots[r['post_id']] = dict(r)
    posts = [dict(r) for r in store.db.execute('SELECT * FROM posts') if r['account_id'] in ids]
    identities = {}
    for p in posts:
        if not p['published_at']:
            continue
        identity = (p['account_id'], p['external_id'] or p['id'])
        previous = identities.get(identity)
        current_time = snapshots.get(p['id'], {}).get('observed_at') or ''
        previous_time = snapshots.get(previous['id'], {}).get('observed_at') or '' if previous else ''
        if previous is None or (current_time, p['id']) > (previous_time, previous['id']):
            identities[identity] = p
    canonical_ids = {p['id'] for p in identities.values()}
    duplicates = sum(p['published_at'] is not None for p in posts) - len(canonical_ids)
    all_time_posts = []
    top = []
    for p in posts:
        if p['id'] not in canonical_ids or timestamp(p['published_at']) > now:
            continue
        s = snapshots.get(p['id'], {})
        row = {'post_id': p['id'], 'external_id': p['external_id'], 'username': accounts[p['account_id']]['username'],
               'account_id': p['account_id'], 'team': accounts[p['account_id']]['team'], 'title': p['title'],
               'caption': (p['caption'] or '')[:300], 'published_at': p['published_at'], 'permalink': p['permalink'],
               'updated_at': s.get('observed_at')}
        for field in ('views', 'impressions', 'reach', *ENGAGEMENT):
            row[field] = s.get(field)
        row['engagement_rate'] = performance([row])['engagement_rate']
        row['stale'] = not row['updated_at'] or now - timestamp(row['updated_at']) > timedelta(hours=36)
        all_time_posts.append(row)
        if first <= timestamp(p['published_at']):
            top.append(row)
    top.sort(key=lambda r: r['views'] if r['views'] is not None else -1, reverse=True)
    data['top_posts'] = top
    data['performance'] = performance(top)
    data['performance']['period'] = 'Posts published in selected period; latest lifetime metrics'
    data['all_time'] = performance(all_time_posts)
    data['all_time'].update({'profile_views': None, 'profile_reach': None,
        'oldest_tracked_post': min((p['published_at'] for p in all_time_posts), default=None),
        'storage': 'One permanent latest-total record per video; updates replace older totals, never add them.'})
    data['summary']['video_views'] = data['all_time']['views']
    data['summary']['published_posts'] = len(all_time_posts)
    data['summary']['posts_with_metrics'] = data['all_time']['views_coverage']
    data['summary']['view_gains'] = known_sum(a['view_gains'] for a in accounts.values())
    data['summary']['followers'] = known_sum(a['followers'] for a in accounts.values())
    # Keep account and network totals on the same deduplicated set of actual Instagram videos.
    for aid, a in accounts.items():
        own = [p for p in all_time_posts if p['account_id'] == aid]
        a['video_views'] = known_sum(p['views'] for p in own)
        a['published_posts'] = len(own)
        a['posts_with_metrics'] = sum(p['views'] is not None for p in own)
    by_account = defaultdict(list)
    for row in top:
        by_account[row['account_id']].append(row)
    for aid, a in accounts.items():
        metrics = performance(by_account[aid])
        for field in (*ENGAGEMENT, 'impressions', 'reach', 'engagement_rate', 'average_views', 'median_views',
                      'comments_per_1000', 'shares_per_1000', 'saves_per_1000'):
            a[field] = metrics[field]
    publishing = {'published': 0, 'failed': 0, 'scheduled': 0, 'processing': 0}
    outcomes = defaultdict(lambda: {'published': 0, 'failed': 0})
    account_outcomes = defaultdict(lambda: {'published': 0, 'failed': 0, 'scheduled': 0})
    for p in posts:
        if p['published_at'] and p['id'] not in canonical_ids:
            continue
        if p['status'] == 'SCHEDULED' and p['scheduled_at'] and timestamp(p['scheduled_at']) > now:
            publishing['scheduled'] += 1
            account_outcomes[p['account_id']]['scheduled'] += 1
        at = p['attempted_at'] or p['scheduled_at']
        if not at or not first <= timestamp(at) <= now:
            continue
        if p['status'] in ('POSTED', 'ERROR'):
            field = 'published' if p['status'] == 'POSTED' else 'failed'
            publishing[field] += 1
            account_outcomes[p['account_id']][field] += 1
            outcomes[local_day(at)][field] += 1
        elif p['status'] in ('PROCESSING', 'RETRYING'):
            publishing['processing'] += 1
    publishing['success_rate'] = ratio(publishing['published'], publishing['published'] + publishing['failed'])
    for aid, a in accounts.items():
        a['publishing'] = account_outcomes[aid]
        a['success_rate'] = ratio(account_outcomes[aid]['published'],
                                  account_outcomes[aid]['published'] + account_outcomes[aid]['failed'])
    data['publishing'] = publishing
    # Keep source rolling totals on their own trend; carry forward latest observed values.
    seed = {}
    per_day = defaultdict(dict)
    for p in history:
        d = local_day(p['observed_at'])
        if d < since:
            seed[p['account_id']] = p
        else:
            per_day[d][p['account_id']] = p
    daily = [dict(r) for r in store.db.execute('SELECT * FROM daily ORDER BY day') if r['account_id'] in ids]
    changes = defaultdict(list)
    for r in daily:
        changes[r['day']].append(r)
    for point in data['series']:
        seed.update(per_day[point['day']])
        for field in PROFILE_FIELDS:
            point[field] = known_sum(p[field] for p in seed.values())
        for field in ENGAGEMENT:
            point[field + '_gain'] = known_sum(r[field + '_gain'] for r in changes[point['day']])
            point[field + '_covered'] = sum(r[field + '_covered'] or 0 for r in changes[point['day']])
        point['published'] = outcomes[point['day']]['published']
        point['failed'] = outcomes[point['day']]['failed']
        point['is_today'] = point['day'] == now.astimezone(TZ).date().isoformat()
    today = now.astimezone(TZ).date()
    comparisons = {}
    for metric in ('views_gain', 'follower_change', *(f'{f}_gain' for f in ENGAGEMENT)):
        ranges = []
        coverage = []
        for offset in (0, 7):
            values = [known_sum(r[metric] for r in changes[(today - timedelta(days=i + offset)).isoformat()])
                      for i in range(1, 8)]
            ranges.append(sum(values) if all(v is not None for v in values) else None)
            full = True
            for i in range(1, 8):
                d = (today - timedelta(days=i + offset)).isoformat()
                rows = changes[d]
                if metric == 'follower_change':
                    eligible = sum(not a.get('created_at') or local_day(a['created_at']) < d for a in accounts.values())
                    complete = sum(r['follower_change'] is not None for r in rows) >= eligible and eligible > 0
                else:
                    field = metric.replace('_gain', '') + '_covered'
                    expected = sum(r['views_expected'] for r in rows)
                    complete = expected > 0 and sum(r[field] or 0 for r in rows) >= expected
                full = full and complete
            coverage.append(full)
        current, previous = ranges
        reason = ('missing_readings' if current is None or previous is None else
                  'partial_coverage' if not all(coverage) else
                  'zero_or_negative_baseline' if previous <= 0 else 'comparable')
        comparisons[metric] = {'current': current, 'previous': previous, 'reason': reason,
              'current_complete': coverage[0], 'previous_complete': coverage[1],
              'change_percent': ratio(current - previous, previous) if reason == 'comparable' else None}
    data['weekly_comparison'] = comparisons
    audiences = [dict(r) for r in store.db.execute('SELECT * FROM audience') if r['account_id'] in ids]
    combined = {'accounts_with_data': 0, 'accounts_checked': len(audiences), 'followers': {}, 'engaged': {},
                'follows': None, 'unfollows': None, 'online': {}, 'age_gender': {},
                'daily_reach_available': False, 'reach_split_available': False, 'source_errors': []}
    parsed = []
    for row in audiences:
        if row['error'] and 'No raw analytics' not in row['error']:
            combined['source_errors'].append({'username': accounts[row['account_id']]['username'], 'error': row['error']})
        if not row['data']:
            continue
        item = json.loads(row['data'])
        has_data = any(item.get(group, {}).get(k) for group in ('followers', 'engaged') for k in ('country', 'city', 'age', 'gender'))
        has_data = has_data or item.get('online') or item.get('follows') is not None or item.get('unfollows') is not None
        if has_data:
            combined['accounts_with_data'] += 1
        parsed.append(item)
    for group in ('followers', 'engaged'):
        for dim in ('country', 'city', 'age', 'gender'):
            totals = defaultdict(float)
            for item in parsed:
                for label, count in item.get(group, {}).get(dim, {}).items():
                    totals[label] += count
            combined[group][dim] = dict(sorted(totals.items(), key=lambda pair: pair[1], reverse=True))
    for field in ('follows', 'unfollows'):
        combined[field] = known_sum(item.get(field) for item in parsed)
    for item in parsed:
        for label, count in item.get('age_gender', {}).items():
            combined['age_gender'][label] = combined['age_gender'].get(label, 0) + count
        if item.get('online'):
            for hour, count in item['online']['hours'].items():
                if isinstance(count, (int, float)) and str(hour).isdigit():
                    combined['online'][str(hour)] = combined['online'].get(str(hour), 0) + count
    data['audience'] = combined
    data['funnel'] = store.get('automation_status', {'status': 'not_configured', 'message': 'Recipe funnel is not configured.'})
    comparable = [p for p in profiles.values() if p['reach'] is not None and p['impressions'] is not None]
    matching = sum(p['reach'] == p['impressions'] for p in comparable)
    identical = len(comparable) > 1 and matching == len(comparable) and any(p['reach'] > 0 for p in comparable)
    quality = {'profile_reach_impressions_identical': identical, 'matching_profile_fields': matching,
               'profile_fields_checked': len(comparable), 'duplicate_instagram_post_ids': duplicates,
               'active_accounts': len(accounts), 'source_profile_post_count': profile_metrics['post_count'],
               'tracked_video_count': len(all_time_posts),
               'stale_video_readings': sum(p['stale'] for p in all_time_posts),
               'partial_activity_days': [p['day'] for p in data['series'] if p['views_expected']>p['views_covered']],
               'scope_note': 'Account figures cover all content in each account over the last 30 days. Video figures cover only the videos tracked here. Their totals cannot be directly reconciled.'}
    data['quality'] = quality
    def time_range(values):
        values = [v for v in values if v]
        return {'oldest': min(values) if values else None, 'newest': max(values) if values else None}
    data['source_times'] = {'profiles': time_range(p['observed_at'] for p in profiles.values()),
                            'videos': time_range(p['updated_at'] for p in all_time_posts),
                            'downloaded_at': data['sync']['last_completed']}
    return data
