import sys
import os
import yaml
import pathlib
import re

# ユーティリティ関数群

def sanitarily_actor_name(actor_name):
    return re.sub(r'[:\.\s\(\)\[\]\\\/]+', '_', actor_name)

def create_voicepeak_actor_list(config):
    return list(filter(lambda actor: config['voice_actor'][actor] == "VP",config['voice_actor'].keys()))

def create_voicepeak_dir(engine_name, actor_list):
    for actor_name in actor_list:
        vp_name = f'{engine_name}_{actor_name}'
        create_voice_engine_dir(vp_name)

def create_voice_engine_dir(engine_name, output_dir):
    print(f'generating output [{engine_name}] folder...')
    output_voice_engine_dir = os.path.join(output_dir, engine_name)
    os.mkdir(output_voice_engine_dir)

