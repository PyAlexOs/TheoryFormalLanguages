from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    Binary = 1
    Octal = 2
    Decimal = 3
    Hexadecimal = 4
    Real = 5
    Boolean = 6

    Keyword = 7
    Identifier = 8
    Assignment = 9
    VariableType = 10
    Delimiter = 11

    Relation = 12
    AddSub = 13
    MulDiv = 14
    Not = 15


@dataclass
class Token:
    value: str
    token_type: TokenType
    line: int
    char: int

    def __init__(self, _value, _token_type, _line, _char):
        self.value = _value
        self.token_type = _token_type
        self.line = _line
        self.char = _char

    def __str__(self) -> str:
        return self.token_type.name + "(" + self.value + ") at {" + str(self.line) + ", " + str(self.char) + "}"

    def __repr__(self) -> str:
        return self.token_type.name + "\t\t" + self.value
