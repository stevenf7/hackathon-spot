import cv2
import requests
import openai
import base64
from io import BytesIO
from elevenlabs import generate, play, set_api_key

set_api_key("7a4bf4db5d1b7aac0bf08d99951e42e7")

# Initialize the camera
cap = cv2.VideoCapture(0)  # 0 is usually the default camera

voiceID = 'jBpfuIE2acCO8z3wKNLl'

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
else:
    # Capture one frame
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if ret:
        # Convert the image to PNG format (OpenAI API might require specific formats)
        _, buffer = cv2.imencode('.png', frame)
        img_str = base64.b64encode(buffer).decode('utf-8')

        # Make sure to release the camera and close any open windows
        cap.release()
        cv2.destroyAllWindows()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer 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"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What’s in this image?"
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

        # Make sure to release the camera and close any open windows
    cap.release()
    cv2.destroyAllWindows()

def main():
    camera_capture = cv2.VideoCapture(0)
    rv, image = camera_capture.read()
