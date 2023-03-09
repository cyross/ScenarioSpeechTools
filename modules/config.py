# -*- coding: utf-8 -*-

from modules import Singleton
from modules.file import load_yaml

class Config(Singleton):
    VERSION = 'version'
    PATH = './config.yaml'
    ENCODE = 'utf-8'

    def __init__(self):
        self.config = load_yaml(self.PATH, self.ENCODE)

    def get(self, key):
        return self.config[key]
