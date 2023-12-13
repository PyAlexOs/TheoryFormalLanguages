from enum import Enum


class State(Enum):
    Error = -1
    Note = 0
    Start = 1

    Delimiter = 2
    Identifier = 3
    Number = 4

    MulDiv = 5
    AddSub = 6
    Relation = 7
    Type = 8
