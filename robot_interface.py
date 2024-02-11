import os
import time
from spot_controller import SpotController
import cv2
import requests
import openai
import base64
from io import BytesIO
from elevenlabs import generate, play, set_api_key

ROBOT_IP = "192.168.50.3"#os.environ['ROBOT_IP']
SPOT_USERNAME = "admin"#os.environ['SPOT_USERNAME']
SPOT_PASSWORD = "2zqa8dgw7lor"#os.environ['SPOT_PASSWORD']


class RobotInterface:
    def __init__(self, spot):
        self.spot = spot

    def dance(self):
        for i in range(3):
            self.spot.bow(-1)

        # Move head to specified positions with intermediate time.sleep
        self.spot.move_head_in_points(yaws=[0.2, 0],
                                 pitches=[0.3, 0],
                                 rolls=[0.4, 0],
                                 sleep_after_point_reached=1)

        self.spot.move_head_in_points(yaws=[-0.2, 0],
                                 pitches=[-0.3, 0],
                                 rolls=[-0.4, 0],
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
        self.spot.move_to_goal(goal_x=0, goal_y=0.5)
        time.sleep(1)

    def move_right(self):
        self.spot.move_to_goal(goal_x=0, goal_y=-0.5)
        time.sleep(1)

    def describe_env(self, cap):
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        if ret:
            # Convert the image to PNG format (OpenAI API might require specific formats)
            _, buffer = cv2.imencode('.png', frame)
            img_str = base64.b64encode(buffer).decode('utf-8')


            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.environ['openai']}"
            }

            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "What’s in this image in 15 words or less?"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_str}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            content = response.json()['choices'][0]['message']['content']

            print(response.json()['choices'][0]['message']['content'])




            audio = generate(
                    text=f"{content}",
                    voice="Gigi",
                    model="eleven_multilingual_v1"
            )
            play(audio)
        else:
                print("Error: Could not capture an image.")


