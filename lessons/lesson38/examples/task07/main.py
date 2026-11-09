from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    import ast
    files = sorted((ROOT / "src").glob("*.py"))
    for source in files:
        ast.parse(source.read_text(encoding="utf-8"))
    assert files
    return {"syntax_checked": [file.name for file in files], "ci_linter": "flake8 src/"}
