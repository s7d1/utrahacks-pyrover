from flask import Flask, Response, render_template


app = Flask(__name__)


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/alert/<int:id>")
def alert_page(id):
    return render_template("alert.html")


@app.route("/camera")
def camera():
    return Response(, mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/fire-detected", methods=['POST'])
def fire():
    pass  # Replace with the actual method to receive the POST request
