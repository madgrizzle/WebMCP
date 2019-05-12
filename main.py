# main.py
from app import app, socketio
from gevent import monkey

monkey.patch_all()

import time
import threading
import json
import schedule
import sys

from flask import Flask, jsonify, render_template, current_app, request, flash
from flask_mobility.decorators import mobile_template
from Background.UIProcessor import UIProcessor
from DataStructures.data import Data
from Controller.controller import Controller
from WebPageProcessor.webPageProcessor import WebPageProcessor
from Background.gracefulKiller import GracefulKiller

import docker
from os import listdir
from os.path import isfile, join
#import socket

app.data = Data()
app.data.docker = docker.from_env()
app.data.container = None
app.Controller = Controller()
app.Controller.setUpData(app.data)
app.UIProcessor = UIProcessor()
app.webPageProcessor = WebPageProcessor(app.data)
app.data.actions.autoStart()

#app.host = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]


def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)

app.th = threading.Thread(target=run_schedule)
app.th.daemon = True
app.th.start()

app.uithread = None

#def monitorKillSignal():
#    while True:
#       if app.killer.kill_now:
#           print("kill app")
#           app.data.actions.stopWebControl()
#           print("back")
#           return
#       time.sleep(0.01)

#app.th3 = threading.Thread(target=monitorKillSignal)
#app.th3.daemon = True
#app.th3.start()




@app.route("/")
@mobile_template("{mobile/}")
def index(template):
    # print template
    if template == "mobile/":
        return render_template("frontpage_mobile.html")
    else:
        return render_template("frontpage.html")


@app.route("/webMCPSettings", methods=["POST"])
def maslowSettings():
    if request.method == "POST":
        result = request.form
        app.data.config.updateSettings("WebMCP Settings", result)
        message = {"status": 200}
        resp = jsonify(message)
        resp.status_code = 200
        return resp


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
    try:
        app.data.actions.processAction(msg)
    except Exception as e:
        self.data.ui_queue.put(e)
        print(e)


@socketio.on("checkIn", namespace="/WebMCP")
def checkIn():
    print("received checkIn")
    app.data.checkedIn = time.time()
    
    
@socketio.on("shutdown", namespace="/WebMCP")
def shutdown():
    print("shutting down")
    app.data.actions.shutdown()

@socketio.on("message", namespace="/WebMCP")
def on_message(msg):
    print("here")
    print(msg)
    print(msg["command"])


@socketio.on("requestPage", namespace="/WebMCP")
def requestPage(msg):
    print(msg)
    try:
        page, title, isStatic, modalSize, modalType, resume = app.webPageProcessor.createWebPage(msg["data"]["page"],msg["data"]["isMobile"], msg["data"]["args"])
        data = json.dumps({"title": title, "message": page, "isStatic": isStatic, "modalSize": modalSize, "modalType": modalType, "resume":resume})
        socketio.emit("message", {"command": "activateModal", "data": data, "dataFormat": "json"},
            namespace="/WebMCP",
        )
    except Exception as e:
        print(e)

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
