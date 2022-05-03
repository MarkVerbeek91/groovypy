from os.path import expandvars
import subprocess
import shlex


class Shell:
    def __init__(self, parent, command):
        self.parent = parent
        self.command = command

    def __call__(self):
        cmd = " ".join([expandvars(x) for x in shlex.split(self.command)])
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as err:
            print(f"Command did not run: {err}")
