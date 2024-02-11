import os
import time
from spot_controller import SpotController

ROBOT_IP = "192.168.50.3"#os.environ['ROBOT_IP']
SPOT_USERNAME = "admin"#os.environ['SPOT_USERNAME']
SPOT_PASSWORD = "2zqa8dgw7lor"#os.environ['SPOT_PASSWORD']


class RobotInterface:
    def __init__(self):
        self.spot = SpotController(SPOT_USERNAME, SPOT_PASSWORD, ROBOT_IP)

    def dance(self):
        for i in range(3):
            self.spot.bow(-1)
            time.sleep(1)
            self.spot.bow(1)
            time.sleep(1)

        # Move head to specified positions with intermediate time.sleep
        self.spot.move_head_in_points(yaws=[0.2, 0],
                                 pitches=[0.3, 0],
                                 rolls=[0.4, 0],
                                 sleep_after_point_reached=1)
        time.sleep(1)


    def sit(self):
        self.spot.move_head_in_points(yaws=[0], pitches=[0], rolls=[0])
        time.sleep(1)

    def stand(self):
        self.spot.stand_at_height(1)
        time.sleep(1)

    def move_forward(self):
        self.spot.move_to_goal(goal_x=0.5, goal_y=0)
        time.sleep(1)

    def move_backward(self):
        self.spot.move_to_goal(goal_x=-0.5, goal_y=0)
        time.sleep(1)

    def move_left(self):
        self.spot.move_to_goal(goal_x=0, goal_y=-0.5)
        time.sleep(1)

    def move_right(self):
        self.spot.move_to_goal(goal_x=0, goal_y=0.5)
        time.sleep(1)

    def describe_env(self):
        raise NotImplementedError()


class MockRobot(RobotInterface):
    def sit(self):
        print("sit")

    def move(self):
        print("move")

    def describe_env(self):
        print("describe_env")


class SpotRobot(RobotInterface):
    def sit(self):
        print("sit")

    def move(self):
        print("move")

    def describe_env(self):
        print("describe_env")
