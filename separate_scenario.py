#! python separate_scenario.py
# -*- coding: utf-8 -*-

import sys
from scenario import check_command_line_args
from scenario.project import Project
from scenario.worker.separator import Separator

# シナリオファイルセパレーター

if __name__ == '__main__':
    args = sys.argv

    if not check_command_line_args(args):
        quit()

    project = Project(args[1])

    if not project.exists():
        print(f'project directory is not exist! : {project.name}')
        quit()

    if not project.is_serifu_file_exists():
        print(f'serifu file is not exist! : {project.io.serifu_filepath}')
        quit()

    separator = Separator(project)

    if separator.separate():
        print('complete!')
