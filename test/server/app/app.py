from flask import Flask
import time

app = Flask(__name__)


@app.route("/sleep")
def index():
    time.sleep(1)
    return "I have awoken"