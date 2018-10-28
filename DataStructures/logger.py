"""

This module provides a logger which can be used to record and later report the machine's
behavior.

"""

from DataStructures.makesmithInitFuncs import MakesmithInitFuncs
import threading


class Logger(MakesmithInitFuncs):

    messageBuffer = ""

    # clear the old log file
    with open("log.txt", "a") as logFile:
        logFile.truncate()

    def writeToLog(self, message):

        self.messageBuffer = self.messageBuffer + message

        if len(self.messageBuffer) > 0:
            t = threading.Thread(
                target=self.writeToFile, args=(self.messageBuffer, True, "write")
            )
            t.daemon = True
            t.start()
            self.messageBuffer = ""

    def writeToFile(self, toWrite, log, *args):
        """
        Write to the log file
        """
        if log is True:
            with open("WebMCP.log", "a") as logFile:
                logFile.write(toWrite)
        return

