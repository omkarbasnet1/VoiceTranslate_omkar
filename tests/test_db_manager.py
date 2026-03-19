import pytest
import sqlite3
import os
import db_manager


@pytest.fixture(scope="module")
def test_db():
    test_db_file = "test_db.sqlite3"

    if os.path.exists(test_db_file):
        os.remove(test_db_file)

    original_db = db_manager.DB_FILE
    db_manager.DB_FILE = test_db_file

    conn = sqlite3.connect(test_db_file)
    cursor = conn.cursor()

    # meeting room table
    cursor.execute("""
        CREATE Table booking_meetingroom(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            is_active INTEGER DEFAULT 1
        )
    """)

    # booking history table
    cursor.execute("""
        CREATE Table booking_bookinghistory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meeting_room_id INTEGER,
            booked_by_id INTEGER,
            start_time TEXT,
            end_time TEXT
        )
    """)

    # user table
    cursor.execute("""
        CREATE TABLE member_customuser (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

    yield test_db_file

    # cleanup after all tests
    db_manager.DB_FILE = original_db
    if os.path.exists(test_db_file):
        os.remove(test_db_file)


# test adding a room works
def test_add_room(test_db):
    print("\n testing add room function")

    # add a room
    success, message = db_manager.add_room("Test Room A", 10)
    assert success is True, "add room should return True"
    assert "successfully" in message.lower(), "success message should be successfully"

    # verify it actually got added to database
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("Select room_name, capacity FROM booking_meetingroom WHERE room_name = ?", ("Test Room A",))
    result = cursor.fetchone()
    conn.close()

    assert result is not None, " room should exist in database"
    assert result[0] == "Test Room A"
    assert result[1] == 10
    print("room added ")


# test updating capacity works
def test_update_room_capacity(test_db):
    print("\n testing update room functions")

    # add a room first
    db_manager.add_room("Test Room B", 5)

    # update capacity
    success, message = db_manager.update_room("Test Room B", 15)
    assert success is True, "update should success"
    assert "updated" in message.lower()

    # check database has new capacity
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT capacity FROM booking_meetingroom WHERE room_name = ?", ("Test Room B",))
    result = cursor.fetchone()
    conn.close()

    assert result is not None
    assert result[0] == 15, "capacity should be updated to 15"
    print("capacity updated")


# test removing room and cancellation report
def test_remove_room(test_db):
    print("\n testing remove room function")

    # setup for room,user and booking
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO booking_meetingroom "
                   "(room_name, capacity, is_active) VALUES(?, ? , 1)",
                   ("Test Room C", 8))
    room_id = cursor.lastrowid

    cursor.execute("INSERT INTO member_customuser "
                   "(username) VALUES (?)", ("testuser123",))
    user_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO booking_bookinghistory
        (meeting_room_id, booked_by_id, start_time, end_time)
        Values(?, ?, '2026-03-10 10:00AM', '2026-03-10 11:00AM')
    """, (room_id, user_id))
    conn.commit()
    conn.close()

    # remove the room
    success, message = db_manager.remove_room("Test Room C")
    assert success is True, "remove should success"
    assert "user123" in message, "message should mention cancelled user"

    # verify room
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM booking_meetingroom "
                   "WHERE room_name = ?", ("Test Room C",))
    room_result = cursor.fetchone()

    # verify bookings are gone
    cursor.execute("SELECT * FROM booking_bookinghistory "
                   "WHERE meeting_room_id = ?", (room_id,))
    booking_result = cursor.fetchone()
    conn.close()

    assert room_result is None, " Room should deleted"
    assert booking_result is None, "booking should deleted"

    # check cancellation report
    assert os.path.exists("cancellation_report.txt"), "report file should exist"
    print(" room removed and booking cancelled")


def test_update_non_room(test_db):
    print("\n Testing update on a room that does not exist")
    success, message = db_manager.update_room("Ghost Room", 50)
    assert success is False, "update a non existing room fail"
    assert "not found" in message.lower(), "Message that the room was not found"
