from enum import Enum


class State(Enum):
    Error = -1
    Note = 0
    Start = 1

    Delimiter = 2
    Identifier = 3
    Keyword = 4
    Number = 5
    Boolean = 6

    MulDiv = 7
    AddSub = 8
    Logical = 9
    Relation = 10
    Type = 11
