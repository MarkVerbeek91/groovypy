from pathlib import Path

import pytest

from groovypy.runner import Runner
from groovypy.slurper import Slurper

TEST_DATA_PATH = Path(__file__) / ".." / "data"


@pytest.mark.parametrize(
    "input_file",
    [str(p) for p in Path(TEST_DATA_PATH).iterdir()],
)
def test_slurp_example(input_file):
    Slurper().parse(input_file)


@pytest.mark.parametrize(
    "input_file",
    [str(p) for p in Path(TEST_DATA_PATH).iterdir()],
)
def test_run_pipeline(input_file):
    model = Slurper().parse(input_file)

    with Runner() as runner:
        runner.run(model)
