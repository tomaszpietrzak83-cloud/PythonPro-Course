"""Verify real HTTP/database behavior, teaching coverage and studio boundaries."""
import asyncio
import importlib
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT/'examples'))
import app
from curriculum import lesson
from django.test import Client
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer
from api_support import SESSION, database


class TeachingTests(unittest.TestCase):
    def test_quick_presentations_are_short_and_detailed_versions_unchanged(self):
        original=json.loads((ROOT/'material.json').read_text(encoding='utf-8'))
        for n in range(1,21):
            item=lesson(n)
            self.assertEqual(item['steps']['steps'],original[n-1]['steps']['steps'])
            detailed=item['steps']['steps']
            quick=item['steps'].get('quick')
            if len(detailed)<=20:
                self.assertIsNone(quick)
                continue
            self.assertTrue(quick)
            self.assertLessEqual(len(quick),20)
            lines=item['steps']['source'].splitlines()
            covered=set()
            for step in quick:
                self.assertGreaterEqual(step['start'],1)
                self.assertLessEqual(step['start'],step['end'])
                self.assertLessEqual(step['end'],len(lines))
                covered.update(range(step['start'],step['end']+1))
                for language in ('pl','en'):
                    self.assertLessEqual(len(step['body'][language].split()),90)
                    self.assertGreater(len(step['body'][language]),30)
            # Every function body remains represented in the compiled narrative.
            import ast
            tree=ast.parse(item['steps']['source'])
            for node in tree.body:
                if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
                    self.assertTrue(set(range(node.lineno,node.end_lineno+1))<=covered)
        self.assertEqual(len(lesson(14)['steps']['quick']),16)

    def test_every_source_line_has_matching_bilingual_explanation(self):
        for n in range(1,21):
            item=lesson(n)
            lines=item['steps']['source'].splitlines()
            expected={i for i,line in enumerate(lines,1) if line.strip()}
            actual={step['start'] for step in item['steps']['steps']}
            self.assertEqual(actual,expected)
            self.assertTrue(item['assignment']['pages']['pl'])
            self.assertTrue(item['assignment']['pages']['en'])
            for step in item['steps']['steps']:
                self.assertEqual(step['start'],step['end'])
                for language in ('pl','en'):
                    self.assertGreater(len(step['body'][language]),30)

    def test_studio_api_and_csrf(self):
        client=Client(enforce_csrf_checks=True)
        self.assertEqual(client.get('/').status_code,200)
        self.assertEqual(len(client.get('/api/course').json()['lessons']),20)
        self.assertEqual(client.post('/api/run/1','{}',content_type='application/json').status_code,403)
        token=client.cookies['csrftoken'].value
        for payload in ([], {'input':{'unknown':1}}, {'backend':'docker'}, {'input':True}):
            response=client.post('/api/run/1',json.dumps(payload),content_type='application/json',HTTP_X_CSRFTOKEN=token)
            self.assertEqual(response.status_code,400)
        for name in ('.env','../.env','../../lesson28/.env'):
            self.assertEqual(client.get('/api/code/1',{'file':name}).status_code,404)
        for name in ('api_support.py','lab_support.py','routes.py'):
            self.assertEqual(client.get('/api/code/19',{'file':name}).status_code,200)

    def test_all_local_programs_and_results(self):
        reports={}
        for n in range(1,21):
            if n in (12,13):
                continue
            with self.subTest(task=n):
                process=subprocess.run([sys.executable,str(ROOT/'examples'/f'task{n:02}.py')],
                                       capture_output=True,text=True,encoding='utf-8',timeout=30)
                self.assertEqual(process.returncode,0,process.stderr)
                events=[json.loads(line) for line in process.stdout.splitlines()]
                self.assertEqual(events[0]['kind'],'boot')
                self.assertEqual(events[-1]['kind'],'done')
                self.assertFalse(process.stderr)
                reports[n]=events
        def bodies(n):
            return [e['label'].split(': ',1)[1] for e in reports[n] if e['actor']=='response']
        self.assertEqual(json.loads(bodies(9)[0]),{'id':1,'name':'Notebook','price':1299})
        request6=next(e for e in reports[6] if e['actor']=='client')
        response6=next(e for e in reports[6] if e['actor']=='response')
        self.assertEqual(request6['request_body'],{'message':'Python'})
        self.assertEqual(request6['http_method'],'POST')
        self.assertEqual(response6['http_status'],200)
        self.assertEqual(json.loads(response6['response_body']),{'message':'Python'})
        self.assertEqual(request6['http_url'],response6['http_url'])
        self.assertEqual(json.loads(bodies(14)[-1])['price'],999)
        self.assertEqual(bodies(15)[-2:],[ '', 'Product not found'])
        balances=[json.loads(body) for body in bodies(16) if body.startswith('{"1"')]
        self.assertEqual(balances,[{'1':900,'2':600}]*2)
        self.assertEqual(json.loads(bodies(17)[3])[0]['name'],'Pen')
        self.assertEqual(json.loads(bodies(20)[0])['creator'],'Anna')
        self.assertIn('status',json.loads(bodies(18)[0]))
        self.assertIn('response',json.loads(bodies(18)[1]))
        for n in (1,18):
            metrics={e['label']:e['value'] for e in reports[n] if e['kind']=='metric'}
            self.assertGreaterEqual(metrics['Elapsed time'],3 if n==18 else 4)
            self.assertLess(metrics['Elapsed time'],6)

    @unittest.skipUnless(os.environ.get('LESSON32_LIVE_API')=='1','Opt-in public API integration')
    def test_public_api_clients(self):
        for n in (12,13):
            process=subprocess.run([sys.executable,str(ROOT/'examples'/f'task{n:02}.py')],capture_output=True,text=True,encoding='utf-8',timeout=30)
            self.assertEqual(process.returncode,0,process.stderr)


