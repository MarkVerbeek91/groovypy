class Shell:
    def __init__(self, parent, command):
        self.parent = parent
        self.command = command

    def __call__(self):
        print(self.command)
