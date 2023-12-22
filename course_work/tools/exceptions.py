from course_work.tools.structures import Token, TokenType, IdentifierType


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
        if self.token.value == ":":
            self.token.value = "operator delimiter"

        elif self.token.token_type == TokenType.IDENTIFIER:
            self.token.value = "identifier " + '"' + self.token.value + '"'

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


class OperationError(ModelLanguageError):
    def __init__(self, type1: IdentifierType, type2: IdentifierType, operator: str, _line: int, _char: int):
        self.type1 = type1
        self.type2 = type2
        self.operator = operator
        self.line = _line
        self.char = _char
        super().__init__()

    def __str__(self):
        return ("Incorrect operator " + self.operator + " for " +
                self.type1.name.lower() + " and " + self.type2.name.lower() +
                " at " + str(self.line) + ":" + str(self.char))


class PredicateTypeError(ModelLanguageError):
    def __init__(self, _type: IdentifierType, line: int, char: int):
        self._type = _type
        self.line = line
        self.char = char
        super().__init__()

    def __str__(self):
        return ("Incorrect predicate at " + str(self.line) + ":" + str(self.char) +
                ". Expected for boolean, found " + self._type.name.lower())


class AssignmentTypeError(ModelLanguageError):
    def __init__(self, _token: Token, _value: IdentifierType, _type: IdentifierType):
        self.token = _token
        self._type = _type
        self.value = ""
        match _value:
            case IdentifierType.REAL:
                self.value = "real"

            case IdentifierType.INTEGER:
                self.value = "integer"

            case IdentifierType.BOOLEAN:
                self.value = "boolean"

        super().__init__()

    def __str__(self):
        return ("Incorrect assignment type at " + str(self.token.line) + ":" +
                str(self.token.char) + ". Trying to assign " + self._type.name.lower() +
                " variable '" + self.token.value + "' with " + self.value + " value")


class ReferencedBeforeAssignmentError(ModelLanguageError):
    def __init__(self, _token: Token):
        self.token = _token
        super().__init__()

    def __str__(self):
        return ("Variable '" + self.token.value + "' referenced before assignment at " +
                str(self.token.line) + ":" + str(self.token.char))
