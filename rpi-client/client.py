import time
import cv2
from roboflow import Roboflow
import os
from dotenv import load_dotenv
from datetime import datetime
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from itertools import islice # for slicing an iterator
from random import uniform
from datetime import datetime


def camera_frame():
    capture = cv2.VideoCapture(0)
    while True:
        time.sleep(0.5)
        success, frame = capture.read()
        if not success:
            break
        success, buf = cv2.imencode(".jpeg", frame)
        buf = buf.tobytes()
        if not success:
            break
        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buf + b"\r\n"
  
def write_frame_to_file(frame, file_path):
    # Extract the image data from the multipart frame
    image_data = frame.split(b"\r\n\r\n")[1].rsplit(b"\r\n", 1)[0]

    with open(file_path, 'wb') as f:
        f.write(image_data)

def fire_detection(frame_path):
    '''
    Detects fire in the frame and creates a POST request to the server with the frame and the prediction result.
    '''
    prediction = model.predict(frame_path).json()
    timestamp = datetime.now()
    if prediction['predictions'][0]['top'] == "fire":
        print("Fire detected")
        mp_encoder = MultipartEncoder(
            fields={
                'confidence': str(prediction['predictions'][0]['confidence']),
                'time': str(timestamp),
                'latitude': str(43.6606491 + uniform(-0.00003, 0.00003)),
                'longitude': str(-79.3964662 + uniform(-0.00003, 0.00003)),
                'temperature': str(100.0),
                'frame': (frame_path, open(frame_path, 'rb'))
            }
        )
        response = requests.post('http://15.222.245.42:80/fire-detected', data=mp_encoder, headers={'Content-Type': mp_encoder.content_type}) 
        if response.status_code != 200:
            print('Failed to send frame: ', response.text)
            return
        print(response.text)
    else:
        print("No fire detected")

if __name__ == '__main__':
    
    load_dotenv()
    ROBOFLOW_KEY = os.getenv('roboflow_key')
    rf = Roboflow(api_key=ROBOFLOW_KEY)
    project = rf.workspace().project("firebot")
    model = project.version(1).model
    last_detection = datetime.now()

    for frame in camera_frame(): # for testing purposes to not use up all allowed inference requests
        frame_path = "live.jpeg"
        write_frame_to_file(frame, frame_path)
        # Add a delay to ensure the file is fully written
        time.sleep(0.5)
        if not os.path.exists(frame_path):
            print("File not found.")
            continue
        file = {'live.jpeg': (frame_path, open(frame_path, 'rb'))}
        # Send the frame to the server at camera endpoint
        response = requests.post('http://15.222.245.42:80/camera', files=file)
        if response.status_code != 200:
                print('Failed to send frame: ', response.__dict__)

        if (datetime.now() - last_detection).total_seconds() > 10:
            last_detection = datetime.now()
            fire_detection(frame_path)
