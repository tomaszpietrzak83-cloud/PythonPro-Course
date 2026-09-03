"""
Debug endpoints for query performance exercises.
"""

from time import perf_counter

from flask import Blueprint, render_template
from sqlalchemy import event
from sqlalchemy.orm import joinedload

from app.models import Booking, db

debug_bp = Blueprint("debug", __name__)


def collect_bookings(query):
    return [
        {
            "title": booking.title,
            "room": booking.room.name,
            "user": booking.user.name,
        }
        for booking in query.all()
    ]


@debug_bp.route("/debug/n-plus-1")
# TASK 02
def debug_n_plus_1():
    query_count = 0

    def count_queries(conn, cursor, statement, parameters, context, executemany):
        nonlocal query_count
        query_count += 1

    event.listen(db.engine, "before_cursor_execute", count_queries)
    try:
        query_count = 0
        start = perf_counter()
        unoptimized = collect_bookings(Booking.query)
        unoptimized_time = perf_counter() - start
        unoptimized_queries = query_count

        query_count = 0
        start = perf_counter()
        optimized = collect_bookings(
            Booking.query.options(
                joinedload(Booking.room),
                joinedload(Booking.user),
            )
        )
        optimized_time = perf_counter() - start
        optimized_queries = query_count
    finally:
        event.remove(db.engine, "before_cursor_execute", count_queries)

    return render_template(
        "debug_n_plus_1.html",
        unoptimized={
            "query_count": unoptimized_queries,
            "time_ms": round(unoptimized_time * 1000, 2),
            "rows": len(unoptimized),
            "sample": unoptimized[:5],
        },
        optimized={
            "query_count": optimized_queries,
            "time_ms": round(optimized_time * 1000, 2),
            "rows": len(optimized),
            "sample": optimized[:5],
        },
        query_ratio=round(unoptimized_queries / optimized_queries, 1)
        if optimized_queries
        else None,
    )
