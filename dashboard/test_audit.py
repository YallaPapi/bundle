import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from dashboard.app import Store,report

NOW=datetime.fromisoformat('2026-10-26T10:00:00+07:00')


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.s=Store(Path(self.tmp.name)/'test.sqlite3');self.addCleanup(self.s.close)
        self.s.accounts([{'id':'t','name':'JOJI-test','socialAccounts':[
            {'id':'a','username':'test','type':'INSTAGRAM'}]}])

    def post(self,pid='p',published='2026-10-24T02:00:00Z',external='ig-p'):
        self.s.posts('t',[{'id':pid,'status':'POSTED','postDate':published,'postedDate':published,
          'socialAccounts':[{'socialAccountId':'a','externalPostId':external,'socialAccount':{'type':'INSTAGRAM'}}]}])

    def metric(self,pid='p',sid='s',at='2026-10-25T02:00:00Z',views=100):
        self.s.post_metrics(pid,[{'id':sid,'createdAt':at,'views':views,
              'likes':10,'comments':2,'shares':3,'saves':1,'impressions':views,'impressionsUnique':80}])

    def test_unknown_view_gains_and_video_totals_are_not_zero(self):
        self.post();self.metric(views=None);self.s.rebuild(NOW)
        r=report(self.s,NOW,days=1)
        self.assertIsNone(r['accounts'][0]['view_gains'])
        self.assertIsNone(r['accounts'][0]['video_views'])
        self.assertEqual(r['summary']['posts_with_metrics'],0)

    def test_identical_account_fields_get_an_explicit_source_warning(self):
        self.s.accounts([{'id':'t','name':'JOJI-test','socialAccounts':[
          {'id':'a','username':'test','type':'INSTAGRAM'}, {'id':'b','username':'test2','type':'INSTAGRAM'}]}])
        for aid in ['a','b']:
            self.s.profiles(aid,[{'id':'s'+aid,'createdAt':'2026-10-25T01:00:00Z',
                  'followers':2,'impressions':100,'impressionsUnique':100}])
        r=report(self.s,NOW)
        self.assertTrue(r['quality']['profile_reach_impressions_identical'])
        self.assertEqual(r['quality']['matching_profile_fields'],2)

    def test_all_time_does_not_follow_publication_date_filter(self):
        self.post(published='2026-10-01T02:00:00Z');self.metric()
        r=report(self.s,NOW,days=1)
        self.assertEqual(r['top_posts'],[])
        self.assertEqual(r['all_time']['views'],100)
        self.assertEqual(r['all_time']['posts'],1)
        self.assertIsNone(r['all_time']['profile_views'])

    def test_lifetime_totals_survive_detailed_history_cleanup_and_old_backfill(self):
        self.post();self.metric(at='2026-10-25T02:00:00Z',views=150)
        self.metric(sid='old',at='2026-10-24T02:00:00Z',views=100)
        self.s.db.execute('DELETE FROM post_snapshots');self.s.db.commit()
        r=report(self.s,NOW)
        self.assertEqual(r['all_time']['views'],150)

    def test_same_instagram_video_is_not_counted_twice(self):
        self.post('p',external='same-ig');self.post('duplicate',external='same-ig')
        self.metric('p','one');self.metric('duplicate','two')
        r=report(self.s,NOW)
        self.assertEqual(r['all_time']['views'],100)
        self.assertEqual(r['all_time']['posts'],1)
        self.assertEqual(r['quality']['duplicate_instagram_post_ids'],1)

    def test_daily_gains_also_count_one_instagram_video_once(self):
        self.post('p',external='same-ig');self.post('duplicate',external='same-ig')
        self.metric('p','one',at='2026-10-24T03:00:00Z')
        self.metric('duplicate','two',at='2026-10-24T03:00:00Z')
        self.s.rebuild(NOW)
        d=self.s.db.execute("SELECT views_gain,views_expected FROM daily WHERE day='2026-10-24'").fetchone()
        self.assertEqual(d['views_gain'],100)
        self.assertEqual(d['views_expected'],1)

    def test_partial_weekly_coverage_does_not_create_a_growth_percentage(self):
        for day in range(12,26):
            self.s.db.execute('''INSERT INTO daily(account_id,day,followers,follower_change,
              views_gain,views_covered,views_expected) VALUES(?,?,?,?,?,?,?)''',
              ('a',f'2026-10-{day}',1,0,1 if day<19 else 2,1,2))
        self.s.db.commit();c=report(self.s,NOW)['weekly_comparison']['views_gain']
        self.assertIsNone(c['change_percent'])
        self.assertEqual(c['reason'],'partial_coverage')

    def test_zero_previous_week_has_an_accurate_explanation(self):
        for day in range(12,26):
            self.s.db.execute('''INSERT INTO daily(account_id,day,followers,follower_change,
              views_gain,views_covered,views_expected) VALUES(?,?,?,?,?,?,?)''',
              ('a',f'2026-10-{day}',1,0,0,1,1))
        self.s.db.commit();c=report(self.s,NOW)['weekly_comparison']['views_gain']
        self.assertEqual(c['reason'],'zero_or_negative_baseline')


if __name__=='__main__':unittest.main()
