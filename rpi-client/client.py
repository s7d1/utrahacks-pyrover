import time
import cv2
import base64
import requests
from roboflow import Roboflow
import os
from dotenv import load_dotenv
from datetime import datetime
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from itertools import islice # for slicing an iterator

def camera_frame(model):
    capture = cv2.VideoCapture(0)
    while True:
        time.sleep(0.5)
        success, frame = capture.read()
        img_dims = (frame.shape[0], frame.shape[1])
        if not success:
            break
        success, buf = cv2.imencode(".jpeg", frame)
        buf = buf.tobytes()
        if not success:
            break
        data = b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + buf + b"\r\n"
        data = data.split(b"\r\n\r\n")[1].rsplit(b"\r\n", 1)[0]
        data = base64.b64encode(data)
        data = data.decode("ascii")
        resp = requests.post(
            model.api_url,
            data = data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        if resp.status_code == 200:
            yield resp.json(), data        

def fire_detection(prediction, frame):
    '''
    Detects fire in the frame and creates a POST request to the server with the frame and the prediction result.
    '''
    timestamp = datetime.now()
    if prediction['top'] == "fire":
        print("Fire detected")
        mp_encoder = MultipartEncoder(
            fields={
                'confidence': str(prediction['confidence']),
                'time': str(timestamp),
                'location': ("Latitude, Longitude"),
                'frame': ("Frame", frame)
            }
        )
        response = requests.post('http://15-222-245-42:80/fire', data=mp_encoder, headers={'Content-Type': mp_encoder.content_type}) 
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
    
    for prediction, data in islice(camera_frame(model), 1): # for testing purposes to not use up all allowed inference requests
        # Add a delay to ensure the file is fully written
        time.sleep(0.5)
        
        # Send the frame to the server at camera endpoint
        response = requests.post('http://15-222-245-42:80/camera', data=data)
        if response.status_code != 200:
                print('Failed to send frame: ', response.text)

        fire_detection(frame)
