import shlex
import subprocess


class Shell:
    def __init__(self, parent, command):
        self.parent = parent
        self.command = command

    def __call__(self):
        args = shlex.split(self.command)
        print(args)
        # subprocess.run(args, shell=True, check=True)
