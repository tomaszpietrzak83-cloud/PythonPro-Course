"""
API endpoints for bookings.
"""

import uuid
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request

from app.models import Booking, Room, User, db

bookings_bp = Blueprint("bookings", __name__, url_prefix="/api/bookings")


@bookings_bp.route("/", methods=["GET"])
def get_bookings():
    """
    Get list of bookings with filters.

    Query params:
        room_id: Filter by room
        user_id: Filter by user
        date: Filter by date (YYYY-MM-DD)
        status: Filter by status
    """
    from sqlalchemy.orm import joinedload

    query = Booking.query.options(
        joinedload(Booking.room), joinedload(Booking.user)
    )

    # Filters
    if room_id := request.args.get("room_id"):
        query = query.filter(Booking.room_id == room_id)

    if user_id := request.args.get("user_id"):
        query = query.filter(Booking.user_id == user_id)

    if date_str := request.args.get("date"):
        date = datetime.strptime(date_str, "%Y-%m-%d")
        query = query.filter(db.func.date(Booking.start_time) == date.date())

    if status := request.args.get("status"):
        query = query.filter(Booking.status == status)

    # Sort
    query = query.order_by(Booking.start_time.desc())

    # Pagination
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    pagination = query.paginate(page=page, per_page=per_page)

    return jsonify({
        "bookings": [
            b.to_dict(include_room=True, include_user=True)
            for b in pagination.items
        ],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page,
    })


