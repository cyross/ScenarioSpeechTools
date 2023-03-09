# -*- coding: utf-8 -*-

from scenario.io import *
from scenario.config import Config
from scenario.master.actor import Actor
from scenario.master.engine import Engine

class Project:
    def __init__(self, name):
        self.config = Config.instance()
        self.name = name
        self.io = IO(self.name, self.config)
        self.actor = Actor.instance(self)
        self.engine = Engine.instance(self)

    def is_serifu_file_exists(self):
        return file_exists(self.io.base_serifu_filepath)

    def exists(self):
        return file_exists(self.io.project_dir)

    def projects_exists(self):
        return file_exists(self.io.base_dir)

    def create_projects_dir(self):
        if not self.projects_exists():
            make_dir(self.io.base_dir)
