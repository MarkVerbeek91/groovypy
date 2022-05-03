import os


class Environment:
    def __init__(self, parent, **kwargs):
        self.parent = parent

        for var in kwargs.pop("variables", []):
            var_name, var_value = var.split("=")
            os.environ[var_name] = var_value
