"""Exercise real programs, API execution, reviewed source ranges and input boundaries."""
import json
import os
import subprocess
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import app
from curriculum import lesson
from django.test import Client


def execute(number, inputs=None):
    completed = subprocess.run(
        [sys.executable, '-u', str(ROOT / 'examples' / f'task{number:02}.py')],
        env=dict(os.environ, LESSON31_INPUT=json.dumps(inputs or {}),
                 PYTHONIOENCODING='utf-8'),
        capture_output=True, encoding='utf-8', timeout=35)
    if completed.returncode:
        raise AssertionError(completed.stderr or completed.stdout)
    if completed.stderr:
        raise AssertionError(completed.stderr)
    events = [json.loads(line) for line in completed.stdout.splitlines()]
    return events, {e['label']: e['value'] for e in events if e['kind'] == 'metric'}


class StudioTests(unittest.TestCase):
    def test_01_every_real_program(self):
        reports = {}
        for number in range(1, 21):
            with self.subTest(task=number):
                events, metrics = execute(number)
                self.assertEqual(events[0]['kind'], 'boot')
                self.assertEqual(events[-1]['kind'], 'done')
                self.assertIn('Elapsed time', metrics)
                self.assertFalse(any(e['kind'] == 'error' for e in events))
                reports[number] = metrics
                print(f'Task {number:02}: {metrics}', flush=True)
        self.assertEqual(reports[5]['5 ** 3'], 125)
        self.assertEqual(reports[6]['Temperature'], 25)
        self.assertEqual(reports[7]['Cities'], 3)
        self.assertEqual(reports[8]['Responses'], 5)
        self.assertEqual(reports[9]['HTTP statuses'], '[200, 404, 503]')
        self.assertEqual(reports[11]['Count'], 10)
        self.assertTrue(reports[12]['Cancelled tasks'] >= 1)
        self.assertTrue(reports[13]['Echo matches input'])
        self.assertTrue(reports[14]['Exactly 1..20'])
        self.assertEqual(reports[14]['Processed items'], 20)
        self.assertTrue(reports[15]['All records intact'])
        self.assertEqual(reports[16]['Granted requests'], 40)
        self.assertTrue(reports[16]['Rolling window respected'])
        self.assertEqual(reports[17]['Posts'], 3)
        self.assertTrue(reports[18]['Task cancelled'])
        self.assertEqual(reports[19]['Prime count'], 25)
        self.assertEqual(reports[19]['Largest prime'], 97)
        self.assertFalse(reports[20]['Timeout'])
        # Relational timing allows overhead while detecting sequential execution.
        self.assertGreater(reports[3]['Elapsed time'], reports[4]['Elapsed time'] + 0.5)
        (ROOT / '.runtime').mkdir(exist_ok=True)
        (ROOT / '.runtime' / 'verification.json').write_text(
            json.dumps(reports, indent=2), encoding='utf-8')

    def test_02_timeout_branch(self):
        events, metrics = execute(20, {'delay': 5})
        self.assertTrue(metrics['Timeout'])
        self.assertTrue(any(e['label'] == 'Cleanup complete' for e in events))
        self.assertFalse(any(e['label'] == 'Completed in time' for e in events))

    def test_03_source_and_bilingual_material(self):
        for number in range(1, 21):
            item = lesson(number)
            lines = item['steps']['source'].splitlines()
            self.assertTrue(item['assignment']['pages']['pl'])
            self.assertTrue(item['assignment']['pages']['en'])
            for step in item['steps']['steps']:
                self.assertTrue(step['body']['pl'])
                self.assertTrue(step['body']['en'])
                self.assertLessEqual(step['end'], len(lines))
                for detail in step['details']:
                    self.assertGreaterEqual(detail['start'], step['start'])
                    self.assertLessEqual(detail['end'], step['end'])
                    self.assertTrue(detail['body']['pl'])
                    self.assertTrue(detail['body']['en'])
                    fragment = '\n'.join(lines[detail['start']-1:detail['end']])
                    self.assertIn(detail['expression'], fragment)

    def test_04_api_validation_and_csrf(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.get('/').status_code, 200)
        token = client.cookies['csrftoken'].value
        self.assertEqual(client.post('/api/run/1', '{}', content_type='application/json').status_code, 403)
        self.assertEqual(client.get('/api/run/1').status_code, 405)
        self.assertEqual(client.get('/api/code/21').status_code, 404)
        for body in ([], {'input': {'delay': float('nan')}},
                     {'input': {'delay': True}}, {'input': {'delay': 100}},
                     {'backend': 'docker'}, {'input': {'unknown': 1}}):
            self.assertEqual(client.post('/api/run/20', json.dumps(body),
                content_type='application/json', HTTP_X_CSRFTOKEN=token).status_code, 400)
        self.assertEqual(app.validate(13, {'port': 8888}), {'port': 8888})
        self.assertEqual(app.validate(20, {'delay': 'random'}), {'delay': 'random'})
        course = client.get('/api/course').json()
        self.assertEqual(len(course['lessons']), 20)
        self.assertEqual(client.get('/api/course')['Cache-Control'], 'no-store')
        response = client.post('/api/run/1', '{}', content_type='application/json',
                               HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 202)
        key = response.json()['id']
        for _ in range(100):
            job = client.get(f'/api/status/{key}').json()
            if job['status'] != 'running':
                break
            time.sleep(0.05)
        self.assertEqual(job['status'], 'done')


if __name__ == '__main__':
    unittest.main(verbosity=2)
