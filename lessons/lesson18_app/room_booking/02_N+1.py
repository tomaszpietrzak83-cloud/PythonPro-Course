import time

from app import create_app
from app.models import Booking, db
from sqlalchemy import event
from sqlalchemy.orm import joinedload

app = create_app()
query_count = 0


def count_queries(conn, cursor, statement, parameters, context, executemany):
    global query_count
    query_count += 1


with app.app_context():
    event.listen(db.engine, "before_cursor_execute", count_queries)


@app.route("/debug/n-plus-1")
def demo_n_plus_1():

    global query_count

    query_count = 0
    start = time.time()
    products = Booking.query.all()
    bad_result = []
    for p in products:
        bad_result.append(f"{p.title} - {p.room.name} - {p.user.name} ")
    bad_time = time.time() - start
    bad_queries = query_count

    query_count = 0
    start = time.time()
    products = Booking.query.options(
        joinedload(Booking.room), joinedload(Booking.user)
    ).all()
    good_result = []
    for p in products:
        good_result.append(f"{p.title} - {p.room.name} - {p.user.name}")
    good_time = time.time() - start
    good_queries = query_count
    return f"""
    <head>
        <meta charset="UTF-8">
    </head>
    <h2>Porównanie wydajności</h2>
    <table border="1" cellpadding="10">
        <tr>
            <th>Metoda</th>
            <th>Zapytań SQL</th>
            <th>Czas</th>
        </tr>
        <tr style="background: #ffcccc">
            <td>❌ Bez optymalizacji (N+1)</td>
            <td>{bad_queries}</td>
            <td>{bad_time * 1000:.2f} ms</td>
        </tr>
        <tr style="background: #ccffcc">
            <td>✅ Z joinedload</td>
            <td>{good_queries}</td>
            <td>{good_time * 1000:.2f} ms</td>
        </tr>
    </table>
    <p>Różnica: {bad_queries / good_queries:.0f}x mniej zapytań!</p>
    """


if __name__ == "__main__":
    app.run(debug=True, port=5000)
