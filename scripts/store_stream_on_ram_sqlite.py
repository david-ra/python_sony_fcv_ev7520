
RAM_PATH = "/Volumes/RAMDisk"
FILENAME = "stream.jpg"
DB = "camera_streams.sqlite"
import sqlite3
import numpy as np
import io
import sys
import cv2

cap = cv2.VideoCapture(0)


conn = sqlite3.connect(f'{RAM_PATH}/{DB}', detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn.cursor()
# Create a table (if not exists) with a BLOB column
cursor.execute('''CREATE TABLE IF NOT EXISTS streams_data (id INTEGER PRIMARY KEY, data BLOB)''')

camera_id = 0

cursor.execute(f"select id from streams_data where id={camera_id};")
existing_record = cursor.fetchone()

if existing_record:
    pass
else:
    # If the record does not exist, perform an insert
    cursor.execute('''INSERT INTO streams_data (id, data) VALUES (?, ?)''', (camera_id, b'\04'))

try:
    while True:
        ret, frame = cap.read()
        # Insert the NumPy array bytes into the table
        #print("write frame", frame.tobytes())
        # If the record exists, perform an update
        _frame = frame.tobytes()
        cursor.execute('''UPDATE streams_data SET data = ? WHERE id = ?''', (_frame, 0))

        # Commit the changes and close the connection
        conn.commit()
        key = cv2.waitKey(3)
        if key == 27: 
            print('Pressed Esc, free camera resource')
            cap.release()
            conn.commit()
            conn.close()
            break

except KeyboardInterrupt:
    cap.release()
    sys.exit(0)