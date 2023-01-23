#! python create_scenario_speech_project.py
# -*- coding: utf-8 -*-

import sys
import os
import yaml
import pathlib

# シナリオプロジェクト作成

if __name__ == '__main__' or len(sys.argv < 2):
    project_name = sys.argv[1]

    project_dir = os.path.join('.', project_name)

    if os.path.exists(project_dir):
        print(f'project folder is already exist! : {project_name}')
        quit()

    config = None
    with open('./config.yaml', 'r', encoding='utf-8') as yaml_file:
        config = yaml.safe_load(yaml_file)

    print('generating project folder...')

    os.mkdir(project_dir)

    input_dir = os.path.join(project_dir, config['input_dir'])

    print('generating input folder...')

    os.mkdir(input_dir)

    serifu_filepath = os.path.join(input_dir, config['serifu_file'])

    print('generating serifu file...')

    pathlib.Path.touch(serifu_filepath)

    output_dir = os.path.join(project_dir, config['output_dir'])

    print('generating output folder...')

    os.mkdir(output_dir)

    for voice_engine_key in config['voice_engine'].keys():
        output_voice_engine_dir = os.path.join(output_dir, voice_engine_key)

        print(f'generating output [{voice_engine_key}] folder...')

        os.mkdir(output_voice_engine_dir)

    print('generating renamed output file folder...')

    renamed_output_dir = os.path.join(output_dir, config['renamed_output_dir'])
    os.mkdir(renamed_output_dir)

    print('complete!')
