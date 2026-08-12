"""
Models for room booking system.
"""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, select

db = SQLAlchemy()

# MANY-TO-MANY: Rooms and Equipment
room_equipment = db.Table(
    "room_equipment",
    db.Column(
        "room_id", db.Integer, db.ForeignKey("rooms.id"), primary_key=True
    ),
    db.Column(
        "equipment_id",
        db.Integer,
        db.ForeignKey("equipment.id"),
        primary_key=True,
    ),
)


class User(db.Model):
    """User model for the system."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 1:N relationship with bookings
    bookings = db.relationship("Booking", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.email}>"

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "department": self.department,
            "is_admin": self.is_admin,
        }


class Equipment(db.Model):
    """Equipment model (projector, whiteboard, video conference, etc.)."""

    __tablename__ = "equipment"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    icon = db.Column(db.String(50))  # e.g. "projector", "whiteboard"

    def __repr__(self):
        return f"<Equipment {self.name}>"


class Room(db.Model):
    """Conference room model."""

    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    hourly_rate = db.Column(db.Numeric(10, 2), default=0)  # Cost per hour

    # 1:N relationship with bookings
    bookings = db.relationship(
        "Booking", backref="room", lazy="dynamic", cascade="all, delete-orphan"
    )

    # M:N relationship with equipment
    equipment = db.relationship(
        "Equipment",
        secondary=room_equipment,
        lazy="subquery",
        backref=db.backref("rooms", lazy=True),
    )

    def __repr__(self):
        return f"<Room {self.name} (cap: {self.capacity})>"

    def to_dict(self, include_equipment=True):
        data = {
            "id": self.id,
            "name": self.name,
            "capacity": self.capacity,
            "floor": self.floor,
            "description": self.description,
            "is_active": self.is_active,
            "hourly_rate": float(self.hourly_rate) if self.hourly_rate else 0,
        }
        if include_equipment:
            data["equipment"] = [e.name for e in self.equipment]
        return data

    def is_available(self, start_time, end_time, exclude_booking_id=None):
        """
        Check if room is available in the given time range.

        Args:
            start_time: Reservation start (datetime)
            end_time: Reservation end (datetime)
            exclude_booking_id: Booking ID to exclude (for editing)

        Returns:
            bool: True if room is available
        """
        query = Booking.query.filter(
            Booking.room_id == self.id,
            Booking.status != "cancelled",
            # Check time range overlap
            Booking.start_time < end_time,
            Booking.end_time > start_time,
        )

        if exclude_booking_id:
            query = query.filter(Booking.id != exclude_booking_id)

        return query.count() == 0


class Booking(db.Model):
    """Booking model."""

    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    status = db.Column(
        db.String(20), default="confirmed", nullable=False
    )  # confirmed, cancelled, completed

    attendees_count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    recurrence_rule = db.Column(db.String(20), nullable=True)
    series_id = db.Column(db.String(36), nullable=True)

    # Index for fast searching
    __table_args__ = (
        db.Index("idx_booking_room_time", "room_id", "start_time", "end_time"),
    )

    def __repr__(self):
        return f"<Booking {self.title} ({self.start_time})>"

    @property
    def duration_hours(self):
        """Booking duration in hours."""
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 3600

    @property
    def total_cost(self):
        """Total booking cost."""
        if self.room and self.room.hourly_rate:
            return float(self.room.hourly_rate) * self.duration_hours
        return 0

    def to_dict(self, include_room=False, include_user=False):
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "status": self.status,
            "attendees_count": self.attendees_count,
            "duration_hours": round(self.duration_hours, 2),
            "total_cost": round(self.total_cost, 2),
            "recurrence_rule": self.recurrence_rule,
            "series_id": self.series_id,
        }
        if include_room:
            data["room"] = self.room.to_dict(include_equipment=False)
        if include_user:
            data["user"] = self.user.to_dict()
        return data


# --- Task 04: Notifications ---
class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    booking_id = db.Column(
        db.Integer, db.ForeignKey("bookings.id"), nullable=True
    )
    notification_type = db.Column(
        db.String(50)
    )  # e.g. "booking_reminder", "booking_update"

    user = db.relationship("User", backref="notifications")
    booking = db.relationship("Booking", backref="notifications")


# --- HELPER FUNCTIONS ---


def find_available_rooms(
    start_time, end_time, min_capacity=1, required_equipment=None
):
    """
    Find available rooms matching criteria.

    Args:
        start_time: Start time (datetime)
        end_time: End time (datetime)
        min_capacity: Minimum capacity
        required_equipment: List of required equipment names

    Returns:
        List of available rooms
    """
    from sqlalchemy.orm import joinedload

    # Base query with eager loading
    query = Room.query.options(joinedload(Room.equipment)).filter(
        Room.is_active == True, Room.capacity >= min_capacity
    )

    # Filter by equipment
    if required_equipment:
        for eq_name in required_equipment:
            query = query.filter(Room.equipment.any(Equipment.name == eq_name))

    # Get candidate rooms
    candidate_rooms = query.all()

    # Check availability for each room
    available = []
    for room in candidate_rooms:
        if room.is_available(start_time, end_time):
            available.append(room)

    return available


def get_booking_statistics(start_date=None, end_date=None):
    """
    Get booking statistics.

    Returns:
        dict: Statistics dictionary
    """
    from sqlalchemy import func, extract

    base_query = db.session.query(Booking).filter(Booking.status != "cancelled")

    if start_date:
        base_query = base_query.filter(Booking.start_time >= start_date)
    if end_date:
        base_query = base_query.filter(Booking.end_time <= end_date)

    # General statistics
    total_bookings = base_query.count()

    # Statistics per room
    room_stats = (
        db.session
        .query(
            Room.name,
            func.count(Booking.id).label("booking_count"),
            func.sum(
                extract("epoch", Booking.end_time - Booking.start_time) / 3600
            ).label("total_hours"),
        )
        .join(Booking)
        .filter(Booking.status != "cancelled")
        .group_by(Room.name)
        .all()
    )

    # Statistics per weekday
    weekday_stats = (
        db.session
        .query(
            extract("dow", Booking.start_time).label("weekday"),
            func.count(Booking.id).label("count"),
        )
        .filter(Booking.status != "cancelled")
        .group_by("weekday")
        .order_by("weekday")
        .all()
    )

    weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    return {
        "total_bookings": total_bookings,
        "room_stats": [
            {
                "room": r.name,
                "bookings": r.booking_count,
                "hours": round(float(r.total_hours or 0), 1),
            }
            for r in room_stats
        ],
        "weekday_stats": [
            {"day": weekdays[int(w.weekday)], "count": w.count}
            for w in weekday_stats
        ],
    }


# --- Task 04: Notifications ---
@event.listens_for(Booking, "after_insert")
def booking_after_insert(mapper, connection, target):
    admin_id = connection.execute(
        select(User.id).where(User.is_admin == True)
    ).scalar()

    if admin_id is None:
        return

    connection.execute(
        Notification.__table__.insert().values(
            user_id=admin_id,
            message=f"New booking created: {target.title}",
            is_read=False,
            booking_id=target.id,
            notification_type="booking_created",
            created_at=datetime.now(),
        )
    )
