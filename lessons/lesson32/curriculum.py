"""Serve source and line explanations from one checked snapshot."""
import json
from pathlib import Path

from assignments import assignment
from quick_notes import quick_steps

ROOT = Path(__file__).resolve().parent


def lesson(number):
    if not 1 <= number <= 20:
        raise ValueError('Unknown task')
    record = json.loads((ROOT/'material.json').read_text(encoding='utf-8'))[number-1]
    source = (ROOT/'examples'/f'task{number:02}.py').read_text(encoding='utf-8')
    if source != record['steps']['source']:
        raise ValueError('Source changed: run create_material.py to review line explanations')
    if len(record['steps']['steps']) > 20:
        record['steps']['quick'] = quick_steps(record)
    record['assignment'] = assignment(number, record.pop('adaptation'))
    return record
