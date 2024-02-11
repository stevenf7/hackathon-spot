import cv2
import os
from queue import Queue
import threading
import time
# from spot_controller import SpotController
from robot_interface import RobotInterface
from spot_controller import SpotController

ROBOT_IP = "192.168.50.3" # os.environ['ROBOT_IP']
SPOT_USERNAME = "admin" # os.environ['SPOT_USERNAME']
SPOT_PASSWORD = "2zqa8dgw7lor" # os.environ['SPOT_PASSWORD']


queue = Queue(10)


def listen():
    cam = cv2.VideoCapture(0)
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    aruco_params = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

    for i in range(100):
        ret, frame = cam.read()
        if ret: 
            corners, ids, rejected = detector.detectMarkers(frame)

            if not corners:
                pass
            else:
                match ids[0]:
                    case 0:
                        queue.put("<stop>")
                    case 1:
                        queue.put("<describe>")
                    case 2:
                        queue.put("<dance>")
                    case 3:
                        queue.put("<sit>") 
                    case 4:
                        queue.put("<stand>")
                    case 5:
                        queue.put("<forward>")
                    case 6:
                        queue.put("<back>")
                    case 7:
                        queue.put("<left>")
                    case 8:
                        queue.put("<right>")
        else:
            print("failed to capture image")
        time.sleep(1)

    queue.put("<STOP>")
    cam.release()
    cv2.destroyAllWindows()

def action():
    with SpotController(username=SPOT_USERNAME, password=SPOT_PASSWORD, robot_ip=ROBOT_IP) as spot:
        robot = RobotInterface(spot)
        for _ in range(100):
            cmd = queue.get()
            match cmd:
                case "<describe>":
                    robot.describe_env()
                case "<dance>":
                    robot.dance()
                case "<sit>":
                    robot.sit()
                case "<stand>":
                    robot.stand()
                case "<forward>":
                    robot.move_forward()
                case "<backward>":
                    robot.move_backward()
                case "<left>":
                    robot.move_left()
                case "<right>":
                    robot.move_right()
                case other:
                    break


def main():
    action_thread = threading.Thread(target=action)
    action_thread.start()
    listen()


# def main2():
#     #example of using micro and speakers
#     print("Start recording audio")
#     sample_name = "aaaa.wav"
#     cmd = f'arecord -vv --format=cd --device={os.environ["AUDIO_INPUT_DEVICE"]} -r 48000 --duration=10 -c 1 {sample_name}'
#     print(cmd)
#     os.system(cmd)
#     print("Playing sound")
#     os.system(f"ffplay -nodisp -autoexit -loglevel quiet {sample_name}")
    
#     # Capture image
#     camera_capture = cv2.VideoCapture(0)
#     rv, image = camera_capture.read()
#     print(f"Image Dimensions: {image.shape}")
   
#     with SpotController(username=SPOT_USERNAME, password=SPOT_PASSWORD, robot_ip=ROBOT_IP) as spot:
#         controller = RobotInterface(spot)
#         controller.describe_env(camera_capture)
#         controller.dance()
#         # controller.sit()
#         # controller.stand()
#         # controller.move_forward()
#         # controller.move_backward()
#         # controller.move_left()
#         # controller.move_right()
#     camera_capture.release()
#     cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
