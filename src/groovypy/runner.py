from groovypy.slurper import Slurper


class Runner:
    @classmethod
    def __enter__(cls):
        return cls

    @classmethod
    def __exit__(cls, exc_type, exc_val, exc_tb):
        ...

    @classmethod
    def run(cls, config):
        config.pipeline()


if __name__ == "__main__":
    model = Slurper().parse("example")

    with Runner() as runner:
        runner.run(model)
