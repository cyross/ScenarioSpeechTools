#! python build_project.py
# -*- coding: utf-8 -*-

import sys
from modules import check_command_line_args
from modules.io import *
from modules.project import Project
from modules.worker.builder import Builder

# シナリオプロジェクトフォルダ作成
if __name__ == '__main__':
    args = sys.argv

    if not check_command_line_args(args):
        quit()

    project = Project(args[1])

    project.create_projects_dir()

    if project.exists():
        print(f'project folder is already exist! : {project.name}')
        quit()

    builder = Builder(project)

    if builder.build():
        print('complete!')
