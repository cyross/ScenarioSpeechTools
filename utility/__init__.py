import sys
import os
import yaml
import pathlib
import re
import shutil

# ユーティリティ関数群

def load_config_file(config_file_path = './config.yaml', encoding = 'utf-8'):
    config = None
    with open(config_file_path, 'r', encoding=encoding) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def sanitarily_actor_name(actor_name):
    return re.sub(r'[:\.\s\(\)\[\]\\\/]+', '_', actor_name)

def create_voicepeak_actor_list(config):
    return list(filter(lambda actor: config['voice_actor'][actor] == "VP",config['voice_actor'].keys()))

def create_voicepeak_dir(engine_name, actor_list, output_dir):
    for actor_name in actor_list:
        vp_name = f'{engine_name}_{sanitarily_actor_name(actor_name)}'
        create_voice_engine_dir(vp_name, output_dir)

def create_voice_engine_dir(engine_name, output_dir):
    print(f'generating output [{engine_name}] folder...')
    output_voice_engine_dir = os.path.join(output_dir, engine_name)
    os.mkdir(output_voice_engine_dir)

def create_serifu_file(filepath):
    pathlib.Path.touch(filepath)

def copy_file(src_path, dst_path):
    shutil.copyfile(src_path, dst_path)
