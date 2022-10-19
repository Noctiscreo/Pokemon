import logging


def clearLogs():
    with open('pokemonLogs.log', 'w'):
        pass


class Logger(object):
    _instance = None

    def __init__(self):
        self.logger = logging.getLogger()

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Logger, cls).__new__(cls)
            logging.basicConfig(filename="pokemonLogs.log", filemode="a", level=logging.DEBUG,
                                format='%(asctime)s - %(levelname)s: %(message)s [%(filename)s:%(lineno)s - %(funcName)20s() ]', datefmt='%m/%d/%Y %I:%M:%S %p')
        return cls._instance
