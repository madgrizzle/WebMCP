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
                    if message != "":
                      if message[0:8] == "Message:":
                        if message.find("adjust Z-Axis") != -1:
                            socketio.emit(
                                "requestedSetting",
                                {"setting": "pauseButtonSetting", "value": "Resume"},
                                namespace="/WebMCP",
                            )
                        self.activateModal("Notification:", message[9:])
                      elif message[0:7] == "Action:":
                        if message.find("setAsPause") != -1:
                            socketio.emit(
                                "requestedSetting",
                                {"setting": "pauseButtonSetting", "value": "Pause"},
                                namespace="/MaslowCNC",
                            )
                      elif message[0:6] == "ALARM:":
                        self.activateModal("Notification:", message[7:])
                      elif message == "ok\r\n":
                        pass  # displaying all the 'ok' messages clutters up the display
                      else:
                        print(message)

    def activateModal(self, title, message):
        socketio.emit(
            "activateModal",
            {"title": title, "message": message},
            namespace="/WebMCP",
        )

    def sendControllerMessage(self, message):
        socketio.emit("controllerMessage", {"data": message}, namespace="/WebMCP")


