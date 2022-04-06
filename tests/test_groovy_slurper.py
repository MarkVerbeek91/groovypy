from textx import metamodel_from_file


class Echo:
    def __init__(self, parent, message):
        self.parent = parent
        self.message = message

    def __call__(self, *args, **kwargs):
        print(self.message)


classes = [Echo]


def test():
    meta_model = metamodel_from_file('groovy.tx', classes=classes)
    model = meta_model.model_from_file('minimal_Jenkinsfile')

    model.pipeline.comps[0].stages[0].steps[0].steps[0]()


if __name__ == "__main__":
    ...
