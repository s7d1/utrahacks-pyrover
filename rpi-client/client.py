import time
import cv2
from roboflow import Roboflow
import os
from dotenv import load_dotenv


load_dotenv()
ROBOFLOW_KEY = os.getenv('roboflow_key')

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


rf = Roboflow(api_key=ROBOFLOW_KEY)
project = rf.workspace().project("firebot")
model = project.version(1).model

def fire_detection():
    '''
    Detects fire in the frame and creates a POST request to the server with the frame and the prediction result.
    '''
    for frame in camera_frame():
        write_frame_to_file(frame, "frame.jpeg")
        
        # Check if the file is written and is a valid image file
        if not os.path.exists("frame.jpeg"):
            print("File not found.")
            continue

        # Add a delay to ensure the file is fully written
        time.sleep(1)

        prediction = model.predict("frame.jpeg").json()
        if prediction['predictions'][0]['top'] == "fire":
            post_obj = {'confidence' : prediction['predictions'][0]['confidence'], 'time' : prediction['predictions'][0]['time']}
            
            return post_obj # change this to post the object on ec2 instance along with image.
        else:
            return "No fire detected"

print(fire_detection())
