import json
import sys
from pathlib import Path


def report(source, output):
    dependencies = json.loads(source.read_text(encoding="utf-8"))["dependencies"]
    findings = [f"- {item['name']}: {vuln['id']}" for item in dependencies
                for vuln in item.get("vulns", [])]
    if findings:
        output.write_text("# Dependency findings\n\n" + "\n".join(findings) + "\n", encoding="utf-8")
    elif output.exists():
        output.unlink()


if __name__ == "__main__":
    report(Path(sys.argv[1]), Path(sys.argv[2]))
