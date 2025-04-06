from flask import Flask, render_template, request
import os
import sqlite3
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()



app = Flask(__name__)
load_dotenv()

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

# Ensure data folder and DB exist
if not os.path.exists("data"):
    os.makedirs("data")
init_db()

@app.route('/space-weather')
def space_weather():
    api_key = os.getenv("NASA_API_KEY")  # from your .env
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=7)  # last 7 days

    url = f"https://api.nasa.gov/DONKI/FLR?startDate={start_date}&endDate={end_date}&api_key={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        flares = response.json()
    else:
        flares = []
    print("Fetched flares:", flares) 
    return render_template("space_weather.html", flares=flares)
api_key = os.getenv("NASA_API_KEY")

@app.route('/correlation')
def correlation():
    conn = sqlite3.connect('data/wellness.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM entries")
    rows = cursor.fetchall()
    conn.close()

    # Extract and format data
    labels = [f"Entry {i+1}" for i in range(len(rows))]
    mood = [int(row[1]) for row in rows]
    sleep = [float(row[2]) for row in rows]
    energy = [int(row[3]) for row in rows]

    # Fetch solar flare count per entry
    api_key = os.getenv("NASA_API_KEY")
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=7)
    url = f"https://api.nasa.gov/DONKI/FLR?startDate={start_date}&endDate={end_date}&api_key={api_key}"
    response = requests.get(url)
    flare_data = response.json() if response.status_code == 200 else []
    flares_per_entry = [0] * len(rows)  # Simplified count placeholder
    if flare_data:
        count = len(flare_data)
        flares_per_entry = [count] * len(rows)  # Roughly assign count equally

    return render_template("correlation.html", labels=labels, mood=mood, sleep=sleep, energy=energy, flares=flares_per_entry)



# Run app
if __name__ == '__main__':
    app.run(debug=True)
