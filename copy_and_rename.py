#! python copy_and_rename.py
# -*- coding: utf-8 -*-

import sys
from scenario import check_command_line_args
from scenario.project import Project
from scenario.worker.renamer import Renamer

# 生成されたオーディオファイルの連番リネーム
if __name__ == '__main__' or len(sys.argv < 2):
    args = sys.argv

    if not check_command_line_args(args):
        quit()

    project = Project(args[1])

    if not project.exists():
        print(f'project directory is not exist! : {project.name}')
        quit()

    renamer = Renamer(project)

    if renamer.copy_and_rename():
        print('complete!')
