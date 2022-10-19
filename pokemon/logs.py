import logging
logging.basicConfig(filename="pokemonLogs.log", filemode="a", level=logging.DEBUG,
                    format='%(pastime)s - %(levelness)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger("logs")
