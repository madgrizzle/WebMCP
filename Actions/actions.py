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
                self.data.ui_queue.put("error")
                self.data.ui_queue.put("Message: Error with starting WebControl.")
        elif msg["data"]["command"] == "stopWebControl":
            if not self.stopWebControl():
                self.data.ui_queue.put("Message: Error with stopping WebControl.")
        elif msg["data"]["command"] == "updateWebControl":
            if not self.updateWebControl():
                self.data.ui_queue.put("Message: Error with updatingWebControl.")

    def startWebControl(self):
        try:
            self.data.ui_queue.put("Start WebControl")
            print("Start WebControl")
            self.data.container = self.data.docker.containers.run(image="madgrizzle/webcontrol", ports={5000:5000}, volumes={self.home+'/.WebControl':{'bind':'/root/.WebControl','mode':'rw'}}, privileged=True, detach=True)
            self.data.ui_queue.put("Started WebControl: "+str(self.data.container.short_id))
            print("Started WebControl:"+str(self.data.container.short_id))
            return True
        except Exception as e:
            self.data.ui_queue.put(e)
            print(e)
            return False

    def stopWebControl(self):
        try:
            self.data.ui_queue.put("Stop WebControl:"+str(self.data.container.short_id))
            print("Stop WebControl:"+str(self.data.container.short_id))
            self.data.container.stop()
            self.data.container = None
            self.data.ui_queue.put("Stopped WebControl")
            print("Stopped WebControl")
            return True
        except Exception as e:
            self.data.ui_queue.put(e)
            print(e)
            return False

    def updateWebControl(self):
        try:
            self.data.ui_queue.put("Update WebControl")
            print("Update WebControl")
            if self.data.container!= None:
                if not self.stopWebControl():
                    return False
            self.data.ui_queue.put("Pull WebControl")
            print("Pull WebControl")
            image = self.data.docker.images.pull("madgrizzle/webcontrol","latest")
            self.data.ui_queue.put("Pulled WebControl:"+str(image.short_id))
            print("Pulled WebControl:"+str(image.short_id))
            return True
        except Exception as e:
            self.data.ui_queue.put(e)
            print(e)
            return False
