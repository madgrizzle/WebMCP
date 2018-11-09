
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
    th1 = None

    def initialize(self):
        print("Initializing WatchDog")
        self.client = socketio_client('192.168.1.69',  5000)
        print("1")
        self.namespace = self.client.define(WatchDogNamespace, '/WebMCP')
        print("2")
        self.namespace.setUpData(self.data)
        print("3")
        self.namespace.on('connect', self.on_connect)
        self.namespace.on('disconnect', self.on_disconnect)
        self.namespace.on('error', self.on_error)
        self.namespace.on('connect_error', self.on_connect_error())
        print("Scheduling checkins")
        schedule.every(5).seconds.do(self.requestCheckIn)
        print("Threading monitor of checkins")
        self.th = threading.Thread(target=self.monitorCheckIn)
        self.th.daemon = True
        self.th.start()
        print("Threaded")

        print("Threading monitor of container")
        self.th1 = threading.Thread(target=self.monitorContainer)
        self.th1.daemon = True
        self.th1.start()
        print("Threaded")


    def monitorContainer(self):
        while True:
            try:
                if self.data.container!=None:
                    if self.data.container.status=='created':
                        self.data.ui_queue.put("Action: webControlStatus:_" + json.dumps({'status': 'running'}))
                    else: 
                        self.data.ui_queue.put("Action: webControlStatus:_" + json.dumps({'status': 'notRunning'}))
                else:
                    self.data.ui_queue.put("Action: webControlStatus:_" + json.dumps({'status': 'notRunning'}))
                    self.data.ui_queue.put("Action: webControlResponsivenessStatus_" + json.dumps({"status": "nonresponsive"}))
            except ConnectionError:
                print('The server is down. Try again later.')
            time.sleep(5)

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



