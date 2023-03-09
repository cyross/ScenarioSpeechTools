# -*- coding: utf-8 -*-

from scenario.file.serifu import Serifu

# SEPARATED SERIFU FILE
class SepSerifu(Serifu):
    def __init__(self, project, key, engine, actor):
        self.key = key
        self.engine_name = engine
        self.actor_name = actor

        filepath = project.io.serifu_file_path(self.key)
        encode = project.config.get(Serifu.ENCODING)[self.engine_name]

        super().__init__(project, filepath, encode)

        self.separator = self.engine.separator(self.engine_name)

    def write(self, serifu):
        if self.engine.is_sep(self.engine_name):
            self.stream.write(f'{serifu}\n')
        else:
            self.stream.write(f'{self.actor_name}{self.separator}{serifu}\n')
