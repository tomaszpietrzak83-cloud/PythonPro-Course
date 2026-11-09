import sys
from pathlib import Path
from xml.etree import ElementTree


def badge(report, output):
    rate = float(ElementTree.parse(report).getroot().attrib["line-rate"])
    label = f"coverage {rate:.0%}"
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="145" height="24">'
           '<rect width="145" height="24" rx="4" fill="#267451"/>'
           f'<text x="9" y="17" fill="white" font-family="sans-serif">{label}</text></svg>')
    output.write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    badge(Path(sys.argv[1]), Path(sys.argv[2]))
