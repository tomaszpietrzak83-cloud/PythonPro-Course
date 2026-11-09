import subprocess
import sys


def demo(work):
    output = subprocess.check_output([sys.executable, __file__], text=True).strip()
    assert output == "Hello, Docker!"
    return {"stdout": output}


if __name__ == "__main__":
    print("Hello, Docker!")
