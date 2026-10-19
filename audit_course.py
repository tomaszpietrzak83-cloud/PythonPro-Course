"""Read-only source checks and smoke tests in temporary lesson copies."""
import ast
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import socket
import time
import urllib.request
import urllib.error
import re

ROOT = Path(__file__).resolve().parent
FILES = [ROOT / p for p in subprocess.check_output(['rg', '--files', '-g', '*.py'], cwd=ROOT, text=True).splitlines()]
ENV = {**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUNBUFFERED': '1', 'DJANGO_SECRET_KEY': 'audit-only-local-key', 'POSTGRES_PASSWORD': 'audit-only', 'DATABASE_URL': 'sqlite:///:memory:'}
results = []

def command(label, args, cwd, timeout=35, stdin=""):
    try:
        r = subprocess.run([sys.executable, *args], cwd=cwd, env=ENV, input=stdin, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)
        return {'test': label, 'status': 'PASS' if r.returncode == 0 else 'FAIL', 'output': (r.stdout + r.stderr)[-12000:]}
    except subprocess.TimeoutExpired:
        return {'test': label, 'status': 'TIMEOUT'}

for p in FILES:
    try:
        ast.parse(p.read_text(encoding='utf-8-sig'), filename=str(p))
    except Exception as e:
        results.append({'test': str(p.relative_to(ROOT)), 'status': 'SYNTAX_ERROR', 'output': str(e)})
results.append({'test': 'syntax', 'status': 'PASS' if not results else 'FAIL', 'count': len(FILES)})
results.append(command('undefined names', ['-m', 'flake8', 'lessons', 'course_runtime.py', 'setup_course.py', '--exclude', '.venv', '--select', 'E9,F821,F822,F823'], ROOT))
manage_files = [p for p in FILES if p.name == 'manage.py']
with ThreadPoolExecutor(max_workers=4) as pool:
    jobs = [pool.submit(command, str(p.relative_to(ROOT)) + ' check', [str(p), 'check'], p.parent) for p in manage_files]
    for job in jobs:
        r = job.result(); results.append(r); print(r['test'], r['status'], flush=True)

ignore = shutil.ignore_patterns('.venv', '.env', '.env.*', '__pycache__', '*.sqlite3', '.runtime', 'media')
(ROOT / '.audit-temp').mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='course-audit-', dir=ROOT / '.audit-temp') as temp:
    temp = Path(temp)
    shutil.copy2(ROOT/'help_functions.py', temp/'help_functions.py')
    shutil.copy2(ROOT/'course_runtime.py', temp/'course_runtime.py')
    for lesson in (ROOT/'lessons').iterdir():
        if not lesson.is_dir(): continue
        shutil.copytree(lesson, temp/'lessons'/lesson.name, ignore=ignore)
    simple=[]
    for p in FILES:
        relative=p.relative_to(ROOT)
        if len(relative.parts)<3 or relative.parts[0]!='lessons': continue
        name=relative.parts[1]
        if name not in {f'lesson{i:02d}' for i in [*range(1,14),16]}: continue
        source=p.read_text(encoding='utf-8-sig')
        if p.name == 'run_before_checking_lesson.py':
            results.append({'test':str(relative), 'status':'SKIP', 'reason':'package installation'})
            continue
        if any(word in source for word in ('input(', 'input (', 'while True', 'requests.', 'webbrowser.', 'subprocess.', 'run_before_checking')):
            results.append({'test':str(relative), 'status':'SKIP', 'reason':'interactive or external action'})
            continue
        copy=temp.joinpath(*relative.parts)
        simple.append((relative,copy))
    simple.sort(key=lambda pair:str(pair[0]))
    # SQLite exercises share a database; run in lesson order.
    with ThreadPoolExecutor(max_workers=1) as pool:
        jobs=[pool.submit(command,str(rel),[str(p)],p.parent,8) for rel,p in simple]
        for job in jobs: results.append(job.result())
    for relative,module in [('lesson14','app'),('lesson17_app/registry','app'),('lesson17_app/app ex 01-09','app'),('lesson18_app/flask_masterclass','app'),('lesson18_app/room_booking','run')]:
        base=temp/'lessons'/relative
        code=f"import {module} as m; app=m.app; app.config['TESTING']=True; client=app.test_client(); rules=[r.rule for r in app.url_map.iter_rules() if not r.arguments and 'GET' in r.methods and r.endpoint!='static']; statuses=[(url,client.get(url).status_code) for url in rules]; print(statuses); assert all(status<500 for url,status in statuses)"
        r=command('Flask '+relative,['-c',code],base)
        results.append(r); print(r['test'],r['status'],flush=True)
    # Start each Django project against an isolated SQLite database.
    for original in manage_files:
        base=temp/original.relative_to(ROOT).parent
        source=(base/'manage.py').read_text(encoding='utf-8')
        settings=re.search(r'[\"\']([\w.]+\.settings)[\"\']',source).group(1)
        (base/'audit_settings.py').write_text(f"from {settings} import *\nDATABASES = {{'default': {{'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}}}\nALLOWED_HOSTS = ['localhost','127.0.0.1','testserver']\nCACHES = {{**globals().get('CACHES', {{}}), 'default': {{'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}}}\n",encoding='utf-8')
        # The shared Cache Lab lives beside the projects, outside discovery's
        # default directory. Include it explicitly while retaining project tests.
        labels = ['.', 'cache_demo'] if (base.parent / 'cache_demo').is_dir() else []
        r=command('Django tests '+str(original.relative_to(ROOT).parent),['manage.py','test',*labels,'--noinput','--settings','audit_settings'],base,90)
        results.append(r); print(r['test'],r['status'],flush=True)
    # CLI application imports, initialization and clean exit.
    for relative,exit_option in [('Raw SQL/app_raw_sql.py','7'),('SQL-Alchemy/app_orm.py','6'),('zadanie_08_raw_sql_klasy/app_raw_sql_class.py','7'),('zadanie_09_sqlalchemy_tagi/app_orm.py','7')]:
        script=temp/'lessons/lesson15_project_sql_app'/relative
        code="import sys,runpy; sys.path.insert(0,"+repr(str(temp))+"); import course_runtime; course_runtime.PYTHON=__import__('pathlib').Path(sys.executable); runpy.run_path("+repr(str(script))+",run_name='__main__')"
        r=command('CLI '+relative,['-c',code],script.parent,20,exit_option+'\n')
        results.append(r); print(r['test'],r['status'],flush=True)
    # Exercise programs with simple sample input; random/menu loops stay manual.
    for p in FILES:
        rel=p.relative_to(ROOT)
        if len(rel.parts)<3 or rel.parts[0]!='lessons' or rel.parts[1] not in {f'lesson{i:02d}' for i in range(1,9)}: continue
        source=p.read_text(encoding='utf-8-sig')
        if 'input(' not in source or 'while' in source: continue
        script=temp/rel
        r=command('sample input '+str(rel),[str(script)],script.parent,8,'2\n'*30)
        results.append(r)
report=ROOT/'audit-results.json'
report.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
from collections import Counter
print(dict(Counter(r['status'] for r in results)))
for r in results:
    if r['status'] not in ('PASS','SKIP'): print(r['test'],r.get('output','')[-3500:])
raise SystemExit(1 if any(r['status'] not in ('PASS', 'SKIP') for r in results) else 0)