@bookings_bp.route("/series/<series_id>/cancel", methods=["POST"])
def cancel_series(series_id):
    bookings = Booking.query.filter_by(series_id=series_id).all()

    if not bookings:
        return jsonify({"error": "Series not found"}), 404

    cancelled_count = 0

    for booking in bookings:
        if (
            booking.status != "cancelled"
            and booking.start_time > datetime.now()
        ):
            booking.status = "cancelled"
            cancelled_count += 1

    try:
        db.session.commit()
        return jsonify({
            "message": f"Cancelled {cancelled_count} bookings in series"
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@bookings_bp.route("/<int:id>/cancel", methods=["POST"])
def cancel_single_occurrence(id):
    booking = Booking.query.get(id)

    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    if booking.status == "cancelled":
        return jsonify({"error": "Booking is already cancelled"}), 400

    if booking.start_time <= datetime.now():
        return jsonify({"error": "Past bookings cannot be cancelled"}), 400

    booking.status = "cancelled"

    try:
        db.session.commit()
        return jsonify({
            "message": "Booking cancelled",
            "booking_id": booking.id,
            "series_id": booking.series_id,
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@bookings_bp.route("/", methods=["POST"])
def create_booking():
    """
    Create a new booking.

    Body JSON:
        room_id: int
        user_id: int
        title: str
        start_time: str (ISO format)
        end_time: str (ISO format)
        description: str (optional)
        attendees_count: int (optional)
    """
    data = request.get_json()

    # Validate required fields
    required = ["room_id", "user_id", "title", "start_time", "end_time"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        start_time = datetime.fromisoformat(data["start_time"])
        end_time = datetime.fromisoformat(data["end_time"])
    except ValueError:
        return jsonify({"error": "Invalid date format. Use ISO format."}), 400

    # Logic validation
    if start_time >= end_time:
        return jsonify({"error": "Start time must be before end time"}), 400

    if start_time < datetime.now():
        return jsonify({"error": "Cannot book in the past"}), 400

    # Check if room exists
    room = Room.query.get(data["room_id"])
    if not room:
        return jsonify({"error": "Room not found"}), 404

    if not room.is_active:
        return jsonify({"error": "Room is inactive"}), 400

    # Check if user exists
    user = User.query.get(data["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check room availability
    if not room.is_available(start_time, end_time):
        return jsonify({
            "error": "Room is already booked at this time",
            "conflicts": get_conflicts(room.id, start_time, end_time),
        }), 409

    # Check capacity
    attendees = data.get("attendees_count", 1)
    if attendees > room.capacity:
        return jsonify({
            "error": f"Too many attendees. Room capacity: {room.capacity}"
        }), 400

    # Create booking
    try:
        recurrence_rule = data.get("recurrence_rule")

        raw_occurrences = data.get("occurrences", 0)

        try:
            occurrences = int(raw_occurrences)
        except (TypeError, ValueError):
            return jsonify({"error": "occurrences must be an integer"}), 400

        if recurrence_rule and not occurrences:
            return jsonify({
                "error": "Recurring bookings require occurrences"
            }), 400

        if recurrence_rule and occurrences < 2:
            return jsonify({
                "error": "Recurring bookings require occurrences >= 2"
            }), 400

        if recurrence_rule not in (None, "WEEKLY", "BIWEEKLY"):
            return jsonify({"error": "Invalid recurrence_rule"}), 400

        if recurrence_rule == "WEEKLY":
            step_days = 7
        elif recurrence_rule == "BIWEEKLY":
            step_days = 14
        else:
            step_days = 0

        if recurrence_rule and occurrences:
            is_recurring = True
        else:
            is_recurring = False

        if is_recurring:
            series_id = str(uuid.uuid4())

            duration = end_time - start_time
            recurring_slots = []

            for i in range(occurrences):
                occurrence_start = start_time + timedelta(days=step_days * i)
                occurrence_end = occurrence_start + duration

                recurring_slots.append({
                    "start_time": occurrence_start,
                    "end_time": occurrence_end,
                })

            for slot in recurring_slots:
                if not room.is_available(slot["start_time"], slot["end_time"]):
                    return jsonify({
                        "error": "Room is already booked at this time",
                        "conflicts": get_conflicts(
                            room.id, slot["start_time"], slot["end_time"]
                        ),
                    }), 409

            new_bookings = []

            for slot in recurring_slots:
                booking = Booking(
                    room_id=room.id,
                    user_id=user.id,
                    title=data["title"],
                    description=data.get("description"),
                    start_time=slot["start_time"],
                    end_time=slot["end_time"],
                    attendees_count=attendees,
                    recurrence_rule=recurrence_rule,
                    series_id=series_id,
                )
                new_bookings.append(booking)

            db.session.add_all(new_bookings)
            db.session.commit()

            return jsonify({
                "message": "Recurring bookings created",
                "series_id": series_id,
                "bookings": [
                    booking.to_dict(include_room=True)
                    for booking in new_bookings
                ],
            }), 201

        else:
            series_id = None

            booking = Booking(
                room_id=room.id,
                user_id=user.id,
                title=data["title"],
                description=data.get("description"),
                start_time=start_time,
                end_time=end_time,
                attendees_count=attendees,
                recurrence_rule=recurrence_rule,
                series_id=series_id,
            )

            db.session.add(booking)
            db.session.commit()

            return jsonify({
                "message": "Booking created",
                "booking": booking.to_dict(include_room=True),
            }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error creating booking: {str(e)}"}), 500


@bookings_bp.route("/<int:booking_id>", methods=["DELETE"])
def cancel_booking(booking_id):
    """Cancel a booking."""
    booking = Booking.query.get_or_404(booking_id)

    if booking.status == "cancelled":
        return jsonify({"error": "Booking already cancelled"}), 400

    if booking.start_time < datetime.now():
        return jsonify({"error": "Cannot cancel past booking"}), 400

    try:
        booking.status = "cancelled"
        db.session.commit()
        return jsonify({"message": "Booking cancelled"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@bookings_bp.route("/available-rooms", methods=["GET"])
def find_available():
    """
    Find available rooms.

    Query params:
        start_time: str (ISO format)
        end_time: str (ISO format)
        capacity: int (optional)
        equipment: str (comma-separated, optional)
    """
    from app.models import find_available_rooms

    try:
        start_time = datetime.fromisoformat(request.args["start_time"])
        end_time = datetime.fromisoformat(request.args["end_time"])
    except (KeyError, ValueError):
        return jsonify({
            "error": "Required: start_time and end_time in ISO format"
        }), 400

    capacity = request.args.get("capacity", 1, type=int)

    equipment = None
    if eq_param := request.args.get("equipment"):
        equipment = [e.strip() for e in eq_param.split(",")]

    rooms = find_available_rooms(start_time, end_time, capacity, equipment)

    return jsonify({
        "available_rooms": [r.to_dict() for r in rooms],
        "search_criteria": {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "min_capacity": capacity,
            "required_equipment": equipment,
        },
    })


def get_conflicts(room_id, start_time, end_time):
    """Helper function returning conflicting bookings."""
    conflicts = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.status != "cancelled",
        Booking.start_time < end_time,
        Booking.end_time > start_time,
    ).all()

    return [
        {
            "id": b.id,
            "title": b.title,
            "start": b.start_time.isoformat(),
            "end": b.end_time.isoformat(),
        }
        for b in conflicts
    ]
