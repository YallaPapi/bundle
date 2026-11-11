import importlib.util
import tempfile
import unittest
from pathlib import Path
from datetime import datetime
from dashboard.app import Store, report


NOW = datetime.fromisoformat('2026-10-26T10:00:00+07:00')


class ExpandedMetricsTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('dashboard.metrics'), 'Expanded analytics is not implemented yet')
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = Store(Path(self.tmp.name) / 'test.sqlite3')
        self.addCleanup(self.store.close)
        self.store.accounts([{'id': 'team', 'name': 'JOJI-test', 'socialAccounts': [
            {'id': 'a', 'username': 'test', 'type': 'INSTAGRAM'}]}])

    def profile(self, day, visits):
        self.store.profiles('a', [{'id': f'a{day}', 'createdAt': f'2026-10-{day}T02:00:00Z',
            'followers': 10, 'following': 4, 'views': visits, 'impressions': 200,
            'impressionsUnique': 150, 'likes': 8, 'comments': 2, 'postCount': 3}])

    def post(self, pid, views, likes, shares=0, saves=0, status='POSTED', published='2026-10-24T02:00:00Z'):
        self.store.posts('team', [{'id': pid, 'status': status, 'postDate': published, 'postedDate': published,
            'title': 'Cookie video '+pid, 'data': {'INSTAGRAM': {'text': 'Try these cookies'}},
            'socialAccounts': [{'socialAccountId': 'a', 'externalPostId': 'ig-'+pid if status=='POSTED' else None,
                                'socialAccount': {'type':'INSTAGRAM'}}],
            'externalData': {'INSTAGRAM': {'permalink': 'https://www.instagram.com/reel/'+pid+'/'}}}])
        if status == 'POSTED':
            self.store.post_metrics(pid, [{'id': 'm'+pid, 'createdAt':'2026-10-25T02:00:00Z',
              'views': views, 'impressions': views, 'impressionsUnique': 50,
              'likes': likes, 'comments': 0, 'shares': shares, 'saves': saves}])

    def result(self):
        self.store.rebuild(NOW)
        return report(self.store, NOW, days=7)

    def test_profile_visits_remain_rolling_totals_not_daily_differences(self):
        self.profile(24,100);self.profile(25,80)
        r=self.result()
        self.assertEqual(r['profile_metrics']['profile_views'],80)
        self.assertEqual(next(d for d in r['series'] if d['day']=='2026-10-25')['profile_views'],80)
        self.assertEqual(r['profile_metrics']['following'],4)

    def test_weighted_engagement_and_median_and_per_thousand(self):
        self.post('one',100,10,shares=2,saves=3);self.post('two',900,0)
        r=self.result()['performance']
        self.assertEqual(r['engagement_rate'],1.5)
        self.assertEqual(r['average_views'],500)
        self.assertEqual(r['median_views'],500)
        self.assertEqual(r['shares_per_1000'],2)
        self.assertEqual(r['saves_per_1000'],3)

    def test_missing_fields_and_zero_denominator_are_unknown(self):
        self.post('one',0,None)
        r=self.result()['performance']
        self.assertIsNone(r['likes'])
        self.assertIsNone(r['engagement_rate'])
        self.assertIsNone(r['shares_per_1000'])

    def test_top_videos_include_correct_identity_and_metrics(self):
        self.post('one',100,10);self.post('two',900,20)
        rows=self.result()['top_posts']
        self.assertEqual(rows[0]['post_id'],'two')
        self.assertEqual(rows[0]['external_id'],'ig-two')
        self.assertEqual(rows[0]['reach'],50)
        self.assertEqual(rows[0]['username'],'test')

    def test_posting_success_uses_attempts_in_range_not_scheduled_future(self):
        self.post('ok',100,10);self.post('bad',0,0,status='ERROR')
        self.post('future',0,0,status='SCHEDULED',published='2026-11-01T02:00:00Z')
        r=self.result()['publishing']
        self.assertEqual(r['published'],1);self.assertEqual(r['failed'],1)
        self.assertEqual(r['scheduled'],1);self.assertEqual(r['success_rate'],50)

    def test_removed_accounts_excluded_from_all_current_totals(self):
        self.profile(25,80);self.post('one',100,10)
        self.store.accounts([])
        r=self.result()
        self.assertEqual(r['accounts'],[])
        self.assertIsNone(r['profile_metrics']['profile_views'])
        self.assertEqual(r['top_posts'],[])

    def test_documented_audience_breakdown_parsing(self):
        from dashboard.metrics import parse_audience
        raw={'demographics':{'follower_demographics':{'country':{'data':[{'total_value':{'breakdowns':[
              {'dimension_keys':['country'],'results':[{'dimension_values':['US'],'value':123}]}]}}]}},
              'follows_and_unfollows_by_follow_type':{'follows':20,'unfollows':3,'unknown':0}},
             'onlineFollowers':{'data':[{'values':[{'end_time':'2026-10-25T00:00:00Z','value':{'0':5,'1':8}}]}]}}
        result=parse_audience(raw)
        self.assertEqual(result['followers']['country']['US'],123)
        self.assertEqual(result['follows'],20)
        self.assertEqual(result['online']['hours']['1'],8)

    def test_unavailable_raw_data_is_not_zero_demographics(self):
        self.store.audience('a', [])
        r=self.result()['audience']
        self.assertEqual(r['accounts_with_data'],0)
        self.assertIsNone(r['follows'])


if __name__=='__main__':unittest.main()
