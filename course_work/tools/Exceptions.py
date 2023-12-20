class EmptyProgramError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return "At least one statement was expected, nothing was found"


class UnexpectedCharacterSequenceError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return "Unexpected character sequence at: " + self.args[0] if self.args else "[parser failed]"


class OperatorSyntaxError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


raise UnexpectedCharacterSequenceError()
