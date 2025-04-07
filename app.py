from flask import Flask, render_template, request
import os
import sqlite3
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Ensure data folder and DB exist
if not os.path.exists("data"):
    os.makedirs("data")

# Database initialization
def init_db():
    conn = sqlite3.connect('data/wellness.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT NOT NULL,
            sleep REAL NOT NULL,
            energy TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home route to handle form submission
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mood = request.form.get('mood')
        sleep = request.form.get('sleep')
        energy = request.form.get('energy')

        conn = sqlite3.connect('data/wellness.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entries (mood, sleep, energy) VALUES (?, ?, ?)",
                       (mood, sleep, energy))
        conn.commit()
        conn.close()

    return render_template('index.html')

# Logs route to show all entries
@app.route('/logs')
def logs():
    conn = sqlite3.connect('data/wellness.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries")
    entries = cursor.fetchall()
    conn.close()
    return render_template("logs.html", entries=entries)

# Space weather data route
@app.route('/space-weather')
def space_weather():
    api_key = os.getenv("NASA_API_KEY")
    if not api_key:
        return "NASA API key not found. Please set it in your .env or environment variables.", 500

    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=7)

    url = f"https://api.nasa.gov/DONKI/FLR?startDate={start_date}&endDate={end_date}&api_key={api_key}"
    response = requests.get(url)
    flares = response.json() if response.status_code == 200 else []

    return render_template("space_weather.html", solar_flares=flares)

# Correlation visualization route
@app.route('/correlation')
def correlation():
    conn = sqlite3.connect('data/wellness.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries")
    rows = cursor.fetchall()
    conn.close()

    labels = [f"Entry {i+1}" for i in range(len(rows))]

    try:
        mood = [int(row[1]) for row in rows]
        sleep = [float(row[2]) for row in rows]
        energy = [int(row[3]) for row in rows]
    except ValueError:
        return "Invalid data found in the database. Please ensure inputs are numeric.", 500

    # Fetch solar flare data
    api_key = os.getenv("NASA_API_KEY")
    if not api_key:
        return "NASA API key not found. Please set it in your .env or environment variables.", 500

    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=7)
    url = f"https://api.nasa.gov/DONKI/FLR?startDate={start_date}&endDate={end_date}&api_key={api_key}"

    response = requests.get(url)
    flare_data = response.json() if response.status_code == 200 else []
    flares_per_entry = [len(flare_data)] * len(rows) if flare_data else [0] * len(rows)

    return render_template("correlation.html", labels=labels, mood=mood, sleep=sleep, energy=energy, flares=flares_per_entry)

# Run app locally
if __name__ == '__main__':
    app.run(debug=True)
