import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import sqlite3
import os
import sys

# Initialize RFID reader
reader = SimpleMFRC522()

# Automatically find the database path
db_path = os.path.expanduser("/home/pi/pi-rfid/coffee_shop.db")

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def add_user(name, surname, email, phone):
    """Function to read RFID card ID and add user to the database"""
    try:
        print("Place your RFID card near the reader...")
        
        # Read the RFID card ID
        rfid_card_id, _ = reader.read()
        rfid_card_id = str(rfid_card_id)  # Convert to string for database storage

        print(f"Card detected! UID: {rfid_card_id}")

        # Insert into the database
        cursor.execute("""
            INSERT INTO users (rfid_card_id, name, surname, email, phone)
            VALUES (?, ?, ?, ?, ?)
        """, (rfid_card_id, name, surname, email, phone))
        conn.commit()

        print("User successfully added to the database!")

    except sqlite3.IntegrityError:
        print("Error: This RFID Card ID already exists in the database.")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        GPIO.cleanup()
        conn.close()

if __name__ == "__main__":
    # Get user input from command-line arguments
    if len(sys.argv) < 5:
        print("Usage: python3 write.py <name> <surname> <email> <phone>")
        sys.exit(1)

    name = sys.argv[1]
    surname = sys.argv[2]
    email = sys.argv[3]
    phone = sys.argv[4]

    add_user(name, surname, email, phone)
