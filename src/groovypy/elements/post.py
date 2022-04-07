class Post:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.cleanups = kwargs.pop('cleanups', [])

    def __call__(self, *args, **kwargs):
        for command in self.cleanups.commands:
            command()
