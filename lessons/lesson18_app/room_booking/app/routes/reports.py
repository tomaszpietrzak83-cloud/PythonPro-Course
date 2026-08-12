from datetime import datetime
from io import BytesIO

import matplotlib.pyplot as plt
from flask import Blueprint, jsonify, request, send_file
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from sqlalchemy import desc, func

from app.models import Booking, Room, User, db

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/monthly", methods=["GET"])
def monthly_report():

    month = request.args.get("month")

    if not month:
        return jsonify({"error": "Missing month"}), 400

    try:
        month_start = datetime.strptime(month, "%Y-%m")
    except ValueError:
        return jsonify({"error": "Month must be in YYYY-MM format"}), 400

    if month_start.month == 12:
        next_month_start = datetime(month_start.year + 1, 1, 1)
    else:
        next_month_start = datetime(month_start.year, month_start.month + 1, 1)

    bookings = Booking.query.filter(
        Booking.start_time >= month_start,
        Booking.start_time < next_month_start,
        Booking.status != "cancelled",
    ).all()

    booking_count = len(bookings)
    total_hours = sum(booking.duration_hours for booking in bookings)
    total_revenue = sum(booking.total_cost for booking in bookings)

    top_rooms = (
        db.session
        .query(
            Room.name,
            func.count(Booking.id).label("booking_count"),
        )
        .join(Booking)
        .filter(
            Booking.start_time >= month_start,
            Booking.start_time < next_month_start,
            Booking.status != "cancelled",
        )
        .group_by(Room.name)
        .order_by(desc("booking_count"))
        .limit(10)
        .all()
    )

    top_users = (
        db.session
        .query(
            User.name,
            func.count(Booking.id).label("booking_count"),
        )
        .join(Booking)
        .filter(
            Booking.start_time >= month_start,
            Booking.start_time < next_month_start,
            Booking.status != "cancelled",
        )
        .group_by(User.name)
        .order_by(desc("booking_count"))
        .limit(10)
        .all()
    )

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.setTitle(f"Monthly report {month}")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 800, f"Monthly report: {month}")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 770, f"Bookings: {booking_count}")
    pdf.drawString(50, 750, f"Total hours: {round(total_hours, 2)}")
    pdf.drawString(50, 730, f"Total revenue: {round(total_revenue, 2)}")
    pdf.drawString(50, 700, "Top rooms:")

    room_labels = [row[0] for row in top_rooms]
    room_values = [row[1] for row in top_rooms]

    for i, (label, value) in enumerate(zip(room_labels, room_values), start=1):
        pdf.drawString(50, 680 - i * 20, f"{label}: {value}")

    user_labels = [row[0] for row in top_users]
    user_values = [row[1] for row in top_users]

    pdf.drawString(300, 700, "Top users:")
    for i, (label, value) in enumerate(zip(user_labels, user_values), start=1):
        pdf.drawString(300, 680 - i * 20, f"{label}: {value}")

    pdf.showPage()

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 800, f"Room utilization chart: {month}")

    def build_room_chart(labels, values):
        buffer = BytesIO()

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(labels, values, color="#4e79a7")
        ax.set_title("Room utilization")
        ax.set_ylabel("Bookings")
        plt.xticks(rotation=25, ha="right")
        plt.tight_layout()

        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)

        return buffer

    chart_buffer = build_room_chart(room_labels, room_values)

    pdf.drawImage(
        ImageReader(chart_buffer),
        50,
        450,
        width=500,
        height=250,
    )

    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"monthly_report_{month}.pdf",
        mimetype="application/pdf",
    )
