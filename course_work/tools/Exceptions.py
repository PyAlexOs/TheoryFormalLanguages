from course_work.tools.structures import Token


class ModelLanguageError(BaseException):
    def __init__(self, *args):
        super().__init__(*args)


class EmptyProgramError(ModelLanguageError):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return "At least one statement was expected, nothing was found before the 'end' statement"


class EndOfProgramError(ModelLanguageError):
    def __init__(self, _token: Token = None):
        self.token = _token
        super().__init__()

    def __str__(self):
        if not self.token:
            return "The 'end' token was expected but was not found"

        return ("Tokens were not expected after the 'end' but were found at " +
                str(self.token.line) + ":" + str(self.token.char) + " " +
                self.token.value)


class UnexpectedTokenError(ModelLanguageError):
    def __init__(self, _token: Token, _expected: str):
        self.token = _token
        self.expected = _expected
        super().__init__()

    def __str__(self):
        return ("Unexpected token at " + str(self.token.line) + ":" +
                str(self.token.char) + ". " + self.expected + " was expected, " +
                self.token.value + " was found")


class UnexpectedCharacterSequenceError(ModelLanguageError):
    def __init__(self, _token: Token):
        self.token = _token
        super().__init__()

    def __str__(self):
        return ("Unexpected character sequence at " + str(self.token.line) + ":" +
                str(self.token.char) + " " + self.token.value)
