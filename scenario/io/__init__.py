# -*- coding: utf-8 -*-

import os
import glob
import pathlib
import shutil

def is_dir(path: str) -> bool:
    return os.path.isdir(path)

def make_dir(dir: str) -> None:
    os.mkdir(dir)

def create_file(filepath: str) -> None:
    pathlib.Path.touch(filepath)

def copy_file(src_path: str, dst_path: str) -> None:
    shutil.copyfile(src_path, dst_path)

def generate_stream(filepath: str, mode: str, encoding: str):
    return open(filepath, mode, encoding=encoding)

def filename(path: str) -> str:
    return os.path.basename(path)

def splitext(path: str) -> tuple[str]:
    return os.path.splitext(filename(path))

def basename(path: str) -> str:
    return splitext(path)[0]

def ext(path: str) -> str:
    return splitext(path)[1]

def split_basename(path: str, sep: str ='-') -> list[str]:
    return basename(path).split(sep)

def file_exists(path: str) -> bool:
    return os.path.exists(path)

class IO:
    BASE_DIR = 'project_base_dir'
    IN_DIR = 'input_dir'
    OUT_DIR = 'output_dir'
    RN_DIR = 'renamed_output_dir'
    JIMAKU_FILE = 'jimaku_file'
    R_JIMAKU_FILE = 'raw_jimaku_file'
    SERIFU_FILE = 'serifu_file'
    SERIFU_PE_FILE = 'serifu_per_engine_file'
    AUDIO_FILE_EXT = 'supported_audio_file_ext'

    def __init__(self, project_name, config):
        self.base_dir = config.get(self.BASE_DIR)
        self.project_dir = self.join_base_dir(project_name)
        self.input_dir = self.join_project_dir(config.get(self.IN_DIR))
        self.output_dir = self.join_project_dir(config.get(self.OUT_DIR))
        self.renamed_dir = self.join_output_dir(config.get(self.RN_DIR))

        self.base_serifu_filepath = self.join_input_dir(config.get(self.SERIFU_FILE))
        self.jimaku_filepath = self.join_input_dir(config.get(self.JIMAKU_FILE))
        self.raw_jimaku_filepath = self.join_input_dir(config.get(self.R_JIMAKU_FILE))
        self.serifu_file_base = config.get(self.SERIFU_PE_FILE)

        self.supported_exts = config.get(self.AUDIO_FILE_EXT)

    def join_base_dir(self, *paths) -> str:
        return os.path.join(self.base_dir, *paths)

    def join_project_dir(self, *paths) -> str:
        return os.path.join(self.project_dir, *paths)

    def join_input_dir(self, *paths) -> str:
        return os.path.join(self.input_dir, *paths)

    def join_output_dir(self, *paths) -> str:
        return os.path.join(self.output_dir, *paths)

    def join_rename_dir(self, *paths) -> str:
        return os.path.join(self.renamed_dir, *paths)

    def glob_audio_files(self, current_dir, key, glob_files, sort_file) -> dict[str, any]:
        current_dir_glob = os.path.join(current_dir, '*')

        path_globs = sort_file(glob.glob(current_dir_glob), key)
        for path_name in path_globs:
            if is_dir(path_name):
                glob_files = self.glob_audio_files(path_name, key, glob_files, sort_file)
                continue

            file_exts = splitext(path_name)

            if len(file_exts) < 2:
                continue

            file_ext = file_exts[1]

            if file_ext in self.supported_exts:
                glob_files[key].append(path_name)

        return glob_files

    def serifu_file_path(self, key: str) -> str:
        return self.join_input_dir(self.serifu_file_base.format(key))
