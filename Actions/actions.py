from DataStructures.makesmithInitFuncs import MakesmithInitFuncs
import docker
from pathlib import Path

class Actions(MakesmithInitFuncs):

    home = ""

    def __init__(self):
        self.home = str(Path.home())

    def processAction(self, msg):
        if msg["data"]["command"] == "startWebControl":
            if not self.startWebControl():
                print("error")
                self.data.ui_queue.put("Message: Error with starting WebControl.")
        elif msg["data"]["command"] == "stopWebControl":
            if not self.stopWebControl():
                self.data.ui_queue.put("Message: Error with stopping WebControl.")
        elif msg["data"]["command"] == "updateWebControl":
            if not self.updateWebControl():
                self.data.ui_queue.put("Message: Error with updatingWebControl.")

    def startWebControl(self):
        try:
            print("Start WebControl")
            self.data.container = self.data.docker.containers.run(image="madgrizzle/webcontrol", ports={5000:5000}, volumes={self.home+'/.WebControl':{'bind':'/root/.WebControl','mode':'rw'}}, privileged=True, detach=True)
            print("Started WebControl:"+str(self.data.container))
            return True
        except Exception as e:
            print(e)
            return False

    def stopWebControl(self):
        try:
            print("Stop WebControl:"+str(self.data.container))
            self.data.container.stop()
            self.data.container = None
            print("Stopped WebControl")
            return True
        except Exception as e:
            print(e)
            return False

    def updateWebControl(self):
        try:
            print("Update WebControl")
            if self.data.container!= None:
                if not self.stopWebControl():
                    return False
            print("Pull WebControl")
            image = self.data.docker.images.pull("madgrizzle/webcontrol","latest")
            print("Pulled WebControl:"+str(image))
            return True
        except Exception as e:
            print(e)
            return False
