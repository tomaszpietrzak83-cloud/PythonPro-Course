from botocore.exceptions import ClientError


def create_s3_bucket(bucket_name, region, client=None):
    if client is None:
        import boto3

        client = boto3.client("s3", region_name=region)
    params = {"Bucket": bucket_name}
    if region != "us-east-1":
        params["CreateBucketConfiguration"] = {"LocationConstraint": region}
    try:
        client.create_bucket(**params)
        return "created"
    except ClientError as error:
        if error.response["Error"]["Code"] in {
            "BucketAlreadyExists",
            "BucketAlreadyOwnedByYou",
        }:
            return "already exists"
        raise


def demo(work, cloud):
    first = create_s3_bucket("lesson35-demo", "eu-central-1", cloud)
    second = create_s3_bucket("lesson35-demo", "eu-central-1", cloud)
    return {"first": first, "second": second}
