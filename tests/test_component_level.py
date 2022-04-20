from pathlib import Path

import pytest

from groovypy.slurper import Slurper

TEST_DATA_PATH = Path(__file__) / ".." / "data"


@pytest.mark.parametrize(
    "input_file",
    [str(p) for p in Path(TEST_DATA_PATH).iterdir()],
)
def test_slurp_example(input_file):
    Slurper().parse(str(input_file))
