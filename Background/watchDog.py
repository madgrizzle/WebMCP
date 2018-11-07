
from DataStructures.makesmithInitFuncs import MakesmithInitFuncs
from socketIO_client import SocketIO as socketio_client, BaseNamespace
import schedule
import time
import json
import threading


class WatchDogNamespace(BaseNamespace, MakesmithInitFuncs):

    def on_connect(self, *args):
        print("connected")

    def on_reconnect(self, *args):
        print("reconnected")

    def on_checkIn(self, *args):
        self.data.checkedIn = time.time()


class WatchDog(MakesmithInitFuncs):

    client = None
    data = None
    namespace = None
    th = None

    def initialize(self):
        self.client = socketio_client('127.0.0.1', 5000)
        self.namespace = self.client.define(WatchDogNamespace, '/WebMCP')
        self.namespace.setUpData(self.data)
        self.namespace.on('connect', self.on_connect)
        self.namespace.on('disconnect', self.on_disconnect)
        self.namespace.on('error', self.on_error)
        self.namespace.on('connect_error', self.on_connect_error())
        schedule.every(5).seconds.do(self.requestCheckIn)

        self.th = threading.Thread(target=self.monitorCheckIn)
        self.th.daemon = True
        self.th.start()


    def requestCheckIn(self):
        try:
            self.namespace.emit('checkInRequested')
            self.client.wait(seconds=1)
        except ConnectionError:
            print('The server is down. Try again later.')

    def monitorCheckIn(self):
        while True:
            try:
                t = time.time()-self.data.checkedIn
                if t > 5:
                    status = "nonresponsive"
                else:
                    status = "responsive"
                print(status)
                self.data.ui_queue.put("Action: webControlResponsivenessStatus_" + json.dumps({"status": status}))

            except Exception as e:
                print(e)

            time.sleep(5)

    def on_error(self, *args):
        print("wd:error")

    def on_connect_error(self, *args):
        print("wd:connect_error")
        print(args)

    def on_connect(self, *args):
        print("wd:connect")

    def on_disconnect(self, *args):
        print("wd:disconnect")



