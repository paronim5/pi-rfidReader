import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import sqlite3
import os
from datetime import datetime

# Initialize RFID reader
reader = SimpleMFRC522()

# Automatically find the database path (modify if needed)
db_path = os.path.expanduser("/home/pi/pi-rfid/coffee_shop.db")  # Change if needed

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def log_visit_or_exit():
    """Reads RFID card and logs visit (entry) or exit in the database"""
    try:
        print("Place your RFID card near the reader...")

        # Read RFID card ID
        rfid_card_id, _ = reader.read()
        rfid_card_id = str(rfid_card_id).strip()

        print(f"Card detected! UID: {rfid_card_id}")

        # Check if user exists
        cursor.execute("SELECT name, surname FROM users WHERE rfid_card_id = ?", (rfid_card_id,))
        user = cursor.fetchone()

        if not user:
            print("Error: No user found with this RFID Card ID.")
            return

        name, surname = user
        print(f"Hello, {name} {surname}!")

        # Check if the user already has an active visit (entry without an exit)
        cursor.execute("SELECT id, departed_at FROM visits WHERE rfid_card_id = ? ORDER BY arrived_at DESC LIMIT 1", (rfid_card_id,))
        latest_visit = cursor.fetchone()

        if latest_visit:
            visit_id, departed_at = latest_visit

            if departed_at is None:
                # User is inside, log their exit by updating the `departed_at` column
                cursor.execute("UPDATE visits SET departed_at = ? WHERE id = ?", (datetime.now(), visit_id))
                conn.commit()
                print("Exit recorded successfully!")
            else:
                # User is outside, log a new entry
                cursor.execute("INSERT INTO visits (rfid_card_id, arrived_at) VALUES (?, ?)", (rfid_card_id, datetime.now()))
                conn.commit()
                print("Entry recorded successfully!")
        else:
            # No previous visits found, log a new entry
            cursor.execute("INSERT INTO visits (rfid_card_id, arrived_at) VALUES (?, ?)", (rfid_card_id, datetime.now()))
            conn.commit()
            print("Entry recorded successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        GPIO.cleanup()
        conn.close()

if __name__ == "__main__":
    log_visit_or_exit()
