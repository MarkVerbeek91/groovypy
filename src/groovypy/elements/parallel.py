class Parallel:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.commands = kwargs.pop("stage", [])

    def __call__(self, *args, **kwargs):
        for command in self.commands:
            command()
