from io import BytesIO

from PIL import Image


def process_images(s3, bucket, seen):
    processed = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            token = (key, obj["ETag"])
            if (
                key.startswith("thumbnails/")
                or not key.lower().endswith((".jpg", ".png"))
                or token in seen
            ):
                continue
            body = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
            with Image.open(BytesIO(body)) as image:
                image.thumbnail((128, 128))
                output = BytesIO()
                image.convert("RGB").save(output, "JPEG")
            target = "thumbnails/" + key.rsplit(".", 1)[0] + ".jpg"
            s3.put_object(
                Bucket=bucket,
                Key=target,
                Body=output.getvalue(),
                ContentType="image/jpeg",
            )
            seen.add(token)
            processed.append(target)
    return processed


def demo(work, cloud):
    source = BytesIO()
    Image.new("RGB", (640, 320), "teal").save(source, "PNG")
    cloud.put_object(Bucket="source", Key="photo.png", Body=source.getvalue())
    seen = set()
    first = process_images(cloud, "source", seen)
    second = process_images(cloud, "source", seen)
    data = cloud.get_object(Bucket="source", Key=first[0])["Body"].read()
    (work / "thumbnail.jpg").write_bytes(data)
    with Image.open(BytesIO(data)) as image:
        size = image.size
    return {"first": first, "second": second, "thumbnail_size": size}
