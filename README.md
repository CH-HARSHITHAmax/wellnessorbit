# WellnessOrbit 🌌

**A full-stack web app to correlate user wellness (mood, sleep, energy) with real-time space weather data like solar flares.**

---

## 🌟 Features

- 📊 Log mood, sleep hours, and energy levels.
- ☀️ View NASA’s solar flare data from the last 7 days.
- 📈 See correlation between your wellness and space weather.
- 📦 Data stored using SQLite database.
- ☁️ Live deployed on Render.

---

## 🛠️ Technologies Used

- Python (Flask)
- HTML, CSS, JavaScript
- SQLite3
- NASA DONKI API
- Chart.js
- Render (Deployment)

---

## 🚀 Setup & Usage

### 🔧 Prerequisites
- Python 3.11+
- `pip install -r requirements.txt`

### ▶️ Running Locally
```bash
git clone https://github.com/CH-HARSHITHAmax/wellnessorbit.git
cd wellnessorbit
pip install -r requirements.txt
python app.py

🧩 Challenges & Solutions
1.NASA API returned no flares at first – Confirmed it's realistic due to recent solar activity; added debug prints and handled fallback cases.

2.Deployment Issues on Render – Ensured correct port binding and gunicorn setup in requirements.txt.

3.Data type mismatches in correlation – Validated and casted form inputs before processing; added error messages for invalid data.

---
 📩 Contact

Created by **CH Harshitha** | B.Tech Electronics & Communication Engineering  
📧 Email: 22wh1a0424@bvrithyderabad.edu.in
🔗 GitHub: [@CH-HARSHITHAmax](https://github.com/CH-HARSHITHAmax)  
🌐 Project: [WellnessOrbit](https://wellnessorbit.onrender.com/)



Add README.md with project details
Update README with contact details
Update README with Challenges & Solutions
