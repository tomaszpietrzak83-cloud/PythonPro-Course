from pathlib import Path

import yaml


def demo(work):
    root = Path(__file__).parent
    base = yaml.safe_load((root / "docker-compose.yml").read_text())[
        "services"
    ]["backend"]
    dev = yaml.safe_load((root / "docker-compose.dev.yml").read_text())[
        "services"
    ]["backend"]
    prod = yaml.safe_load((root / "docker-compose.prod.yml").read_text())[
        "services"
    ]["backend"]
    assert "volumes" in dev and "--reload" in dev["command"]
    assert "volumes" not in base and "volumes" not in prod
    return {"dev": {**base, **dev}, "production": {**base, **prod}}