class DatabaseTests(unittest.IsolatedAsyncioTestCase):
    async def test_product_validation_and_patch_zero(self):
        module=importlib.import_module('task14')
        async with database(module.Base) as factory:
            application=web.Application(); application[SESSION]=factory
            application.router.add_post('/products',module.create_product)
            application.router.add_patch('/products/{id}',module.update_product)
            application.router.add_get('/products/{id}',module.get_product)
            async with TestClient(TestServer(application)) as client:
                for value in ([], {}, {'name':'x','price':True}, {'name':'','price':1}, {'name':'x','price':-1}, {'name':'x','price':1.5}, {'name':'x','price':2147483648}):
                    response=await client.post('/products',json=value)
                    self.assertEqual(response.status,400)
                response=await client.post('/products',data='{bad',headers={'Content-Type':'application/json'})
                self.assertEqual(response.status,400)
                response=await client.post('/products',json={'name':'Book','price':100})
                self.assertEqual(response.status,201)
                response=await client.patch('/products/1',json={'price':0})
                self.assertEqual(await response.json(),{'id':1,'name':'Book','price':0})
                self.assertEqual((await client.get('/products/nope')).status,400)
                self.assertEqual((await client.patch('/products/999',json={'price':5})).status,404)

    async def test_concurrent_transfers_and_rollback(self):
        module=importlib.import_module('task16')
        async with database(module.Base) as factory:
            async with factory.begin() as session:
                session.add_all([module.Account(id=1,balance=1000),module.Account(id=2,balance=500)])
            application=web.Application(); application[SESSION]=factory
            application.router.add_post('/transfer',module.transfer)
            application.router.add_get('/balances',module.balances)
            async with TestClient(TestServer(application)) as client:
                response=await client.post('/transfer',json={'from_id':1,'to_id':2,'amount':13})
                self.assertEqual(response.status,409)
                self.assertEqual(await (await client.get('/balances')).json(),{'1':1000,'2':500})
                responses=await asyncio.gather(*(client.post('/transfer',json={'from_id':1,'to_id':2,'amount':100}) for _ in range(12)))
                self.assertEqual(sorted(r.status for r in responses),[200]*10+[409]*2)
                self.assertEqual(await (await client.get('/balances')).json(),{'1':0,'2':1500})
                for payload,status in [({'from_id':1,'to_id':1,'amount':5},400),({'from_id':1,'to_id':2,'amount':True},400),({'from_id':1,'to_id':999,'amount':5},404)]:
                    self.assertEqual((await client.post('/transfer',json=payload)).status,status)


if __name__ == '__main__':
    unittest.main()
