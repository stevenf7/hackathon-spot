import cv2
import imutils
import os
from queue import Queue
import threading
import time
# from spot_controller import SpotController
from robot_interface import RobotInterface
from spot_controller import SpotController

ROBOT_IP = "192.168.50.3"#os.environ['ROBOT_IP']
SPOT_USERNAME = "admin"#os.environ['SPOT_USERNAME']
SPOT_PASSWORD = "2zqa8dgw7lor"#os.environ['SPOT_PASSWORD']


queue = Queue(10)

cam = cv2.VideoCapture(0)

def listen():
    for i in range(5):
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        time.sleep(3)
        # arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_50)
        # arucoParams = cv2.aruco.DetectorParameters_create()
        # (corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict, parameters=arucoParams)

        # if len(ids) == 0:
        #     time.sleep(0.2)
        #     continue

        # listen for voice command
        # convert to text
        # upload to openai
        # get command
        # push command on queue

def action():
    while True:
        cmd = queue.get()
        

def main():
    listen_thread = threading.Thread(target=listen)
    listen_thread.start()


def main2():
    #example of using micro and speakers
    print("Start recording audio")
    sample_name = "aaaa.wav"
    cmd = f'arecord -vv --format=cd --device={os.environ["AUDIO_INPUT_DEVICE"]} -r 48000 --duration=10 -c 1 {sample_name}'
    print(cmd)
    os.system(cmd)
    print("Playing sound")
    os.system(f"ffplay -nodisp -autoexit -loglevel quiet {sample_name}")
    
    # Capture image
    camera_capture = cv2.VideoCapture(0)
    rv, image = camera_capture.read()
    print(f"Image Dimensions: {image.shape}")
   
    with SpotController(username=SPOT_USERNAME, password=SPOT_PASSWORD, robot_ip=ROBOT_IP) as spot:

        controller = RobotInterface(spot)

        controller.describe_env(camera_capture)
        
        controller.dance()

        # controller.sit()

        # controller.stand()

        # controller.move_forward()

        # controller.move_backward()

        # controller.move_left()

        # controller.move_right()

    
    camera_capture.release()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
