from datetime import datetime, timedelta

from app.models import Booking, User, db
from sqlalchemy import asc, desc, extract, func


def reservation_per_department():

    bookings = (
        db.session
        .query(
            User.department,
            func.count(Booking.id).label("booking_count"),
        )
        .join(Booking)
        .filter(Booking.status != "cancelled")
        .group_by(User.department)
        .order_by(desc("booking_count"))
        .all()
    )
    return bookings


def reservation_per_day():

    bookings = (
        db.session
        .query(
            func.date(Booking.start_time).label("booking_date"),
            func.count(Booking.id).label("booking_count"),
        )
        .filter(
            Booking.status != "cancelled",
            Booking.start_time >= datetime.now() - timedelta(days=30),
        )
        .group_by(func.date(Booking.start_time))
        .order_by(asc("booking_date"))
    ).all()
    return bookings


def heat_map_of_bookings():

    bookings = (
        db.session
        .query(
            extract("dow", Booking.start_time).label("day_of_week"),
            extract("hour", Booking.start_time).label("hour_of_day"),
            func.count(Booking.id).label("booking_count"),
        )
        .filter(Booking.status != "cancelled")
        .group_by(
            extract("dow", Booking.start_time),
            extract("hour", Booking.start_time),
        )
        .order_by(asc("day_of_week"), asc("hour_of_day"))
    ).all()
    return bookings
