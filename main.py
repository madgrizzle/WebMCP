# main.py
from app import app, socketio
from gevent import monkey

monkey.patch_all()

import time
import threading
import json
import schedule

from flask import Flask, jsonify, render_template, current_app, request, flash
from flask_mobility.decorators import mobile_template
from Background.UIProcessor import UIProcessor
from DataStructures.data import Data
from Controller.controller import Controller
import docker
from os import listdir
from os.path import isfile, join

app.data = Data()
app.data.docker = docker.from_env()
app.data.container = None
app.Controller = Controller()
app.Controller.setUpData(app.data)
app.UIProcessor = UIProcessor()

def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)

app.th = threading.Thread(target=run_schedule)
app.th.daemon = True
app.th.start()

app.uithread = None


@app.route("/")
@mobile_template("{mobile/}")
def index(template):
    # print template
    if template == "mobile/":
        return render_template("frontpage_mobile.html")
    else:
        return render_template("frontpage.html")


@socketio.on("my event", namespace="/WebMCP")
def my_event(msg):
    print(msg["data"])

@socketio.on("connect", namespace="/WebMCP")
def test_connect():
    print("connected")
    print(request.sid)
    if app.uithread == None:
        app.uithread = socketio.start_background_task(
            app.UIProcessor.start, current_app._get_current_object()
        )
        app.uithread.start()

    socketio.emit("my response", {"data": "Connected", "count": 0})

@socketio.on("disconnect", namespace="/WebMCP")
def test_disconnect():
    print("Client disconnected")

@socketio.on("action", namespace="/WebMCP")
def command(msg):
    app.data.actions.processAction(msg)

@socketio.on("checkIn", namespace="/WebMCP")
def checkIn():
    print("received checkIn")
    app.data.checkedIn = time.time()

@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"])  # "my error event"
    print(request.event["args"])  # (data,)1

def run_server():
    app.debug = False
    app.config["SECRET_KEY"] = "secret!"
    socketio.run(app, use_reloader=False, host="0.0.0.0", port=5001)
    # socketio.run(app, host='0.0.0.0')

if __name__ == "__main__":
    socketio.start_background_task(run_server)
    while True:
        time.sleep(1)
