class EmptyProgramError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return "At least one statement was expected, nothing was found"


class OperatorError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:

        else:
            return ""


raise EmptyProgramException
