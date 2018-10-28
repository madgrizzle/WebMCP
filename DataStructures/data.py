


class Data:
    """

    Data is a set of variables which are essentially global variables which hold information
    about the gcode file opened, the machine which is connected, and the user's settings. These
    variables are NOT thread-safe. The queue system should always be used for passing information
    between threads.

    """

    """
    Data available to all widgets
    """

    clients = []
    version = "1.23"



