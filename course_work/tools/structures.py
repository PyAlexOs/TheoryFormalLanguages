from dataclasses import dataclass
from enum import Enum


class State(Enum):
    EOF = -1
    Note = 0
    Start = 1

    Delimiter = 2
    Identifier = 3
    Number = 4
    Type = 5
    Undefined = 6


class TokenType(Enum):
    UNEXPECTED_CHARACTER_SEQUENCE = 0
    END = 1
    DIM = 2
    AS = 3
    IF = 4
    THEN = 5
    ELSE = 6
    FOR = 7
    TO = 8
    DO = 9
    WHILE = 10
    READ = 11
    WRITE = 12

    OR = 13
    AND = 14
    NOT = 15
    TRUE = 16
    FALSE = 17

    BINARY = 18
    OCTAL = 19
    DECIMAL = 20
    HEXADECIMAL = 21
    REAL = 22
    BOOLEAN = 23

    IDENTIFIER = 24

    EQUALS = 25
    NOT_EQUALS = 26
    LESS = 27
    LESS_EQUALS = 28
    GREATER = 29
    GREATER_EQUALS = 30

    BLOCK_START = 31
    BLOCK_END = 32
    ARGUMENT_START = 33
    ARGUMENT_END = 34
    ARGUMENT_DELIMITER = 35
    OPERATOR_DELIMITER = 36

    ADDITION = 37
    SUBTRACTION = 38
    MULTIPLICATION = 39
    DIVISION = 40

    NOTE_START = 41
    NOTE_END = 42


KEYWORDS = {
    "end": TokenType.END,
    "dim": TokenType.DIM,
    "as": TokenType.AS,
    "if": TokenType.IF,
    "then": TokenType.THEN,
    "else": TokenType.ELSE,
    "for": TokenType.FOR,
    "to": TokenType.TO,
    "do": TokenType.DO,
    "while": TokenType.WHILE,
    "read": TokenType.READ,
    "write": TokenType.WRITE,

    "or": TokenType.OR,
    "and": TokenType.AND,
    "not": TokenType.NOT,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE
}

DELIMITERS = {
    "<>": TokenType.NOT_EQUALS,
    "=": TokenType.EQUALS,
    "<": TokenType.LESS,
    "<=": TokenType.LESS_EQUALS,
    ">": TokenType.GREATER,
    ">=": TokenType.GREATER_EQUALS,

    "[": TokenType.BLOCK_START,
    "]": TokenType.BLOCK_END,
    "(": TokenType.ARGUMENT_START,
    ")": TokenType.ARGUMENT_END,
    ",": TokenType.ARGUMENT_DELIMITER,
    ":": TokenType.OPERATOR_DELIMITER,
    "\n": TokenType.OPERATOR_DELIMITER,

    "+": TokenType.ADDITION,
    "-": TokenType.SUBTRACTION,
    "*": TokenType.MULTIPLICATION,
    "/": TokenType.DIVISION
}

WHITESPACES = [" ", "\t", "\r"]
DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
EXTENDED_DIGITS = [*DIGITS,
                   "A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f",
                   "+", "-", ".", "O", "o", "H", "h"]

LETTERS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
           "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
           "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
           "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


@dataclass
class Token:
    """ Represents a token used to write to a file and read from a file """
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
        return str(self.token_type.value) + " " + self.value + " " + str(self.line) + " " + str(self.char)

    def __repr__(self) -> str:
        return self.token_type.name + "(" + self.value + ") at {" + str(self.line) + ", " + str(self.char) + "}"


class IdentifierType(Enum):
    INTEGER = 1
    REAL = 2
    BOOLEAN = 3


TYPES = {
    "%": IdentifierType.INTEGER,
    "!": IdentifierType.REAL,
    "$": IdentifierType.BOOLEAN
}


