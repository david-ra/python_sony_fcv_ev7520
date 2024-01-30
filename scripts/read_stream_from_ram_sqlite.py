import cv2
import numpy as np
import sqlite3

RAM_PATH = "/Volumes/RAMDisk"
FILENAME = "stream.jpg"
DB = "camera_streams.sqlite"

# Connect to the SQLite database
connection = sqlite3.connect(f'{RAM_PATH}/{DB}')
cursor = connection.cursor()
camera_id = 0

while True:
    cursor.execute("SELECT * FROM streams_data WHERE id=0;")
    # Fetch the result
    result = cursor.fetchone()
    image = np.frombuffer(result[1], dtype=np.uint8).reshape((720, 1280, 3))
    cv2.imshow("frame", image)
    key = cv2.waitKey(3)
    if key == 27: 
        print('Pressed Esc, free camera resource')

        break

connection.close()