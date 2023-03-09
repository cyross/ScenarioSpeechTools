# -*- coding: utf-8 -*-

# ユーティリティ関数群
def check_command_line_args(args):
    if len(args) == 1:
        print('usage: python {sys.argv[0]} (project name)')
        return False

    return True

class Base:
    def __init__(self, project):
        self.project = project
        self.config = project.config
        self.io = self.project.io
