class Echo:
    def __init__(self, parent, message):
        self.parent = parent
        self.message = message

    def __call__(self, *args, **kwargs):
        print(self.message)
