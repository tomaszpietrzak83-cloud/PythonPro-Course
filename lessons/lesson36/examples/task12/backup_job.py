import argparse
import logging
from datetime import datetime, timezone

from main import rotate


def main():
    parser = argparse.ArgumentParser(description="Create and rotate scheduled RDS snapshots.")
    parser.add_argument("database", help="RDS DB instance identifier")
    parser.add_argument("--region", required=True)
    parser.add_argument("--sender", required=True, help="Verified SES sender address")
    parser.add_argument("--recipient", required=True)
    args = parser.parse_args()

    import boto3

    logging.basicConfig(level=logging.INFO)
    session = boto3.Session(region_name=args.region)
    ses = session.client("ses")

    def notify(message):
        logging.info("%s", message)
        ses.send_email(
            Source=args.sender,
            Destination={"ToAddresses": [args.recipient]},
            Message={
                "Subject": {"Data": "RDS snapshot rotation"},
                "Body": {"Text": {"Data": message}},
            },
        )

    rotate(session.client("rds"), args.database, datetime.now(timezone.utc), notify)


if __name__ == "__main__":
    main()
