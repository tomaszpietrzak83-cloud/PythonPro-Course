# --- Task 04: Notifications ---
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request

from app.models import Booking, Notification, db

notification_bp = Blueprint("notification", __name__)


@notification_bp.route("/api/notifications", methods=["GET"])
def get_notifications():
    current_user_id = request.args.get("user_id", type=int)
    if current_user_id is None:
        return jsonify({"error": "Missing user_id"}), 400
    else:
        notifications = (
            Notification.query
            .filter_by(user_id=current_user_id, is_read=False)
            .order_by(Notification.created_at.desc())
            .all()
        )

        return jsonify(
            notifications=[
                {
                    "id": n.id,
                    "message": n.message,
                    "is_read": n.is_read,
                    "created_at": n.created_at.isoformat(),
                    "booking_id": n.booking_id,
                    "notification_type": n.notification_type,
                    "user_id": n.user_id,
                    "booking": {
                        "id": n.booking.id,
                        "room_id": n.booking.room_id,
                        "start_time": n.booking.start_time.isoformat(),
                        "end_time": n.booking.end_time.isoformat(),
                    }
                    if n.booking
                    else None,
                }
                for n in notifications
            ]
        )


@notification_bp.route("/api/notifications/<int:id>/read", methods=["POST"])
def mark_notification_as_read(id):
    notification = Notification.query.get(id)
    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    notification.is_read = True
    db.session.commit()

    return jsonify({"message": "Notification marked as read"})


def create_upcoming_booking_reminders():
    now = datetime.now()
    one_hour_later = now + timedelta(hours=1)

    upcoming_bookings = Booking.query.filter(
        Booking.status == "confirmed",
        Booking.start_time.between(now, one_hour_later),
    ).all()

    for booking in upcoming_bookings:
        existing = Notification.query.filter_by(
            booking_id=booking.id,
            user_id=booking.user_id,
            notification_type="booking_reminder",
        ).first()

        if existing:
            continue

        reminder_notification = Notification(
            user_id=booking.user_id,
            message=f"Reminder: Your booking '{booking.title}' starts soon.",
            booking_id=booking.id,
            notification_type="booking_reminder",
            is_read=False,
        )
        db.session.add(reminder_notification)

    db.session.commit()


@notification_bp.route(
    "/api/notifications/run-reminders", methods=["GET", "POST"]
)
def run_reminders():
    create_upcoming_booking_reminders()
    return jsonify({"message": "Reminder check completed"})
