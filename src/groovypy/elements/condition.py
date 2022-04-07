class Condition:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.expression = kwargs.pop('expression', True)

    def __bool__(self):
        return True
