# from groovypy.elements.echo import Echo
# from groovypy.elements.shell import Shell
#
# classes = [Echo, Shell]

import importlib
import inspect
from pathlib import Path

classes = []

for pkg in Path(Path(__file__).parent).iterdir():
    if pkg.suffix == ".py" and pkg.name != "__init__.py":
        elements = importlib.import_module(".{0}".format(pkg.stem), package="groovypy.elements")

        for subclass in inspect.getmembers(elements, inspect.isclass):
            if subclass not in classes:
                classes.append(subclass[1])

classes = dict(map(lambda x: (x.__name__, x), classes))


def class_provider():
    for pmodel_class in classes:
        yield classes[pmodel_class]
