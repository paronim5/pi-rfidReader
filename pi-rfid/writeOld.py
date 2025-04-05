import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import sqlite3
import os

# Initialize RFID reader
reader = SimpleMFRC522()

# Automatically find the database path (modify if needed)
db_path = os.path.expanduser("/home/pi/pi-rfid/coffee_shop.db")  # Change if your database is elsewhere

# Connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def add_user():
    """Function to read RFID card ID and add user to the database"""
    try:
        print("Place your RFID card near the reader...")
        
        # Read the RFID card ID
        rfid_card_id, _ = reader.read()
        rfid_card_id = str(rfid_card_id)  # Convert to string for database storage

        print(f"Card detected! UID: {rfid_card_id}")

        # Ask for user details
        name = input("Enter First Name: ").strip()
        surname = input("Enter Surname: ").strip()
        email = input("Enter Email (optional): ").strip() or None
        phone = input("Enter Phone Number (optional): ").strip() or None

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
    add_user()
