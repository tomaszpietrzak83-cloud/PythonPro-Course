from pathlib import Path

import yaml


ROOT = Path(__file__).parent


def demo(work):
    workflow = yaml.safe_load((ROOT / ".github/workflows/lesson.yml").read_text(encoding="utf-8"))
    import subprocess
    import sys
    from xml.etree import ElementTree
    
    report = work / "results.xml"
    subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                    str(ROOT / "tests"), f"--junitxml={report}"], check=True, capture_output=True)
    suite = ElementTree.parse(report).find(".//testsuite")
    assert suite.attrib["tests"] == "1" and suite.attrib["failures"] == "0"
    return {"artifact": report.name, "tests": 1, "failures": 0}
