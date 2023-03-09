# -*- coding: utf-8 -*-

import re
from scenario.file import File

# SERIFU FILE
class Serifu(File):
    RE = 'regexp'
    SUB = 'sub'
    ENCODE = 'serifu'

    def __init__(self, project, file_path = None, file_encode = None):
        path = file_path if file_path is not None else project.io.base_serifu_filepath
        encode = file_encode if file_encode is not None else project.config.get(File.ENCODING)[self.ENCODE]

        super().__init__(project, path, encode)

        self.actor = self.project.actor
        self.engine = self.project.engine
        self.sanitizer: dict[str, dict[str, any]] = self._generate_sanitizer()

    def _generate_sanitizer(self):
        sanitize_regexp = self.engine.sanitize_re
        regexp = {}

        for key in sanitize_regexp.keys():
            regexp[key] = []
            sanitize_pats = sanitize_regexp[key]
            for pattern in sanitize_pats.keys():
                regexp[key].append(
                    {
                        self.RE: re.compile(pattern),
                        self.SUB: sanitize_pats[pattern]
                    }
                )

        return regexp

    def sanitize(self, serifu, engine):
        if not engine in self.sanitizer.keys():
            return serifu

        for s_pair in self.sanitizer[engine]:
            serifu = re.sub(s_pair[self.RE], s_pair[self.SUB], serifu)

        return serifu

    def pair(self, line, actor):
        pair = line.split(',', maxsplit=1)  # 声優名だけを分離

        if len(pair) == 1:
            return [actor, line]

        return pair
