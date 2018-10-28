from DataStructures.makesmithInitFuncs import MakesmithInitFuncs
import docker

class Actions(MakesmithInitFuncs):
    def processAction(self, msg):
        if msg["data"]["command"] == "startWebControl":
            if not self.startWebControl():
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
            self.data.docker.containers.run("-it -v $HOME/.WebControl:/root/.WebControl -p 5000:5000 --privileged madgrizzle/webcontrol")
            return True
        except Exception as e:
            print(e)
            return False

    def stopWebControl(self):
        try:
            print("Stop WebControl")
            return True
        except Exception as e:
            print(e)
            return False

    def updateWebControl(self):
        try:
            print("Update WebControl")
            return True
        except Exception as e:
            print(e)
            return False
