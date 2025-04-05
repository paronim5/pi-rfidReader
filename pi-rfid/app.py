from flask import Flask, render_template, request, jsonify
import sqlite3
import subprocess

app = Flask(__name__)

DB_PATH = "/home/pi/pi-rfid/coffee_shop.db"  # Change to match your database path

def get_attendance():
    """Fetch attendance records from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT users.name, users.surname, visits.arrived_at, visits.departed_at 
        FROM users
        LEFT JOIN visits ON users.rfid_card_id = visits.rfid_card_id
        ORDER BY visits.arrived_at DESC;
    """)
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/attendance', methods=['GET'])
def attendance():
    """Return attendance records as JSON."""
    attendance = get_attendance()
    # Convert data to a list of dictionaries for easier handling in JavaScript
    attendance_data = [
        {
            "name": record[0],
            "surname": record[1],
            "arrived_at": record[2],
            "departed_at": record[3] if record[3] else "Not checked out yet"
        }
        for record in attendance
    ]
    return jsonify(attendance_data)

@app.route('/run_read', methods=['POST'])
def run_read():
    """Trigger the read.py script."""
    try:
        subprocess.Popen(["python3", "/home/pi/pi-rfid/read.py"])
        return '', 204  # No content response (success)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run_write', methods=['POST'])
def run_write():
    """Trigger the write.py script with user input."""
    try:
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        phone = request.form['phone']

        # Run write.py and pass data as command-line arguments
        subprocess.Popen(["python3", "/home/pi/pi-rfid/write.py", name, surname, email, phone])
        return '', 204  # No content response (success)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
