from course_work.tools.structures import Token


class EmptyProgramError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return "At least one statement was expected, nothing was found before the 'end' statement"


class EndOfProgramError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        if not self.args:
            return "The 'end' token was expected but was not found"

        return ("Tokens were not expected after the 'end' but were found: " +
                self.args[0] if self.args else "[parser failed]")


class UnexpectedTokenError(Exception):
    def __init__(self, _token: Token):
        self.token = _token
        super().__init__()

    def __str__(self):
        return ("Unexpected token at " + str(self.token.line) + ":" +
                str(self.token.char) + " " + self.token.value) + ". Description or operator expected"


class UnexpectedCharacterSequenceError(Exception):
    def __init__(self, _token: Token):
        self.token = _token
        super().__init__()

    def __str__(self):
        return ("Unexpected character sequence at " + str(self.token.line) + ":" +
                str(self.token.char) + " " + self.token.value)
