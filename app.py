from flask import Flask, render_template, request, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)

DB_CONFIG = {
    "dbname": "airline",
    "user": "postgres",
    "password": "Victor@20010602",
    "host": "localhost",
    "port": 5432,
}


def get_db():
    return psycopg2.connect(**DB_CONFIG)


# ---------- page (a): search form ----------
@app.route("/")
def index():
    """Render the start page with a search form for origin, destination, and date range."""
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT airport_code, name, city, country FROM Airport ORDER BY airport_code")
    airports = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", airports=airports)


# ---------- page (b): flight results ----------
@app.route("/search", methods=["POST"])
def search_flights():
    """
    Display all available flights (regardless of whether they are completely
    booked) matching the origin, destination, and date range.
    """
    origin = request.form.get("origin", "").strip().upper()
    destination = request.form.get("destination", "").strip().upper()
    start_date = request.form.get("start_date", "")
    end_date = request.form.get("end_date", "")

    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    query = """
        SELECT f.flight_number,
               f.departure_date,
               fs.origin_code,
               fs.dest_code,
               fs.departure_time,
               fs.airline_name,
               fs.duration
          FROM Flight f
          JOIN FlightService fs ON f.flight_number = fs.flight_number
         WHERE fs.origin_code = %s
           AND fs.dest_code   = %s
           AND f.departure_date BETWEEN %s AND %s
         ORDER BY f.departure_date, fs.departure_time
    """
    cur.execute(query, (origin, destination, start_date, end_date))
    flights = cur.fetchall()
    cur.close()
    conn.close()

    return render_template(
        "results.html",
        flights=flights,
        origin=origin,
        destination=destination,
        start_date=start_date,
        end_date=end_date,
    )


# ---------- page (c): seat availability ----------
@app.route("/flight/<flight_number>/<departure_date>")
def flight_detail(flight_number, departure_date):
    """
    Show the number of available seats and the plane capacity for a
    specific flight_number + departure_date combination.
    """
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    query = """
        SELECT fs.flight_number,
               fs.airline_name,
               fs.origin_code,
               fs.dest_code,
               fs.departure_time,
               fs.duration,
               f.departure_date,
               f.plane_type,
               a.capacity,
               a.capacity - COUNT(b.pid) AS available_seats,
               COUNT(b.pid)              AS booked_seats
          FROM Flight f
          JOIN FlightService fs ON f.flight_number  = fs.flight_number
          JOIN Aircraft a       ON f.plane_type      = a.plane_type
          LEFT JOIN Booking b   ON b.flight_number   = f.flight_number
                               AND b.departure_date  = f.departure_date
         WHERE f.flight_number  = %s
           AND f.departure_date = %s
         GROUP BY fs.flight_number, fs.airline_name, fs.origin_code,
                  fs.dest_code, fs.departure_time, fs.duration,
                  f.departure_date, f.plane_type, a.capacity
    """
    cur.execute(query, (flight_number, departure_date))
    detail = cur.fetchone()
    cur.close()
    conn.close()

    return render_template("detail.html", detail=detail)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
