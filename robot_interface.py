class RobotInterface:
    def sit(self):
        raise NotImplementedError()

    def move(self):
        raise NotImplementedError()

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
