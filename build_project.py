#! python build_project.py
# -*- coding: utf-8 -*-

import sys
from scenario.io import *
from scenario import check_command_line_args
from scenario.project import Project
from scenario.worker.builder import Builder

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
