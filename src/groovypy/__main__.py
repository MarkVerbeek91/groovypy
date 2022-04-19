from pathlib import Path

from groovypy.slurper import Slurper
from groovypy.runner import Runner


def main():
    input_file = Path(__file__).parent / ".." / "Jenkinsfile"
    model = Slurper().parse(str(input_file))

    with Runner() as runner:
        runner.run(model)


if __name__ == "__main__":
    main()
