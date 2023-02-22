#! python scenario_speech_separator.py
# -*- coding: utf-8 -*-

import sys
import os
from utility import *

# シナリオファイルセパレーター

if __name__ == '__main__' or len(sys.argv < 2):
    config = load_config_file()

    project_name, project_dir, dir_exist = project_dir_status(sys.argv[1], config)

    if not dir_exist:
        print(f'project directory is not exist! : {project_dir}')
        quit()

    serifu_file_path = os.path.join(project_dir, config['input_dir'], config['serifu_file'])

    if not os.path.exists(serifu_file_path):
        print(f'serifu file is not exist! : {serifu_file_path}')
        quit()

    jimaku_file_path = os.path.join(project_dir, config['input_dir'], config['jimaku_file'])
    streams = {}
    current_actor = list(config['voice_actor'].keys())[0]
    current_serifu = ''

    serifu_sanitize_regexp = {}

    for voice_engine_key in config['serifu_sanitize_regexp'].keys():
        serifu_sanitize_regexp[voice_engine_key] = []
        sanitize_dict = config['serifu_sanitize_regexp'][voice_engine_key]
        for sanitize_key in sanitize_dict.keys():
            serifu_sanitize_regexp[voice_engine_key].append(
                {
                    'regexp': re.compile(sanitize_key),
                    'sub': sanitize_dict[sanitize_key]
                    }
                )

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

                # voice_engineが"VP(VOICEPEAK)"の場合は、声優名も追加し、セリフファイルから声優名を削除
                # (VOICEPEAKの場合は1声優のみのため)
                stream_key = voice_engine
                if voice_engine in ["VP"]:
                    stream_key = f'{voice_engine}_{current_actor}'

                separator = config['voice_engine'][voice_engine]['Separator']

                if not stream_key in streams:
                    serifu_per_engine_filename = config['serifu_per_engine_file'].format(sanitarily_actor_name(stream_key))
                    serifu_per_engine_file_path = os.path.join(project_dir, config['input_dir'], serifu_per_engine_filename)
                    streams[stream_key] = open(serifu_per_engine_file_path, 'w', encoding=config['output_file_encoding'][voice_engine])

                current_jimaku = current_serifu

                if voice_engine in serifu_sanitize_regexp.keys():
                    sanitize_list = serifu_sanitize_regexp[voice_engine_key]

                    for sanitize_pair in sanitize_list:
                        current_serifu = re.sub(sanitize_pair['regexp'], sanitize_pair['sub'], current_serifu)

                # voice_engineが"VP(VOICEPEAK)"の場合は、声優名を省略
                # (VOICEPEAKの場合は1声優のみのため)
                if voice_engine in ["VP"]:
                    streams[stream_key].write(f'{current_serifu}\n')
                else:
                    streams[stream_key].write(f'{current_actor}{separator}{current_serifu}\n')
                jimaku_file.write(f'{current_actor}:{current_jimaku}\n')

    for stream in streams.values():
        stream.close()

    print('complete!')
