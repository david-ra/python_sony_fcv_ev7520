
import os
import redis
import matplotlib.pyplot as plt
import numpy as np
import cv2

# read environment variables
from dotenv import load_dotenv
load_dotenv()

redis_cli = redis.StrictRedis(
    host=os.environ["REDIS_HOST"],
    port=int(os.environ["REDIS_PORT"]),
    password=os.environ["REDIS_PASSWORD"])

#numpy_bytes = redis_cli.get("camera_0")
#decoded = np.frombuffer(numpy_bytes, dtype=np.uint8).reshape((720, 1280,3))
while True:
    numpy_bytes = redis_cli.get("camera_0")
    if numpy_bytes:
        decoded = np.frombuffer(numpy_bytes, dtype=np.uint8).reshape((720, 1280,3))
        cv2.imshow('frame', decoded)

    key = cv2.waitKey(3)
    if key == 27:
        print('Pressed Esc')
        break