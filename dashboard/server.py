from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/alert/<int:id>")
def alert_page(id):
    return render_template("alert.html")
