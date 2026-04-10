# Problem Set 3, Problem 1: Airline Flight Search

A Flask web application that lets users search for flights by origin/destination airport and date range, view matching flights, and check seat availability.

## Requirements

- Python 3.8+
- PostgreSQL 14+
- `pip install flask psycopg2-binary`

## Database Setup

1. **Open pgAdmin** and connect to your PostgreSQL server.

2. **Create a new database and load the schema and data**:
    using flights.sql

3. **Add foreign key constraints**:

```sql
ALTER TABLE FlightService ADD CONSTRAINT fk_origin FOREIGN KEY (origin_code) REFERENCES Airport(airport_code);
ALTER TABLE FlightService ADD CONSTRAINT fk_dest FOREIGN KEY (dest_code) REFERENCES Airport(airport_code);
ALTER TABLE Flight ADD CONSTRAINT fk_flight_service FOREIGN KEY (flight_number) REFERENCES FlightService(flight_number);
ALTER TABLE Flight ADD CONSTRAINT fk_plane_type FOREIGN KEY (plane_type) REFERENCES Aircraft(plane_type);
ALTER TABLE Booking ADD CONSTRAINT fk_passenger FOREIGN KEY (pid) REFERENCES Passenger(pid);
ALTER TABLE Booking ADD CONSTRAINT fk_flight FOREIGN KEY (flight_number, departure_date) REFERENCES Flight(flight_number, departure_date);
```

4. **Update `DB_CONFIG` in `app.py`** to match your PostgreSQL credentials (username, password, host, port).

## Running

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Features

### (a) Search Form
The start page presents a form with dropdown selectors for origin and destination airport codes, plus date pickers for a continuous date range.

### (b) Flight Results
After submitting, all matching flights are displayed (regardless of booking status) with flight number, departure date, origin/destination codes, departure time, airline, and duration. Each row is clickable.

### (c) Seat Availability
Clicking a flight shows the plane type, total capacity, number of booked seats, and number of available seats.

## Project Structure

```
airline-app/
├── app.py              ← Flask app: routes + SQL queries
└── templates/
    ├── base.html       ← Shared layout & CSS (extended by all pages)
    ├── index.html      ← Page (a): search form
    ├── results.html    ← Page (b): list of matching flights
    └── detail.html     ← Page (c): seat availability for one flight
```
