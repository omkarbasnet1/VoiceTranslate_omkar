import sqlite3
from datetime import datetime

DB_FILE = "db.sqlite3"


def get_connection():
    """Establishes and return a connection to the SQLite database."""
    return sqlite3.connect(DB_FILE)


def get_all_rooms():
    """Helper function to fetch all rooms so it helps in UI can display them"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, room_name, capacity FROM booking_meetingroom")
    rooms = cursor.fetchall()
    conn.close()
    return rooms


def add_room(name: str, capacity: int):
    """Adds a new room to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("Insert INTO booking_meetingroom "
                       "(room_name, capacity, is_active) VALUES (?, ? , 1)",
                       (name, capacity))
        conn.commit()
        return True, f"Room '{name}' added successfully"
    except Exception as e:
        return False, f" Error adding room: {e}"
    finally:
        conn.close()


def update_room(name: str, new_capacity: int):
    """Updates the capacity"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE booking_meetingroom SET capacity = ? WHERE room_name = ?", (new_capacity, name))
        if cursor.rowcount == 0:
            return False, f"Room '{name}' not found"
        conn.commit()
        return True, f"Room '{name}' capacity updated to {new_capacity}"
    except Exception as e:
        return False, f"Error updating capacity: {e}"
    finally:
        conn.close()


def remove_room(name: str):
    """Removes a room, deletes its reservation and generates cancellation report."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM booking_meetingroom "
                       "WHERE room_name = ?",
                       (name,))
        room = cursor.fetchone()
        if not room:
            return False, f"Room '{name}' not found."

        room_id = room[0]

        query = """
                Select u.username
                from booking_bookinghistory b
                Join member_customuser u ON b.booked_by_id = u.id
                Where b.meeting_room_id = ? """
        cursor.execute(query, (room_id,))
        cancelled_users = [row[0] for row in cursor.fetchall()]

        cursor.execute("DELETE FROM booking_bookinghistory WHERE meeting_room_id = ?",
                       (room_id,))

        cursor.execute("DELETE FROM booking_meetingroom WHERE id = ?",
                       (room_id,))

        conn.commit()
        with open("cancellation_report.txt", "a") as f:
            f.write(f"\n Room '{name}' Deleted on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \n")
            if cancelled_users:
                unique_users = set(cancelled_users)
                f.write("Cancelled reservations for the usernames \n")
                for user in unique_users:
                    f.write(f" {user} \n")
            else:
                f.write("No existing reservations \n")
        if cancelled_users:
            unique_users = set(cancelled_users)
            user_list_str = ",".join(unique_users)
            report_msg = (
                f"Room '{name}' deleted.\n\n"
                f"Cancelled reservations for: {user_list_str}\n\n"
                "Report saved to cancellation_report.txt"
            )
        else:
            report_msg = f"Room '{name}' deleted.\n\n No existing reservation."

        return True, report_msg

    except Exception as e:
        return False, f"Error removing room: {e}"
    finally:
        conn.close()
