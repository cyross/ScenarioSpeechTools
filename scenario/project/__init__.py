# -*- coding: utf-8 -*-

import re
import yaml
from scenario.io import *
from scenario.config import Config
from scenario.data.actor import Actor
from scenario.data.engine import Engine

class Project:
    def __init__(self, name):
        self.config = Config()
        self.name = name
        self.io = IO(self.name, self.config)
        self.actor = Actor(self)
        self.engine = Engine(self)

    def is_serifu_file_exists(self):
        return file_exists(self.io.base_serifu_filepath)

    def exists(self):
        return file_exists(self.io.project_dir)
