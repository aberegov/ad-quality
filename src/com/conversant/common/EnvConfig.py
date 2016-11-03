import os

import configparser

class EnvConfig:
    config = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(os.path.normpath(os.path.join(os.path.expanduser("~"), '.env')))

    def get(self, section, key):
        return self.config[section][key]

    def __getattr__(self, section_key):
        path = section_key.split("_")
        return self.get(path[0], path[1])

    def clear(self):
        if self.config is not None:
            self.config.clear()

    def __del__(self):
        self.clear()