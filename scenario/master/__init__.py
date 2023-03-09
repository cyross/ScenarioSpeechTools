# -*- coding: utf-8 -*-

from scenario import Base, Singleton
from scenario.file import load_yaml

# DATA BASE
class Data(Base, Singleton):
    SPEC = 'spec'
    SANITIZE_RE = 'sanitize_regexp'

    def __init__(self, project, yaml_filename: str, yaml_encoding: str):
        super().__init__(project)
        self.data = load_yaml(yaml_filename, yaml_encoding)
        self.spec = self.data[self.SPEC]
        self.sanitize_re = self.data[self.SANITIZE_RE]
        self.names: list[str] = self.spec.keys()

    def get(self, key: str) -> any:
        return self.spec[key]