@dataclass
class Identifier:
    """ Represents an identifier that is used to control the use of identifiers in the program """
    name: str
    type: IdentifierType
    value: str
    is_assigned: bool

    def __init__(self, _name, _type):
        self.name = _name
        self.type = _type
        self.value = ""
        self.is_assigned = False

    def __str__(self) -> str:
        return (self.name + ":" + self.type.name + "." +
                "\t is " + ("not " if self.is_assigned else "") + "assigned")

    def __repr__(self):
        return self.type.name + "(" + self.name + "): " + str(self.is_assigned)


OPERATIONS = {
    TokenType.EQUALS: [
        [
            ['REAL', 'REAL'],
            ['BOOLEAN', 'BOOLEAN'],
            ['INTEGER', 'INTEGER'],
            ['INTEGER', 'REAL'],
            ['REAL', 'INTEGER']
        ],
        [
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN
        ]
    ],
    TokenType.NOT_EQUALS: [
        [
            ['REAL', 'REAL'],
            ['BOOLEAN', 'BOOLEAN'],
            ['INTEGER', 'INTEGER'],
            ['INTEGER', 'REAL'],
            ['REAL', 'INTEGER']
        ],
        [
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN
        ]
    ],
    TokenType.LESS: [
        [
            ['REAL', 'REAL'],
            ['INTEGER', 'INTEGER'],
            ['INTEGER', 'REAL'],
            ['REAL', 'INTEGER']
        ],
        [
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
        ]
    ],
    TokenType.LESS_EQUALS: [
        [
            ['REAL', 'REAL'],
            ['INTEGER', 'INTEGER'],
            ['INTEGER', 'REAL'],
            ['REAL', 'INTEGER']
        ],
        [
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
        ]
    ],
    TokenType.GREATER: [
        [
            ['REAL', 'REAL'],
            ['INTEGER', 'INTEGER'],
            ['INTEGER', 'REAL'],
            ['REAL', 'INTEGER']
        ],
        [
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
        ]
    ],
    TokenType.GREATER_EQUALS: [
        [
            ['REAL', 'REAL'],
            ['INTEGER', 'INTEGER'],
            ['INTEGER', 'REAL'],
            ['REAL', 'INTEGER']
        ],
        [
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
            IdentifierType.BOOLEAN,
        ]
    ],

    TokenType.ADDITION: [
        [
            ['REAL', 'REAL'],
            ['INTEGER', 'INTEGER'],
            ['INTEGER', 'REAL'],
            ['REAL', 'INTEGER']
        ],
        [
            IdentifierType.REAL,
            IdentifierType.INTEGER,
            IdentifierType.REAL,
            IdentifierType.REAL
        ]
    ],
    TokenType.SUBTRACTION: [
        [
            ['REAL', 'REAL'],
            ['INTEGER', 'INTEGER'],
            ['INTEGER', 'REAL'],
            ['REAL', 'INTEGER']
        ],
        [
            IdentifierType.REAL,
            IdentifierType.INTEGER,
            IdentifierType.REAL,
            IdentifierType.REAL
        ]
    ],
    TokenType.OR: [
        [
            ['BOOLEAN', 'BOOLEAN']
        ],
        [
            IdentifierType.BOOLEAN
        ]
    ],

    TokenType.MULTIPLICATION: [
        [
            ['REAL', 'REAL'],
            ['INTEGER', 'INTEGER'],
            ['INTEGER', 'REAL'],
            ['REAL', 'INTEGER']
        ],
        [
            IdentifierType.REAL,
            IdentifierType.INTEGER,
            IdentifierType.REAL,
            IdentifierType.REAL
        ]
    ],
    TokenType.DIVISION: [
        [
            ['REAL', 'REAL'],
            ['INTEGER', 'INTEGER'],
            ['INTEGER', 'REAL'],
            ['REAL', 'INTEGER']
        ],
        [
            IdentifierType.REAL,
            IdentifierType.REAL,
            IdentifierType.REAL,
            IdentifierType.REAL
        ]
    ],
    TokenType.AND: [
        [
            ['BOOLEAN', 'BOOLEAN']
        ],
        [
            IdentifierType.BOOLEAN
        ]
    ]
}
