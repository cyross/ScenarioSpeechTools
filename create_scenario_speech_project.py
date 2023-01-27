#! python create_scenario_speech_project.py
# -*- coding: utf-8 -*-

import sys
import os
from utility import *

# シナリオプロジェクト作成

if __name__ == '__main__' or len(sys.argv < 2):
    config = load_config_file()

    project_name, project_dir, dir_exist = project_dir_status(sys.argv[1], config)

    if dir_exist:
        print(f'project folder is already exist! : {project_name}')
        quit()

    voicepeak_actors = create_voicepeak_actor_list(config)

    print('generating project folder...')

    create_project_base_dir(config)

    os.mkdir(project_dir)

    input_dir = os.path.join(project_dir, config['input_dir'])

    print('generating input folder...')

    os.mkdir(input_dir)

    serifu_filepath = os.path.join(input_dir, config['serifu_file'])

    print('generating serifu file...')

    create_serifu_file(serifu_filepath)

    output_dir = os.path.join(project_dir, config['output_dir'])

    print('generating output folder...')

    os.mkdir(output_dir)

    for voice_engine_key in config['voice_engine'].keys():
        if voice_engine_key == "VP":
            create_voicepeak_dir(voice_engine_key, voicepeak_actors, output_dir)
        else:
            create_voice_engine_dir(voice_engine_key, output_dir)

    print('generating renamed output file folder...')

    renamed_output_dir = os.path.join(output_dir, config['renamed_output_dir'])
    os.mkdir(renamed_output_dir)

    print('complete!')
