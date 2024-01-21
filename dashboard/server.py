from flask import Flask, Response, render_template, request
import time
from werkzeug.datastructures import FileStorage



app = Flask(__name__)
live_frame = None
alerts = [{
    "id": 0,
    "confidence": 0.99,
    "time": "2024-01-20 20:54:41.786741",
    "position": [43.6607378, -79.396058],
    "temperature": 100.0,
    "file_path": "/static/fire/0.jpeg"
}]


@app.route("/")
def index_page():
    return render_template("index.html", alerts=alerts)


@app.route("/alert/<int:id>")
def alert_page(id):
    return render_template("alert.html", alert=alerts[id])


def gen_frames():
    global live_frame
    while True:
        if live_frame:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + live_frame + b"\r\n"
        else:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
        time.sleep(0.2)


def save_frame(buf):
    global live_frame
    live_frame = buf


@app.route("/camera", methods=["GET", "POST"])
def camera():
    global live_frame
    if request.method == "GET":
       return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")
    elif request.method == "POST":
        save_frame(request.files["live.jpeg"].read())
        return ""


@app.route("/fire-detected", methods=['POST'])
def fire():
    global alerts

    # Access form data
    confidence = request.form.get('confidence')
    time = request.form.get('time')
    position = request.form.get('position')
    temperature = request.form.get('temperature')
    
    # Access the file
    frame = request.files.get('frame')
    id = get_id()
    if frame and isinstance(frame, FileStorage):
        frame.save("./static/fire/" + str(id) + ".jpeg")
    alerts.append({
        "id": id,
        "confidence": confidence,
        "time": time,
        "position": position,
        "temperature": temperature,
        "file_path": "/static/fire/" + str(id) + ".jpeg"
    })
    return "Alert received"


def get_id():
    global alerts
    return len(alerts)
