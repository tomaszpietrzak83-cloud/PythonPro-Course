import shutil
from datetime import datetime
from pathlib import Path


def backup_directory(source, destination):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if destination == source or source in destination.parents:
        raise ValueError("Backup destination must be outside source")
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / datetime.now().strftime("backup_%Y%m%d_%H%M%S_%f")
    shutil.copytree(source, target)
    return target


def demo(work, cloud):
    source = work / "project"
    source.mkdir()
    (source / "settings.txt").write_text("version=1", encoding="utf-8")
    backup = backup_directory(source, work / "backups")
    assert (backup / "settings.txt").read_text() == "version=1"
    return {"success": True, "backup": str(backup)}
