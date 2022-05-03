class Condition:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.expression = kwargs.pop("expression", True)

    def __bool__(self):
        if self.expression.func1 == "readFile":
            try:
                with open(self.expression.input1, "r") as file_id:
                    data = file_id.read()
                if self.expression.func2 == "contains":
                    return self.expression.input2 in data
            except FileNotFoundError:
                return False

        return True
