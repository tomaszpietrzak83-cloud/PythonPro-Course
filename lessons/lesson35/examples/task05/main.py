from pathlib import Path


def upload_jpg(directory, bucket, s3):
    uploaded = []
    for path in sorted(Path(directory).iterdir()):
        if path.is_file() and path.suffix.lower() == ".jpg":
            s3.upload_file(str(path), bucket, path.name)
            uploaded.append(path.name)
    return uploaded


def demo(work, cloud):
    from PIL import Image

    Image.new("RGB", (32, 32), "teal").save(work / "photo.jpg")
    (work / "notes.txt").write_text("skip me")
    return {"uploaded": upload_jpg(work, "source", cloud)}
