from textx import metamodel_from_file

from groovypy.elements import class_provider


class Slurper:
    meta_model = metamodel_from_file('groovy.tx', classes=class_provider())

    @classmethod
    def parse(cls, input_file):
        return cls.meta_model.model_from_file(input_file)


if __name__ == "__main__":
    model = Slurper().parse("example")

    print(model)
