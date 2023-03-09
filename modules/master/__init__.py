# -*- coding: utf-8 -*-

from modules import Base, Singleton
from modules.file import load_yaml

# DATA BASE
class Data(Base, Singleton):
    SPEC = 'spec'
    SPEC_NAME = 'name'
    SANITIZE_RE = 'sanitize_regexp'
    PATTERN = 'pattern'
    SUB = 'sub'

    def __init__(self, project, yaml_filename: str, yaml_encoding: str):
        super().__init__(project)
        self.data = load_yaml(yaml_filename, yaml_encoding)
        self.spec_list = self.data[self.SPEC]
        self.spec = self._to_dict()
        self.sanitizer = self.data[self.SANITIZE_RE]
        self.names: list[str] = self.spec.keys()

    def get(self, key: str) -> any:
        return self.spec[key]

    def _to_dict(self):
        d = {}
        for spec in self.spec_list:
            d[spec[self.SPEC_NAME]] = spec
        return d
