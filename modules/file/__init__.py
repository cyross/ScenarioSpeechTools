# -*- coding: utf-8 -*-

import io
import yaml
from modules import Base

def load_yaml(file_path, encoding = 'utf-8'):
    data: any = None
    with open(file_path, 'r', encoding=encoding) as file:
        data = yaml.safe_load(file)
    return data

# RAW JIMAKU FILE
class File(Base):
    READ = 'r'
    WRITE = 'w'
    ENCODING = 'file_encoding'

    def __init__(self, project, filepath, encode):
        self.filepath: str = filepath
        self.stream: io.TextIOWrapper = None
        self.mode: str | None = None
        self.lines: list[str] = []
        self.encodings = project.config.get(self.ENCODING)
        self.encode = encode

        super().__init__(project)

    def is_open(self) -> bool:
        return self.stream is not None

    def open(self, mode) -> None:
        self.mode = mode
        self.stream = open(self.filepath, mode=self.mode, encoding=self.encode)

    def open_read(self) -> None:
        if not self.is_open():
            self.close()

        self.open(self.READ)

    def open_write(self) -> None:
        if not self.is_open():
            self.close()

        self.open(self.WRITE)

    def load(self) -> None:
        if not self.is_open():
            self.close()

        self.open_read()
        self.read_lines()
        self.close()

    def read_line(self) -> str | None:
        if not self.is_open() or self.mode != self.READ:
            return None

        return self.stream.readline().rstrip('\n')

    def read_lines(self) -> None:
        if not self.is_open() or self.mode != self.READ:
            return None

        self.lines = list(map(lambda line: line.rstrip('\n'), self.stream.readlines()))

    def write(self, line: str) -> bool:
        if not self.is_open() or self.mode != self.WRITE:
            return False

        self.stream.write(line)

        return True

    def close(self) -> None:
        if not self.is_open():
            return

        self.stream.close()
        self.stream = None
