from DataStructures.makesmithInitFuncs import MakesmithInitFuncs
import docker
from os import environ
from pathlib import Path
import os

import threading

class Actions(MakesmithInitFuncs):

    home = ""

    def __init__(self):
        self.home = str(Path.home())
        self.hosthome = environ.get('HOST_HOME')

    def testConnect(self):
        th = threading.Thread(target=self.data.watchdog.initialize)
        th.daemon = True
        th.start()
        return True

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
        elif msg["data"]["command"] == "testConnect":
            if not self.testConnect():
                self.data.ui_queue.put("Message: Error with updatingWebControl.")
        elif msg["data"]["command"] == "buildAndUploadFirmware":
            if not self.uploadFirmware():
                self.data.ui_queue.put("Message: Error with building and uploading firmware.")

    def startWebControl(self):
        try:
            if self.data.container == None:
                self.data.ui_queue.put("Start WebControl")
                print("Start WebControl")
                print(self.hosthome)
                self.data.container = self.data.docker.containers.run(image="madgrizzle/webcontrol", ports={5000:5000}, volumes={self.hosthome+'/.WebControl':{'bind':'/root/.WebControl','mode':'rw'}}, privileged=True, detach=True)
                self.data.ui_queue.put("Started WebControl: "+str(self.data.container.short_id))
                print("Started WebControl:"+str(self.data.container.short_id))
                th = threading.Thread(target=self.data.watchdog.initialize)
                th.daemon = True
                th.start()
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
            self.data.ui_queue.put("Updated WebControl")
            return True
        except Exception as e:
            self.data.ui_queue.put(e)
            print(e)
            return False


    def uploadFirmware(self):
        cmd = 'C:/Users/John/.WebControl/Firmware/avrdude -c avrispmkII -p atmega2560 -U eeprom:w:"C:/Users/John/.WebControl/Firmware/cnc_ctrl_v1.ino.eep"'
        try:
            os.system('"'+cmd+'"')
        except Exception as e:
            print(e)
        print("eeprom uploaded")
        cmd = 'C:/Users/John/.WebControl/Firmware/avrdude -v -c avrispmkII -P com5 -b 115200 -p atmega2560 -U flash:w:"\\Users\\John\\.WebControl\\Firmware\\cnc_ctrl_v1.ino.hex"'
        try:
            os.system('"'+cmd+'"')
        except Exception as e:
            print(e)
        print("firmware uploaded")

        return True

