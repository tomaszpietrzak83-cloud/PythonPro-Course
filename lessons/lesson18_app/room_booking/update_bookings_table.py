from app.models import db
from run import app
from sqlalchemy import text

with app.app_context():
    db.session.execute(
        text(
            """
            ALTER TABLE bookings
            ADD COLUMN IF NOT EXISTS recurrence_rule VARCHAR(20);
            """
        )
    )

    db.session.execute(
        text(
            """
            ALTER TABLE bookings
            ADD COLUMN IF NOT EXISTS series_id VARCHAR(36);
            """
        )
    )

    db.session.commit()

print("Bookings table updated.")
