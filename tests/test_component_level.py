from pathlib import Path

import pytest

from groovypy.slurper import Slurper


@pytest.mark.parametrize(
    "input_file", [str(p) for p in Path(Path(__file__) / ".." / "data").iterdir()]
)
def test_slurp_example(input_file):
    Slurper().parse(str(input_file))
