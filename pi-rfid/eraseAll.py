import sqlite3
import os

# Automatically find the database path (modify if needed)
db_path = os.path.expanduser("/home/pi/pi-rfid/coffee_shop.db")  # Change if needed

def clear_database():
    """Deletes all data from the database for testing purposes."""
    confirmation = input("Are you sure you want to delete ALL data? (yes/no): ").strip().lower()
    
    if confirmation != "yes":
        print("Operation canceled.")
        return

    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Delete all data from tables
        cursor.execute("DELETE FROM users;")
        cursor.execute("DELETE FROM visits;")

        # Reset visit_id and exit_id in users table
        cursor.execute("UPDATE users SET visit_id = NULL, exit_id = NULL;")

        # Commit changes
        conn.commit()
        print("All data has been erased successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    clear_database()
