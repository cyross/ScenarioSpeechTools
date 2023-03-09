# -*- coding: utf-8 -*-

from scenario.file.jimaku import Jimaku

# RAW JIMAKU FILE
class RawJimaku(Jimaku):
    def __init__(self, project):
        filepath = project.io.raw_jimaku_filepath
        encoding = project.config.get(Jimaku.ENCODING)[Jimaku.ENCODE]
        super().__init__(project, filepath, encoding)

    def write(self, actor, jimaku):
        self.stream.write(f'{actor}:{jimaku}\n')
