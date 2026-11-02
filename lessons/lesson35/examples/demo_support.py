"""Explicit in-memory AWS teaching adapter. Never creates a boto3 session."""
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
from pathlib import Path
import copy
import hashlib
import threading

from botocore.exceptions import ClientError


@contextmanager
def health_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(503 if self.path == '/unavailable' else 200)
            self.end_headers()
            self.wfile.write(b'local training service')

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}'
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


class LocalCloud:
    """Small test double, not a complete AWS emulator; pages deliberately hold one item."""
    def __init__(self):
        self.now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.objects = {'source': {}, 'recovery-eu-west-1': {}}
        self.calls = []
        self.instances = [
            {'InstanceId': 'i-demo-dev', 'InstanceType': 't3.micro', 'State': {'Name': 'running'},
             'PublicIpAddress': '192.0.2.10', 'LaunchTime': self.now-timedelta(hours=24),
             'Tags': [{'Key': 'AutoStop', 'Value': 'true'}]},
            {'InstanceId': 'i-demo-prod', 'InstanceType': 't3.small', 'State': {'Name': 'running'},
             'LaunchTime': self.now-timedelta(hours=10), 'Tags': [{'Key': 'AutoStop', 'Value': 'false'}]},
            {'InstanceId': 'i-demo-stopped', 'InstanceType': 't3.micro', 'State': {'Name': 'stopped'},
             'LaunchTime': self.now-timedelta(hours=48), 'Tags': []},
        ]

    def describe_regions(self, **kwargs):
        return {'Regions': [{'RegionName': r, 'Endpoint': f'ec2.{r}.amazonaws.com'}
                            for r in ['eu-central-1', 'eu-west-1', 'us-east-1']]}

    def create_bucket(self, Bucket, **kwargs):
        if Bucket in self.objects:
            raise ClientError({'Error': {'Code': 'BucketAlreadyOwnedByYou', 'Message': 'test fixture'}}, 'CreateBucket')
        self.objects[Bucket] = {}
        self.calls.append({'operation': 'create_bucket', 'Bucket': Bucket, **kwargs})
        return {}

    def get_paginator(self, operation):
        cloud = self
        class Paginator:
            def paginate(self, **kwargs):
                if operation == 'describe_instances':
                    for item in copy.deepcopy(cloud.instances):
                        yield {'Reservations': [{'Instances': [item]}]}
                elif operation == 'list_objects_v2':
                    bucket = cloud.objects[kwargs['Bucket']]
                    rows = [{'Key': k, 'LastModified': v['LastModified'], 'ETag': v['ETag']}
                            for k, v in list(bucket.items()) if k.startswith(kwargs.get('Prefix', ''))]
                    for row in rows:
                        yield {'Contents': [row]}
                else:
                    raise ValueError('Unsupported test operation: '+operation)
        return Paginator()

    def put_object(self, Bucket, Key, Body, **kwargs):
        data = Body.encode() if isinstance(Body, str) else Body
        self.objects[Bucket][Key] = dict(Body=data, LastModified=self.now,
                                         ETag=hashlib.sha256(data).hexdigest(), **kwargs)
        return {}

    def get_object(self, Bucket, Key):
        return {'Body': BytesIO(self.objects[Bucket][Key]['Body'])}

    def upload_file(self, Filename, Bucket, Key, ExtraArgs=None):
        self.put_object(Bucket=Bucket, Key=Key, Body=Path(Filename).read_bytes(), **(ExtraArgs or {}))

    def copy_object(self, Bucket, Key, CopySource):
        data = self.objects[CopySource['Bucket']][CopySource['Key']]
        self.put_object(Bucket=Bucket, Key=Key, Body=data['Body'])

    def delete_object(self, Bucket, Key):
        del self.objects[Bucket][Key]

    def stop_instances(self, InstanceIds):
        for instance in self.instances:
            if instance['InstanceId'] in InstanceIds:
                instance['State']['Name'] = 'stopping'
        self.calls.append({'operation': 'stop_instances', 'ids': InstanceIds})
        return {}

    def put_bucket_website(self, **params):
        self.calls.append({'operation': 'put_bucket_website', **params})

    def put_bucket_policy(self, **params):
        self.calls.append({'operation': 'put_bucket_policy', **params})
