from DataStructures.makesmithInitFuncs import MakesmithInitFuncs
from Actions.actions import Actions
from DataStructures.logger import Logger
from DataStructures.loggingQueue import LoggingQueue
from Background.watchDog import WatchDog
from Config.config import Config
import queue

class Controller(MakesmithInitFuncs):
    """

    NonVisibleWidgets is a home for widgets which do not have a visible representation like
    the serial connection, but which still need to be tied in to the rest of the program.

    """

    actions = Actions()
    logger = Logger()
    config = Config()
    watchdog = WatchDog()
    ui_queue = queue.Queue()
    message_queue = LoggingQueue(logger)

    def setUpData(self, data):
        """

        The setUpData function is called when a widget is first created to give that widget access
        to the global data object. This should be replaced with a supper classed version of the __init__
        function.

        """

        self.data = data


        self.data.actions = self.actions
        self.data.logger = self.logger
        self.data.config = self.config
        self.data.ui_queue = self.ui_queue
        self.data.message_queue = self.message_queue
        self.data.watchdog = self.watchdog

        self.actions.setUpData(data)
        self.logger.setUpData(data)
        self.config.setUpData(data)
        self.watchdog.setUpData(data)

        self.watchdog.checkForRunningContainer()