import json


class Configuration:

    def __init__(self):
        # TODO add a dynamic path instead of 'config/config.json' to file config.json so that the script could be run
        # from any directory and not just from scc/scc
        with open('config/config.json', 'r') as config_file:
            self.config = json.load(config_file)
