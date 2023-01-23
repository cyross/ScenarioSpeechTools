#! python scenario_speech_separator.py
# -*- coding: utf-8 -*-

import sys
import os
import yaml

# シナリオファイルセパレーター

if __name__ == '__main__' or len(sys.argv < 2):
    project_dir = sys.argv[1]

    if not os.path.exists(sys.argv[1]):
        print(f'project directory is not exist! : {project_dir}')
        quit()

    config = None
    with open('./config.yaml', 'r', encoding='utf-8') as yaml_file:
        config = yaml.safe_load(yaml_file)

    serifu_file_path = os.path.join(project_dir, config['input_dir'], config['serifu_file'])

    if not os.path.exists(serifu_file_path):
        quit()

    jimaku_file_path = os.path.join(
        project_dir, config['input_dir'], config['jimaku_file'])
    streams = {}
    current_actor = list(config['voice_actor'].keys())[0]
    current_serifu = ''

    print('read serifu file...')

    with open(serifu_file_path, 'r', encoding=config['serifu_file_encoding']) as serifu_file:
        print('write jimaku file...')

        with open(jimaku_file_path, 'w', encoding=config['output_file_encoding']['jimaku']) as jimaku_file:
            print('separate serifu file...')

            for serifu_line in serifu_file:
                serifu_line = serifu_line.rstrip('\n')
                serifu_pair = serifu_line.split(',', maxsplit = 1) # 声優名だけを分離
                if len(serifu_pair) == 2 and current_actor in config['voice_actor']:
                    current_actor = serifu_pair[0]
                    current_serifu = serifu_pair[1]
                else: # 声優名を省略している場合は、先に指定した声優名を引き継いで使用
                    current_serifu = serifu_line

                voice_engine = config['voice_actor'][current_actor]
                separator = config['voice_engine'][voice_engine]['Separator']

                if not voice_engine in streams:
                    serifu_per_engine_filename = config['serifu_per_engine_file'].format(voice_engine)
                    serifu_per_engine_file_path = os.path.join(project_dir, config['input_dir'], serifu_per_engine_filename)
                    streams[voice_engine] = open(serifu_per_engine_file_path, 'w', encoding=config['output_file_encoding'][voice_engine])

                streams[voice_engine].write(f'{current_actor}{separator}{current_serifu}\n')
                jimaku_file.write(f'{current_actor}:{current_serifu}\n')

    for stream in streams.values():
        stream.close()

    print('complete!')
