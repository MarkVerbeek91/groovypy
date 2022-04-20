import subprocess


class Shell:
    def __init__(self, parent, command):
        self.parent = parent
        self.command = command

    def __call__(self):
        try:
            subprocess.run(self.command, shell=True, check=True)
        except subprocess.CalledProcessError as err:
            print(f"Command did not run: {err}")
