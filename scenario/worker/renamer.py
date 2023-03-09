# -*- coding: utf-8 -*-

from scenario import Base
from scenario.io import *
from scenario.file.raw_jimaku import RawJimaku

class Renamer(Base):
    RN_DIGITS = 'rename_digits'

    def __init__(self, project):
        super().__init__(project)

        self.actor = self.project.actor
        self.engine = self.project.engine
        self.raw_jimaku: RawJimaku = RawJimaku(self.project)
        self.rename_digits = self.project.config.get(self.RN_DIGITS)
        # 確実にエラー無く処理するために+を使用
        self.output_file_format = '{0:0' + '{0}'.format(self.rename_digits) + '}{1}'

        self.sort_types = {
            'last': {
                'keys': ['VR', 'AIV'],
                'lambda': lambda path: int(split_basename(path).pop())
            },
            'first': {
                'keys': ['VP'],
                'lambda': lambda path: int(split_basename(path)[0])
            }
        }

    def format_output_file(self, ext: str, counter: int) -> str:
        return self.output_file_format.format(counter, ext)

    def _generate_engines_from_jimaku(self):
        engines = []

        for jimaku_line in self.raw_jimaku.lines:
            actor_name = jimaku_line.split(':', maxsplit=1)[0]  # 声優名だけを分離

            key = self.actor.engine(actor_name)

            # NONEのものは音声ファイルが無いので無視
            if self.engine.is_none(key):
                continue

            real_actor_name = self.actor.real_name(actor_name)

            if self.engine.is_sep(key):
                key = f'{key}_{self.actor.sanitize(real_actor_name)}'

            engines.append(key)

        return engines

    def _list_audio_files(self, engines):
        files = {}

        for key in engines:
            files[key] = []
            dir = self.io.join_output_dir(key)
            files = self.io.glob_audio_files(
                dir, key, files, self._sort_filepath)

        return files

    def _sort_filepath(self, path_globs, key):
        for sort_type in self.sort_types.keys():
            if key in self.sort_types[sort_type]['keys']:
                return sorted(path_globs, key=self.sort_types[sort_type]['lambda'])
        return sorted(path_globs)

    def _copy_and_rename_files(self, engines, files):
        counter = 0

        for key in engines:
            org_path = files[key].pop(0)

            filename = self.output_file_format.format(counter, ext(org_path))
            new_path = self.io.join_rename_dir(filename)

            copy_file(org_path, new_path)

            counter = counter + 1

    def copy_and_rename(self):
        self.raw_jimaku.load()

        # 字幕ファイルをもとに、声優の順番に対応する音声合成エンジンのリストを作成
        engines = self._generate_engines_from_jimaku()
        line_cnt = len(engines)
        engines_unique = list(set(engines))

        # 音声ファイルのリストを、音声合成エンジン別にリストアップ
        files = self._list_audio_files(engines_unique)
        file_cnt = sum(map(lambda key: len(files[key]), files))

        if file_cnt != line_cnt:
            print(f'generated audio file number is not equal jimaku lines! - files:{file_cnt} lines:{line_cnt}')
            return False

        # 音声合成エンジンのリストをもとに、音声ファイルをリネームしてコピー
        self._copy_and_rename_files(engines, files)

        return True
