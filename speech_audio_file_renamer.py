#! python speech_audio_file_rename.py
# -*- coding: utf-8 -*-

import sys
import os
import glob
from utility import *

# 生成されたオーディオファイルの連番リネーム

def glob_audio_files(current_dir: str, key: str, glob_files: dict, config: dict) -> dict:
    current_dir_glob = os.path.join(current_dir, '*')

    path_globs = glob.glob(current_dir_glob)
    for path_name in path_globs:
        if os.path.isdir(path_name):
            glob_files = glob_audio_files(path_name, key, glob_files, config)
            continue

        file_exts = os.path.splitext(path_name)

        if len(file_exts) < 2:
            continue

        file_ext = file_exts[1]

        if file_ext in config['supported_audio_file_ext']:
            glob_files[key].append(path_name)

    return glob_files

if __name__ == '__main__' or len(sys.argv < 2):
    project_dir = sys.argv[1]

    if not os.path.exists(project_dir):
        print(f'project directory is not exist! : {project_dir}')
        quit()

    config = load_config_file()

    jimaku_file_path = os.path.join(project_dir, config['input_dir'], config['jimaku_file'])

    # 字幕ファイルをもとに、声優の順番に対応する音声合成エンジンのリストを作成

    print('read jimaku file...')

    engine_per_clause = []

    with open(jimaku_file_path, 'r', encoding=config['output_file_encoding']['jimaku']) as jimaku_file:
        for jimaku_line in jimaku_file:
            jimaku_line = jimaku_line.rstrip('\n')
            actor_name = jimaku_line.split(':', maxsplit = 1)[0] # 声優名だけを分離

            target_voice_engine = config['voice_actor'][actor_name]

            if target_voice_engine == 'VP':
                target_voice_engine = f'{target_voice_engine}_{sanitarily_actor_name(actor_name)}'

            engine_per_clause.append(target_voice_engine)

    # 音声ファイルのリストを、音声合成エンジン別にリストアップ

    print('list up audio file...')

    output_dir = os.path.join(project_dir, config['output_dir'])

    voice_engine_set = list(set(engine_per_clause))
    audio_files = {}
    for voice_engine_key in voice_engine_set:
        audio_files[voice_engine_key] = []
        output_voice_engine_dir = os.path.join(output_dir, voice_engine_key)
        audio_files = glob_audio_files(output_voice_engine_dir, voice_engine_key, audio_files, config)

    audio_file_count = sum(map(lambda key: len(audio_files[key]), audio_files))
    jimaku_line_count = len(engine_per_clause)

    if audio_file_count != jimaku_line_count:
        print(f'generated audio file number is not equal jimaku lines! - files:{audio_file_count} lines:{jimaku_line_count}')
        quit()

    # 音声合成エンジンのリストをもとに、音声ファイルをリネームしてコピー

    print('rename and copy...')

    renamed_output_dirname = os.path.join(project_dir, config['output_dir'], config['renamed_output_dir'])

    rename_file_counter = 0
    output_file_format = '{0:0' + '{0}'.format(config['rename_digits']) + '}{1}' # 確実にエラー無く処理するために+を使用
    for voice_engine_key in engine_per_clause:
        org_filepath = audio_files[voice_engine_key].pop(0)
        org_file_ext = os.path.splitext(org_filepath)[1]

        rename_filename = output_file_format.format(rename_file_counter, org_file_ext)
        rename_filepath = os.path.join(renamed_output_dirname, rename_filename)
        print(f'{org_filepath} -> {rename_filepath}')

        copy_file(org_filepath, rename_filepath)

        rename_file_counter = rename_file_counter + 1

    print('complete!')
