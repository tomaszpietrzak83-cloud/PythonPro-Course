from shutil import make_archive
from zipfile import ZipFile


def package_and_upload(source, output, s3, bucket):
    archive = make_archive(str(output), "zip", root_dir=source)
    key = "releases/app.zip"
    s3.upload_file(archive, bucket, key)
    return f"s3://{bucket}/{key}"


class RecordingS3:
    def upload_file(self, filename, bucket, key):
        with ZipFile(filename) as archive:
            self.members = archive.namelist()


def demo(work):
    source = work / "app"
    source.mkdir()
    (source / "app.txt").write_text("version=1", encoding="utf-8")
    s3 = RecordingS3()
    uri = package_and_upload(source, work / "app", s3, "lesson-releases")
    assert s3.members == ["app.txt"]
    return {"uri": uri, "archive_entries": s3.members}
