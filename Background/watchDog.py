
from DataStructures.makesmithInitFuncs import MakesmithInitFuncs
from socketIO_client import SocketIO as socketio_client, BaseNamespace
import schedule
import Background.gracefulKiller
import time
import json
import threading
import docker

class WatchDogNamespace(BaseNamespace, MakesmithInitFuncs):

    data = None

    def on_connect(self, *args):
        print("connected")

    def on_reconnect(self, *args):
        print("reconnected")

    def on_checkIn(self, *args):
        #print("checked in")
        self.data.checkedIn = time.time()
        
    def on_shutdown(self, *args):
        print("shutdown received")
        self.data.actions.shutdown()

    def on_webcontrolMessage(self, *args):
        if self.data is not None:
            try:
                self.data.ui_queue.put("Message:"+args[0]["data"])
            except Exception as e:
                print(e)
                print(args[0]["data"])


class WatchDog(MakesmithInitFuncs):

    client = None
    data = None
    namespace = None
    th = None
    th1 = None
    stopped = False


    def checkForRunningContainer(self):
        list = self.data.docker.containers.list()
        print(list)

    def initialize(self):
        print("Initializing WatchDog")
        self.client = socketio_client('127.0.0.1',  5000)
        self.namespace = self.client.define(WatchDogNamespace, '/WebMCP')
        self.namespace.setUpData(self.data)
        self.namespace.on('connect', self.on_connect)
        self.namespace.on('disconnect', self.on_disconnect)
        self.namespace.on('error', self.on_error)
        self.namespace.on('connect_error', self.on_connect_error)
        #self.namespace.on('webcontrolMessage', self.on_webcontrolMessage)

        self.stopped = False
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

        print("Threading socketio wait")
        self.th2 = threading.Thread(target=self._receive_events_thread)
        self.th2.daemon = True
        self.th2.start()
        print("Threaded")


    def _receive_events_thread(self):
        while True:
            self.client.wait(seconds = 1)
            if self.stopped:
                return
            time.sleep(0.01)


    def stop(self):
        self.stopped = True
        
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

            if self.stopped:
                return

            time.sleep(5)

    def requestCheckIn(self):
        try:
            self.namespace.emit('checkInRequested')
        except ConnectionError:
            print('The server is down. Try again later.')

    def monitorCheckIn(self):
        while True:
            try:
                t = time.time()-self.data.checkedIn
                if t > 7:
                    status = "nonresponsive"
                else:
                    status = "responsive"
                self.data.ui_queue.put("Action: webControlResponsivenessStatus_" + json.dumps({"status": status}))

            except Exception as e:
                print(e)

            if self.stopped:
                return

            time.sleep(2)

    def on_error(self, *args):
        print("wd:error")

    def on_connect_error(self, *args):
        print("wd:connect_error")
        print(args)

    def on_connect(self, *args):
        print("wd:connect")

    def on_disconnect(self, *args):
        print("wd:disconnect")

    #def on_webcontrolMessage(self, *args):
    #   self.data.ui_queue.put("Message:"+args[0]["data"])


