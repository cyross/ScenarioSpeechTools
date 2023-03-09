# -*- coding: utf-8 -*-

from modules.master import Data

# VOICE ENGINE
class Engine(Data):
    YAML_PATH = './engine.yaml'
    YAML_ENCODING = 'utf-8'

    SPEC_REAL_NAME = 'real_name'
    SPEC_SEP = 'separator'
    SEP_E = 'separate_actor_engines'
    NONE_E = 'none_voice_engines'

    NONE = 'NONE'
    OTHER = 'OTHER'

    def __init__(self, project):
        super().__init__(project, self.YAML_PATH, self.YAML_ENCODING)
        self.sep_engine = self.data[self.SEP_E]
        self.none_engine = self.data[self.NONE_E]

    def real_name(self, engine: str) -> str:
        return self.spec[engine][self.REAL_NAME]

    def separator(self, engine: str) -> str:
        return self.spec[engine][self.SPEC_SEP]

    def is_sep(self, engine: str) -> str:
        return engine in self.sep_engine

    def is_none(self, engine: str) -> str:
        return engine in self.none_engine
