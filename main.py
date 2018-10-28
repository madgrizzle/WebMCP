# main.py
from app import app, socketio
from gevent import monkey

monkey.patch_all()

import time
import threading
import json

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
app.Controller = Controller()
app.Controller.setUpData(app.data)
app.UIProcessor = UIProcessor()

@app.route("/")
@mobile_template("{mobile/}")
def index(template):
    # print template
    current_app._get_current_object()
    thread = socketio.start_background_task(
        app.UIProcessor.start, current_app._get_current_object()
    )
    thread.start()
    if template == "mobile/":
        return render_template("frontpage_mobile.html")
    else:
        return render_template("frontpage.html")


@socketio.on("my event", namespace="/MaslowCNC")
def my_event(msg):
    print(msg["data"])

@socketio.on("connect", namespace="/MaslowCNC")
def test_connect():
    print("connected")
    print(request.sid)
    socketio.emit("my response", {"data": "Connected", "count": 0})

@socketio.on("disconnect", namespace="/MaslowCNC")
def test_disconnect():
    print("Client disconnected")

@socketio.on("action", namespace="/MaslowCNC")
def command(msg):
    app.data.actions.processAction(msg)

@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"])  # "my error event"
    print(request.event["args"])  # (data,)1


if __name__ == "__main__":
    app.debug = False
    app.config["SECRET_KEY"] = "secret!"
    socketio.run(app, use_reloader=False, host="0.0.0.0", port=80)
    # socketio.run(app, host='0.0.0.0')
