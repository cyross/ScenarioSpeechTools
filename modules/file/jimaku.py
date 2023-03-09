# -*- coding: utf-8 -*-

from modules.file import File

# JIMAKU FILE
class Jimaku(File):
    ENCODE = 'jimaku'

    def __init__(self, project, file_path: str | None = None, file_encode: str | None = None):
        path = file_path if file_path is not None else project.io.jimaku_filepath
        encode = file_encode if file_encode is not None else project.config.get(File.ENCODING)[self.ENCODE]
        super().__init__(project, path, encode)
        self.engine = self.project.engine

    def write(self, actor, jimaku, engine) -> None:
        if self.engine.is_none(engine):
            self.stream.write(f'{jimaku}\n')
        else:
            self.stream.write(f'{actor}:{jimaku}\n')
