import importlib.util
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


class AnalyticsTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('dashboard.app'), 'Dashboard storage is not implemented yet')
        from dashboard.app import Store
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Store(Path(self.tmp.name) / 'analytics.sqlite3')
        self.addCleanup(self.store.close)
        self.store.accounts([{'id': 'team', 'name': 'JOJI-name', 'socialAccounts': [
            {'id': 'a', 'username': 'name', 'type': 'INSTAGRAM', 'createdAt': '2026-10-01T00:00:00Z'}]}])

    def profiles(self, values):
        self.store.profiles('a', [{'id': f'p{day}', 'createdAt': f'2026-10-{day:02d}T05:00:00Z',
                                 'followers': count} for day, count in values])

    def post(self, published='2026-10-20T04:00:00Z'):
        self.store.posts('team', [{'id': 'post', 'status': 'POSTED', 'postDate': published,
                                  'postedDate': published, 'socialAccounts': [
            {'socialAccountId': 'a', 'externalPostId': 'ig', 'socialAccount': {'id': 'a', 'type': 'INSTAGRAM'}}],
            'externalData': {'INSTAGRAM': {'permalink': 'https://www.instagram.com/reel/example/'}}}])

    def metrics(self, values):
        self.store.post_metrics('post', [{'id': f'v{day}', 'createdAt': f'2026-10-{day:02d}T06:00:00Z',
                                          'views': views} for day, views in values])

    def rebuild(self, now='2026-10-25T09:00:00+07:00'):
        self.store.rebuild(datetime.fromisoformat(now))

    def day(self, date):
        return dict(self.store.db.execute('SELECT * FROM daily WHERE account_id=? AND day=?', ('a', date)).fetchone())

    def test_repeated_catchup_does_not_duplicate_and_accepts_corrected_snapshots(self):
        self.profiles([(21, 10), (22, 12), (23, 15)])
        self.profiles([(21, 10), (22, 12), (23, 16)])
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM profiles').fetchone()[0], 3)
        self.rebuild()
        self.assertEqual(self.day('2026-10-23')['followers'], 16)
        self.assertEqual(self.day('2026-10-23')['follower_change'], 4)

    def test_lifetime_view_differences_are_daily_gains(self):
        self.post(); self.metrics([(21, 200), (22, 350), (23, 500)])
        self.rebuild()
        self.assertIsNone(self.day('2026-10-21')['views_gain'])
        self.assertEqual(self.day('2026-10-22')['views_gain'], 150)
        self.assertEqual(self.day('2026-10-22')['views_covered'], 1)

    def test_missing_day_is_not_filled_with_zero_or_multi_day_gain(self):
        self.profiles([(21, 10), (23, 15)])
        self.post(); self.metrics([(21, 200), (23, 500)])
        self.rebuild()
        self.assertIsNone(self.day('2026-10-23')['views_gain'])
        self.assertIsNone(self.day('2026-10-23')['follower_change'])

    def test_first_publication_day_has_valid_zero_baseline(self):
        self.post('2026-10-21T03:00:00Z'); self.metrics([(21, 200)])
        self.rebuild()
        self.assertEqual(self.day('2026-10-21')['views_gain'], 200)

    def test_negative_view_correction_is_unknown_not_fake_positive(self):
        self.post(); self.metrics([(21, 350), (22, 200)])
        self.rebuild()
        self.assertIsNone(self.day('2026-10-22')['views_gain'])

    def test_retention_keeps_old_daily_summaries_and_post_baseline(self):
        self.profiles([(21, 10), (22, 12)])
        self.post(); self.metrics([(21, 200), (22, 350)])
        self.rebuild(); original = self.day('2026-10-22')
        self.store.prune(datetime(2027, 3, 1, tzinfo=timezone.utc))
        self.rebuild('2027-03-01T09:00:00+07:00')
        self.assertEqual(self.day('2026-10-22')['views_gain'], original['views_gain'])
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM post_snapshots').fetchone()[0], 1)

    def test_empty_profile_is_missing_not_zero(self):
        self.store.profiles('a', [])
        self.rebuild()
        from dashboard.app import report
        data = report(self.store, datetime.fromisoformat('2026-10-25T09:00:00+07:00'))
        self.assertIsNone(data['accounts'][0]['followers'])
        self.assertEqual(data['summary']['accounts_with_profile'], 0)

    def test_discovery_keeps_history_when_connection_disappears(self):
        self.profiles([(21, 10)]); self.store.accounts([])
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM profiles').fetchone()[0], 1)
        self.assertEqual(self.store.db.execute('SELECT active FROM accounts').fetchone()[0], 0)

    def test_simultaneous_sync_lease_and_release(self):
        now = datetime(2026, 10, 25, tzinfo=timezone.utc)
        self.assertTrue(self.store.claim(now))
        self.assertFalse(self.store.claim(now))
        self.store.release()
        self.assertTrue(self.store.claim(now))

    def test_follower_chart_keeps_last_known_count_when_one_source_misses_a_day(self):
        self.store.accounts([{'id': 'team', 'name': 'JOJI-name', 'socialAccounts': [
            {'id': 'a', 'username': 'name', 'type': 'INSTAGRAM'},
            {'id': 'b', 'username': 'second', 'type': 'INSTAGRAM'}]}])
        self.profiles([(21, 10), (22, 12)])
        self.store.profiles('b', [{'id': 'b21', 'createdAt': '2026-10-21T05:00:00Z', 'followers': 20}])
        self.rebuild()
        from dashboard.app import report
        chart = report(self.store, datetime.fromisoformat('2026-10-23T09:00:00+07:00'))['series']
        point = next(p for p in chart if p['day'] == '2026-10-22')
        self.assertEqual(point['followers'], 32)

    def test_live_shape_collector_catches_up_twice_without_duplicates_and_continues_errors(self):
        from dashboard.app import sync
        teams = [{'id': 'team', 'name': 'JOJI-name', 'socialAccounts': [
            {'id': 'a', 'username': 'name', 'type': 'INSTAGRAM'}]},
            {'id': 'other', 'name': 'CL-second', 'socialAccounts': [
            {'id': 'b', 'username': 'second', 'type': 'INSTAGRAM'}]}]
        class Client:
            def items(self, path, **params):
                if path == '/api/v1/team/':
                    return teams
                if params['teamId'] == 'other':
                    return []
                return [{'id': 'post', 'status': 'POSTED', 'postDate': '2026-10-21T03:00:00Z',
                         'postedDate': '2026-10-21T03:01:00Z', 'socialAccounts': [
                    {'socialAccountId': 'a', 'externalPostId': 'ig', 'socialAccount': {'type': 'INSTAGRAM'}}]}]

            def get(self, path, params):
                if path == '/api/v1/analytics/social-account':
                    if params['teamId'] == 'other':
                        raise RuntimeError('One account cannot supply analytics')
                    return {'items': [{'id': 'p21', 'createdAt': '2026-10-21T05:00:00Z', 'followers': 3}]}
                return {'results': [{'postId': 'post', 'error': None, 'items': [
                    {'id': 'v21', 'createdAt': '2026-10-21T06:00:00Z', 'views': 25}]}],
                        'pagination': {'totalPages': 1}}
        for _ in range(2):
            result = sync(self.store.path, Client())
            self.assertEqual(result['accounts'], 2)
            self.assertEqual(len(result['errors']), 1)
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM profiles').fetchone()[0], 1)
        self.assertEqual(self.store.db.execute('SELECT COUNT(*) FROM post_snapshots').fetchone()[0], 1)
        self.assertIn('cannot supply', self.store.db.execute("SELECT fetch_error FROM accounts WHERE id='b'").fetchone()[0])

    def test_pagination_cannot_silently_drop_rows(self):
        from dashboard.app import BundleClient
        class Client(BundleClient):
            def get(self, path, params):
                return {'items': [{'id': 'first'}] if params['offset'] == 0 else [], 'total': 2}
        with self.assertRaisesRegex(RuntimeError, 'pagination stopped'):
            Client('dummy-key').items('/api/v1/team/')


if __name__ == '__main__':
    unittest.main()
