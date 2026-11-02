import argparse
import json
import mimetypes
from pathlib import Path


def deploy_website(directory, bucket, region, s3, public=False):
    if not public:
        raise ValueError("Public website requires explicit public=True")
    params = {"Bucket": bucket}
    if region != "us-east-1":
        params["CreateBucketConfiguration"] = {"LocationConstraint": region}
    s3.create_bucket(**params)
    s3.put_bucket_website(
        Bucket=bucket,
        WebsiteConfiguration={"IndexDocument": {"Suffix": "index.html"}},
    )
    uploaded = []
    for path in sorted(Path(directory).rglob("*")):
        if path.is_file() and path.suffix.lower() in {".html", ".css", ".js"}:
            key = path.relative_to(directory).as_posix()
            s3.upload_file(
                str(path),
                bucket,
                key,
                ExtraArgs={
                    "ContentType": mimetypes.guess_type(path.name)[0]
                    or "application/octet-stream"
                },
            )
            uploaded.append(key)
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket}/*",
            }
        ],
    }
    s3.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy))
    # Account/bucket Block Public Access may reject this; do not disable it here.
    return {
        "url": f"http://{bucket}.s3-website.{region}.amazonaws.com",
        "files": uploaded,
    }


def demo(work, cloud):
    (work / "index.html").write_text("<h1>Training site</h1>")
    return deploy_website(
        work, "lesson35-website", "eu-central-1", cloud, public=True
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Local simulated S3 website deployment"
    )
    parser.add_argument("directory", type=Path)
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--region", default="eu-central-1")
    parser.add_argument("--public", action="store_true")
    args = parser.parse_args()
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from demo_support import LocalCloud

    print(
        deploy_website(
            args.directory, args.bucket, args.region, LocalCloud(), args.public
        )
    )
