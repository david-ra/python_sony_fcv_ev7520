
import os
import redis
import matplotlib.pyplot as plt
import numpy as np
import cv2

# read environment variables
from dotenv import load_dotenv
load_dotenv()

cap = cv2.VideoCapture(0)
#numpy_bytes = redis_cli.get("camera_0")
#decoded = np.frombuffer(numpy_bytes, dtype=np.uint8).reshape((720, 1280,3))
while True:
    ret, frame = cap.read()
    print("type", type(frame))

    cv2.imshow('frame', frame)

    key = cv2.waitKey(3)
    if key == 27:
        print('Pressed Esc, free camera resource')
        cap.release()
        print('breaking loop')
        break

