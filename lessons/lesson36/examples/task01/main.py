def create_database(rds, identifier, subnet_group, security_group):
    """Create PostgreSQL and wait before taking the manual snapshot."""
    rds.create_db_instance(
        DBInstanceIdentifier=identifier, Engine="postgres",
        DBInstanceClass="db.t3.micro", AllocatedStorage=20,
        MasterUsername="appadmin", ManageMasterUserPassword=True,
        BackupRetentionPeriod=3, PubliclyAccessible=False,
        DBSubnetGroupName=subnet_group, VpcSecurityGroupIds=[security_group],
    )
    rds.get_waiter("db_instance_available").wait(DBInstanceIdentifier=identifier)
    return rds.create_db_snapshot(
        DBInstanceIdentifier=identifier, DBSnapshotIdentifier=f"{identifier}-initial"
    )


class LocalRDS:
    def __init__(self):
        self.calls = []
        self.available = False

    def create_db_instance(self, **parameters):
        self.calls.append({"operation": "create_db_instance", **parameters})

    def get_waiter(self, name):
        assert name == "db_instance_available"
        return self

    def wait(self, **parameters):
        self.available = True
        self.calls.append({"operation": "wait_available", **parameters})

    def create_db_snapshot(self, **parameters):
        assert self.available
        self.calls.append({"operation": "create_db_snapshot", **parameters})
        return {"DBSnapshot": parameters}


def demo(work):
    rds = LocalRDS()
    snapshot = create_database(rds, "lesson-db", "private", "sg-demo")
    assert len(rds.calls) == 3 and rds.calls[0]["BackupRetentionPeriod"] == 3
    return {"mode": "simulated RDS", "calls": rds.calls, "snapshot": snapshot}
