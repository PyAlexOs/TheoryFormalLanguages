from enum import Enum


class State(Enum):
    EOF = -1
    Note = 0
    Start = 1

    Delimiter = 2
    Identifier = 3
    Number = 4
    Type = 5
