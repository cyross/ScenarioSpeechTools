# -*- coding: utf-8 -*-

import re
from scenario.master import Data
from scenario.master.engine import Engine

# VOICE ACTOR
class Actor(Data):
    YAML_PATH = './actor.yaml'
    YAML_ENCODING = 'utf-8'

    NONE_NAME = '[なし]'
    OPEN_ATTR = '['
    CLOSE_ATTR = ']'

    def __init__(self, project):
        super().__init__(project, self.YAML_PATH, self.YAML_ENCODING)

    def sanitize(self, name):
        return re.sub(self.sanitize_re, '_', name)

    def first_name(self, index: int = 0) -> str:
        return list(self.names)[index]

    def has(self, name: str) -> bool:
        return name in self.names

    def engine(self, name: str) -> str:
        return self.get(name) if self.has(name) else Engine.OTHER

    def has_attr(self, name: str) -> bool:
        return name[0] == self.OPEN_ATTR

    def real_name(self, name):
        if name == self.NONE_NAME or not self.has_attr(name):
            return name

        pos = name.find(self.CLOSE_ATTR)
        return name[pos+1:]
