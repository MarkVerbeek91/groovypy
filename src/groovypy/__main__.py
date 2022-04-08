from groovypy.slurper import Slurper
from groovypy.runner import Runner


def main():
    model = Slurper().parse('Jenkinsfile')

    with Runner() as runner:
        runner.run(model)


if __name__ == "__main__":
    main()
