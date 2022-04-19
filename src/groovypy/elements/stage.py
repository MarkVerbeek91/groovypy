class Stage:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.name = kwargs.pop("name", "")
        self.steps = kwargs.pop("steps", [])
        cond = kwargs.pop("condition", None)
        self.condition = cond if cond is not None else True
        self.parallel = kwargs.pop("parallel", None)

    def __call__(self, *args, **kwargs):
        print(self.name)
        if self.condition:
            if callable(self.parallel):
                self.parallel()
            else:
                for step in self.steps:
                    step()
