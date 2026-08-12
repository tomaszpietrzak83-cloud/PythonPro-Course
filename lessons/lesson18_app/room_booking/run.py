"""
Main application runner with seeding.
"""

import random
from datetime import datetime, timedelta

from app import create_app
from app.models import Booking, Equipment, Room, User, db

app = create_app()


def seed_database():
    """Populate database with sample data."""
    with app.app_context():
        # Check if data already exists
        if User.query.first():
            print("Database already contains data. Skipping seeding.")
            return

        print("Creating sample data...")

        # Equipment
        equipment_list = [
            Equipment(name="Projector", icon="projector"),
            Equipment(name="Whiteboard", icon="chalkboard"),
            Equipment(name="Video Conference", icon="video"),
            Equipment(name="Air Conditioning", icon="snowflake"),
            Equipment(name="Sound System", icon="volume-up"),
        ]
        db.session.add_all(equipment_list)

        # Rooms
        rooms = [
            Room(
                name="Room A1",
                capacity=10,
                floor=1,
                description="Small team meeting room",
                hourly_rate=50,
            ),
            Room(
                name="Room B2",
                capacity=20,
                floor=2,
                description="Medium room with projector",
                hourly_rate=80,
            ),
            Room(
                name="Conference Room",
                capacity=50,
                floor=3,
                description="Large room for presentations",
                hourly_rate=150,
            ),
            Room(
                name="Creative Space",
                capacity=8,
                floor=1,
                description="Brainstorming room with whiteboards",
                hourly_rate=60,
            ),
        ]

        # Assign equipment
        rooms[0].equipment = [
            equipment_list[1],
            equipment_list[3],
        ]  # Whiteboard, AC
        rooms[1].equipment = [
            equipment_list[0],
            equipment_list[2],
            equipment_list[3],
        ]  # Projector, Video, AC
        rooms[2].equipment = equipment_list  # All
        rooms[3].equipment = [equipment_list[1]]  # Only whiteboard

        db.session.add_all(rooms)

        # Users
        users = [
            User(name="John Smith", email="john@company.com", department="IT"),
            User(
                name="Anna Johnson", email="anna@company.com", department="HR"
            ),
            User(
                name="Peter Wilson",
                email="peter@company.com",
                department="Marketing",
            ),
            User(
                name="Mary Davis",
                email="mary@company.com",
                department="IT",
                is_admin=True,
            ),
        ]
        db.session.add_all(users)
        db.session.commit()

        # Sample bookings
        titles = [
            "Team meeting",
            "Code review",
            "Project presentation",
            "Job interview",
            "Training",
            "Sprint planning",
            "Retrospective",
            "Client demo",
        ]

        now = datetime.now().replace(minute=0, second=0, microsecond=0)

        for i in range(20):
            room = random.choice(rooms)
            user = random.choice(users)

            # Random date in next 14 days
            days_offset = random.randint(0, 14)
            hour = random.randint(9, 16)
            duration = random.choice([1, 2, 3])

            start = now + timedelta(days=days_offset, hours=hour - now.hour)
            end = start + timedelta(hours=duration)

            # Check availability
            if room.is_available(start, end):
                booking = Booking(
                    room=room,
                    user=user,
                    title=random.choice(titles),
                    start_time=start,
                    end_time=end,
                    attendees_count=random.randint(2, room.capacity),
                )
                db.session.add(booking)

        db.session.commit()
        print("Database populated with sample data!")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_database()

    app.run(debug=True, port=5000)
