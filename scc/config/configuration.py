import json
import pathlib
from config.app_logger import AppLogger

_CURRENT_PATH = str(pathlib.Path(__file__).resolve().parent)   # can also do: os.path.dirname(os.path.abspath(__file__))


class Configuration:

    logger = AppLogger(__name__, AppLogger.DEBUG).logger

    def __init__(self):
        # TODO add a dynamic path instead of 'config/config.json' to file config.json so that the script could be run
        # from any directory and not just from scc/scc
        Configuration.logger.info('Loading config file...')
        with open(_CURRENT_PATH + '/config.json', 'r') as config_file:
            self.config = json.load(config_file)
        Configuration.logger.info('Config file loaded')
