class Pipeline:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.agent = kwargs.pop('agent', None)
        self.trigger = kwargs.pop('trigger', None)
        self.stages = kwargs.pop('stages', None)
        self.post = kwargs.pop('post', None)

    def __call__(self):

        if self.stages is not None:
            for stage in self.stages.stage:
                stage()

        if self.post is not None:
            self.post()
