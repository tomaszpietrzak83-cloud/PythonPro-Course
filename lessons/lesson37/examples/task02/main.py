import os
import subprocess
import sys


def demo(work):
    values = [subprocess.check_output([sys.executable, __file__], text=True,
              env={**os.environ, "NAME": name}).strip() for name in ("Ada", "Linus")]
    assert values == ["Hello, Ada!", "Hello, Linus!"]
    return {"stdout": values}


if __name__ == "__main__":
    print(f"Hello, {os.getenv('NAME', 'Docker')}!")
