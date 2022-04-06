class Stage:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.steps = kwargs.pop('steps', [])

    def __call__(self, *args, **kwargs):
        for step in self.steps:
            step()
