# -*- coding: utf-8 -*-

import re
from modules.file import File

# SERIFU FILE
class Serifu(File):
    ENCODE = 'serifu'

    def __init__(self, project, file_path = None, file_encode = None):
        path = file_path if file_path is not None else project.io.base_serifu_filepath
        encode = file_encode if file_encode is not None else project.config.get(File.ENCODING)[self.ENCODE]

        super().__init__(project, path, encode)

        self.engine = self.project.engine

    def sanitize(self, serifu, engine):
        if not engine in self.engine.sanitizer.keys():
            return serifu

        for s_pair in self.engine.sanitizer[engine]:
            serifu = re.sub(s_pair[self.RE], s_pair[self.SUB], serifu)

        return serifu

    def pair(self, line, actor):
        pair = line.split(',', maxsplit=1)  # 声優名だけを分離

        if len(pair) == 1:
            return [actor, line]

        return pair
