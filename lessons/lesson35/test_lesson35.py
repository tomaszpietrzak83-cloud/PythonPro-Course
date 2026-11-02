"""Exercise all real local scenarios and meaningful failure/boundary cases."""
import contextlib
from datetime import timedelta
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
(ROOT/'.runtime').mkdir(exist_ok=True)
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT/'examples'))
from demo_support import LocalCloud
from run_task import load_task


class Scenarios(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(dir=ROOT/'.runtime')
        cls.results = {}
        # Demonstrations must never create a real AWS session or execute a shell.
        with patch('boto3.session.Session', side_effect=AssertionError('Real AWS session')), patch('subprocess.run', side_effect=AssertionError('External command')):
            for number in range(1, 21):
                work = Path(cls.temp.name)/str(number)
                work.mkdir()
                cls.results[number] = load_task(number).demo(work, LocalCloud())

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_all_twenty_expected_results(self):
        r = self.results
        self.assertEqual([x['status'] for x in r[1]], [200, 200, 503])
        self.assertEqual([x['ok'] for x in r[1]], [True, True, False])
        self.assertTrue(r[2]['success'])
        self.assertEqual(len(r[3]), 3)
        self.assertEqual(r[4], {'first': 'created', 'second': 'already exists'})
        self.assertEqual(r[5]['uploaded'], ['photo.jpg'])
        self.assertEqual(len(r[6]), 3)
        self.assertIsNone(r[6][1]['ip'])
        self.assertEqual(r[7], {'ERROR': 2, 'WARNING': 0, 'INFO': 1})
        self.assertEqual(r[8]['AWS_SECRET_ACCESS_KEY'], 'WARNING: missing')
        self.assertNotIn('test-only', json.dumps(r[8]))
        self.assertEqual(r[9]['plan'], [{'id': 'i-demo-dev', 'action': 'planned'}])
        self.assertEqual(r[10]['removed'], ['backups/old.zip'])
        self.assertEqual(r[11]['copied'], ['data/report.txt'])
        self.assertEqual([x['estimated_usd'] for x in r[12]], ['0.2400', '0.2000'])
        self.assertEqual([r[13][k]['status'] for k in ['success', 'test_failure', 'recovery']], ['deployed', 'failed', 'rolled back'])
        self.assertEqual(len(r[13]['test_failure']['history']), 2)
        self.assertEqual(r[14]['files'], ['index.html'])
        self.assertEqual(len(r[15]['alerts']), 2)
        self.assertEqual(len(r[16]), 20)
        self.assertEqual([x['action'] for x in r[16] if x['action'] != 'hold'], ['start', 'stop'])
        self.assertEqual(r[17]['thumbnail_size'], (128, 64))
        self.assertEqual(r[17]['second'], [])
        self.assertEqual(len(r[18]['differences']), 3)
        self.assertTrue(r[19]['verified'])
        self.assertIn('$2.16/month', r[20]['report'])
        self.assertIn('$4.0/month', r[20]['report'])

    def test_backup_rejects_recursive_destination(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'.runtime') as directory:
            source = Path(directory)
            with self.assertRaises(ValueError):
                load_task(2).backup_directory(source, source/'backups')

    def test_dry_run_does_not_change_instances(self):
        cloud = LocalCloud()
        load_task(9).auto_stop(cloud)
        self.assertEqual(cloud.calls, [])
        self.assertEqual(cloud.instances[0]['State']['Name'], 'running')

    def test_bucket_parameters_and_unexpected_error(self):
        from botocore.exceptions import ClientError
        cloud = LocalCloud()
        load_task(4).create_s3_bucket('test-us', 'us-east-1', cloud)
        self.assertNotIn('CreateBucketConfiguration', cloud.calls[0])
        with patch.object(cloud, 'create_bucket', side_effect=ClientError({'Error': {'Code': 'AccessDenied'}}, 'CreateBucket')):
            with self.assertRaises(ClientError):
                load_task(4).create_s3_bucket('blocked', 'eu-central-1', cloud)

    def test_cost_and_scaling_boundaries(self):
        history = load_task(16).simulate_scaling(lambda: 71, 6)
        self.assertEqual(history[-1]['instances'], 3)
        self.assertEqual(load_task(16).simulate_scaling(lambda: 20)[-1]['instances'], 1)
        self.assertTrue(all(x['action'] == 'hold' for x in load_task(16).simulate_scaling(lambda: 70)))
        cloud = LocalCloud()
        cloud.instances[0]['InstanceType'] = 'unknown'
        self.assertEqual(load_task(12).AWSCostCalculator().report(cloud, cloud.now)[0]['estimated_usd'], 'unknown type')

    def test_rollback_failure_and_private_default(self):
        result = load_task(13).deployment_pipeline(lambda cmd: 0, lambda: False)
        self.assertEqual(result['status'], 'rollback failed')
        with self.assertRaises(ValueError):
            load_task(14).deploy_website(ROOT, 'test', 'eu-central-1', LocalCloud())

    def test_restore_rejects_corruption(self):
        cloud = LocalCloud()
        cloud.put_object(Bucket='source', Key='broken.json', Body=json.dumps({'data': {'v': 2}, 'sha256': 'wrong'}))
        with self.assertRaises(ValueError):
            load_task(19).restore_from_backup('broken', cloud, 'source', [])

    def test_course_api_and_csrf(self):
        import app
        from django.test import Client
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.get('/').status_code, 200)
        course = client.get('/api/course')
        self.assertEqual(course.status_code, 200)
        lessons = course.json()['lessons']
        self.assertEqual(len(lessons), 20)
        for lesson in lessons:
            for source in lesson['steps']['sources'].values():
                for note in source['notes'].values():
                    self.assertLessEqual(note['end'], len(source['source'].splitlines()))
        self.assertEqual(client.post('/api/run/1', data='{}', content_type='application/json').status_code, 403)
        self.assertEqual(client.get('/api/code/21').status_code, 404)
        self.assertEqual(client.get('/api/code/1?file=../../app.py').status_code, 404)


if __name__ == '__main__':
    unittest.main()
