class Stages:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.stage = kwargs.pop("stage", [])

    def __call__(self, *args, **kwargs):
        for stage in self.stage:
            stage()
