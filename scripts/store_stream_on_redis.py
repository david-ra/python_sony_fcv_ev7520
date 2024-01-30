import cv2
import os
import redis

# read environment variables
from dotenv import load_dotenv
load_dotenv(override=True)

camera_id = 0
def main():

    redis_cli = redis.StrictRedis(
            host=os.environ["REDIS_HOST"],
            port=int(os.environ["REDIS_PORT"]),
            password=os.environ["REDIS_PASSWORD"])
    
    stream = cv2.VideoCapture(0)

    while True:
        ret, frame = stream.read()

        redis_cli.set(f"camera_{camera_id}", frame.tobytes())
        
        key = cv2.waitKey(3)
        if key == 27: 
            print('Pressed Esc, free camera resource')
            stream.release()
            break

if __name__ == '__main__':
    main()
