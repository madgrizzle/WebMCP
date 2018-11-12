from __main__ import socketio

import time
import math
import json


class UIProcessor:

    app = None

    def start(self, _app):

        self.app = _app
        with self.app.app_context():
            while True:
                time.sleep(0.001)
                while (
                    not self.app.data.ui_queue.empty()
                ):  # if there is new data to be read
                    message = self.app.data.ui_queue.get()
                    # send message to web for display in appropriate column
                    #print(message)
                    if message != "":
                      if message[0:8] == "Message:":
                        socketio.emit("webcontrolMessage", {"data":message[8:]}, namespace="/WebMCP")
                      elif message[0:7] == "Action:":
                        if message.find("setAsPause") != -1:
                            socketio.emit(
                                "requestedSetting",
                                {"setting": "pauseButtonSetting", "value": "Pause"},
                                namespace="/MaslowCNC",
                            )
                        if message.find("webControlStatus") != -1:
                            msg = message.split("_")
                            socketio.emit("webControlStatus", msg[1], namespace="/WebMCP")
                        if message.find("webControlResponsivenessStatus") != -1:
                            msg = message.split("_")
                            socketio.emit("webControlResponsivenessStatus", msg[1], namespace="/WebMCP")
                        if message.find("requestCheckIn") != -1:
                            socketio.emit("checkInRequested", 'checkInPlease', namespace="/WebMCP", broadcast=True)
                        #if message.find("connectToWebControl") != -1:
                        #    socketio.connect("http://127.0.0.1:5000/WebMCP")
                      elif message[0:6] == "ALARM:":
                        self.activateModal("Notification:", message[7:])
                      elif message == "ok\r\n":
                        pass  # displaying all the 'ok' messages clutters up the display
                      else:
                        #print("UIProcessor:"+message)
                        self.sendUIMessage(message)

    def activateModal(self, title, message):
        socketio.emit(
            "activateModal",
            {"title": title, "message": message},
            namespace="/WebMCP",
        )

    def sendUIMessage(self, message):
        socketio.emit("uiMessage", {"data": message}, namespace="/WebMCP")


