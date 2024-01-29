import os 
import cv2
import redis
import argparse
from typing import List

# imports for threading streaming
import threading
import signal
import time

from .Camera import SonyCamera

# Configure logging
import logging as logger
logger.basicConfig(
    level=logger.INFO,  # Set the logging level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s')  # Define the log message format

# GLOBAL FLAG FOR STREAMING STATE - ON/OFF
continue_streaming = True


def stop_streaming(signal, frame):
    global continue_streaming
    logger.info("Stopping streamming service...")
    continue_streaming = False

def start_streaming(camera:SonyCamera, resolution:tuple, timeout:int=5000):
    redis_cli = redis.StrictRedis(
            host=os.environ["REDIS_HOST"],
            port=int(os.environ["REDIS_PORT"]),
            password=os.environ["REDIS_PASSWORD"])
    
    logger.info(f"Starting Streaming to Redis {os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}")
    
    
    while camera.conn.isOpen() and continue_streaming:
        # getting current frame
        ret, frame = camera.stream.read()
        if ret:
            redis_cli.set(f"camera_{camera.camera_id}", frame.tobytes())
    
    #free device resources
    camera.close()
    camera.stream.release()

def main():
    # Configure signal handling for camera threads
    signal.signal(signal.SIGINT, stop_streaming)
    # get all camera controllers
    resolution = (int(os.environ["WIDTH"]), int(os.environ["HEIGHT"]))
    threads = []
    camera_thread = threading.Thread(target=start_streaming, args=("04b4","00f9"))
    threads.append(camera_thread)
    camera_thread.start() # starting execution
    
    # waiting for threads to end
    [thread.join() for thread in threads]

    logger.info("Main controller end...")
    pass

if __name__ == '__main__':
    main()
