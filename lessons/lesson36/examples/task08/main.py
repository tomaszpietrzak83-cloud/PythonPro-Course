def create_replica(rds, primary, replica):
    rds.create_db_instance_read_replica(
        SourceDBInstanceIdentifier=primary, DBInstanceIdentifier=replica,
        DBInstanceClass="db.t3.micro", PubliclyAccessible=False,
    )
    rds.get_waiter("db_instance_available").wait(DBInstanceIdentifier=replica)
    instance = rds.describe_db_instances(DBInstanceIdentifier=replica)["DBInstances"][0]
    return instance["Endpoint"]["Address"]


class LocalReplica:
    def create_db_instance_read_replica(self, **kwargs):
        self.parameters = kwargs
        self.ready = False

    def get_waiter(self, name):
        assert name == "db_instance_available"
        return self

    def wait(self, **kwargs):
        self.ready = True

    def describe_db_instances(self, **kwargs):
        assert self.ready
        return {"DBInstances": [{"Endpoint": {"Address": "reader.internal.example"}}]}


def demo(work):
    rds = LocalReplica()
    endpoint = create_replica(rds, "writer", "reader")
    assert rds.ready
    return {"parameters": rds.parameters, "endpoint": endpoint}
