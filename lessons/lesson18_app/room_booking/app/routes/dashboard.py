"""
Dashboard with statistics.
"""

from datetime import datetime, timedelta

from _03_new_statistics import (
    heat_map_of_bookings,
    reservation_per_day,
    reservation_per_department,
)
from flask import Blueprint, jsonify, render_template
from sqlalchemy import desc, func
from sqlalchemy.orm import joinedload

from app.models import Booking, Room, User, db, get_booking_statistics

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():
    """Dashboard homepage."""

    # General statistics
    stats = {
        "total_rooms": Room.query.filter_by(is_active=True).count(),
        "total_users": User.query.count(),
        "total_bookings": Booking.query.filter_by(status="confirmed").count(),
        "bookings_today": Booking.query.filter(
            func.date(Booking.start_time) == datetime.today().date(),
            Booking.status == "confirmed",
        ).count(),
    }

    # Upcoming bookings (next 24h)
    now = datetime.now()
    upcoming = (
        Booking.query
        .options(joinedload(Booking.room), joinedload(Booking.user))
        .filter(
            Booking.start_time >= now,
            Booking.start_time <= now + timedelta(hours=24),
            Booking.status == "confirmed",
        )
        .order_by(Booking.start_time)
        .limit(10)
        .all()
    )

    # Top users (most bookings)
    top_users = (
        db.session
        .query(User.name, func.count(Booking.id).label("booking_count"))
        .join(Booking)
        .filter(Booking.status != "cancelled")
        .group_by(User.id)
        .order_by(desc("booking_count"))
        .limit(5)
        .all()
    )

    # Room utilization (% of time booked in last month)
    month_ago = now - timedelta(days=30)

    room_utilization = []
    active_rooms = Room.query.filter_by(is_active=True).all()

    for room in active_rooms:
        # Sum of booking hours
        total_hours = (
            db.session
            .query(
                func.sum(
                    func.extract("epoch", Booking.end_time - Booking.start_time)
                    / 3600
                )
            )
            .filter(
                Booking.room_id == room.id,
                Booking.start_time >= month_ago,
                Booking.status != "cancelled",
            )
            .scalar()
            or 0
        )

        # Max 8h per day * 22 work days = 176h
        max_hours = 176
        utilization = (total_hours / max_hours) * 100

        room_utilization.append({
            "room": room.name,
            "hours": round(total_hours, 1),
            "utilization": round(utilization, 1),
        })

    # Sort by utilization
    room_utilization.sort(key=lambda x: x["utilization"], reverse=True)

    department_rows = reservation_per_department()
    department_labels = [row[0] for row in department_rows]
    department_values = [row[1] for row in department_rows]

    reservation_per_day_data = reservation_per_day()
    trend_labels = [row[0] for row in reservation_per_day_data]
    trend_values = [row[1] for row in reservation_per_day_data]

    heat_map_rows = heat_map_of_bookings()

    day_order = [
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (0, "Sunday"),
    ]

    counts = {}
    for day_of_week, hour_of_day, booking_count in heat_map_rows:
        counts[(int(day_of_week), int(hour_of_day))] = booking_count

    heatmap_rows = []
    for hour in range(24):
        row = {"hour": hour, "cells": []}

        for day_num, day_name in day_order:
            row["cells"].append(counts.get((day_num, hour), 0))

        heatmap_rows.append(row)

    return render_template(
        "dashboard.html",
        stats=stats,
        upcoming=upcoming,
        top_users=top_users,
        room_utilization=room_utilization,
        trend_labels=trend_labels,
        trend_values=trend_values,
        department_labels=department_labels,
        department_values=department_values,
        day_order=day_order,
        heatmap_rows=heatmap_rows,
    )


@dashboard_bp.route("/api/dashboard/stats")
def api_stats():
    """API endpoint for statistics (for JS charts)."""
    stats = get_booking_statistics()
    return jsonify(stats)
