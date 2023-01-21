#! python main.py
# -*- coding: utf-8 -*-

import sys
import os
import yaml

# シナリオファイルセパレーター

if __name__ == "__main__" or len(sys.argv < 2):
    target_dir = sys.argv[1]

    if not os.path.exists(sys.argv[1]):
        quit()

    config = None
    with open('./config.yaml', 'r', encoding='utf-8') as yaml_file:
        config = yaml.safe_load(yaml_file)

    scenario_file_path = os.path.join(target_dir, config['scenario_file'])

    if not os.path.exists(scenario_file_path):
        quit()

    jimaku_file_path = os.path.join(target_dir, config['jimaku_file'])
    streams = {}
    current_actor = list(config['voice_actor'].keys())[0]
    current_serifu = ''

    with open(scenario_file_path, 'r', encoding='utf-8') as serifu_file:
        with open(jimaku_file_path, 'w', encoding='utf-8') as jimaku_file:
            for serifu_line in serifu_file:
                serifu_line = serifu_line.rstrip('\n')
                serifu_pair = serifu_line.split(',')
                if len(serifu_pair) == 2:
                    current_actor = serifu_pair[0]
                    current_serifu = serifu_pair[1]
                else: # len(serifu_pair) == 0
                    current_serifu = serifu_pair[0]

                voice_engine = config['voice_actor'][current_actor]
                separator = config['voice_engine'][voice_engine]['Separator']

                if not voice_engine in streams:
                    output_filename = config['output_file'].format(voice_engine)
                    output_file_path = os.path.join(target_dir, output_filename)
                    streams[voice_engine] = open(output_file_path, 'w', encoding='utf-8')

                streams[voice_engine].write('{}{}{}\n'.format(current_actor, separator, current_serifu))
                jimaku_file.write('{}\n'.format(current_serifu))

    for stream in streams.values():
        stream.close()
