from language_model import (KEYWORDS, RELATION_SYMBOLS, LOGICAL_OPERATORS, TYPES, ADDSUB, MULDIV, DELIMITERS,
                            WHITESPACES, DIGITS, EXTENDED_DIGITS, BOOLEAN, LETTERS)
from token_struct import Token, TokenType
from states import State
from queue import Queue
import re


def is_binary(token: str) -> bool:
    """ Checks if the token is binary """
    return re.match(r"^[01]+[Bb]$", token) is not None


def is_octal(token: str) -> bool:
    """ Checks if the token is octal """
    return re.match(r"^[0-7]+[Oo]$", token) is not None


def is_decimal(token: str) -> bool:
    """ Checks if the token is decimal """
    return re.match(r"^\d+[Dd]$", token) is not None


def is_hexadecimal(token: str) -> bool:
    """ Checks if the token is hexadecimal """
    return re.match(r"^\d[0-9a-fA-F]*[Hh]$", token) is not None


def is_real(token: str) -> bool:
    """ Checks if the token is real """
    return re.match(r"^(\d+[Ee][+-]?\d+)|(\d*\.\d+([Ee][+-]?\d+)?)$", token) is not None


def get_tokens(filename: str, encoding: str = "utf-8") -> Queue[Token]:
    tokens: Queue[Token] = Queue()
    current_state = State.Start
    current_symbol: str = ""
    buffer: str = ""

    current_line: int = 0
    current_char: int = 0

    with open(filename, "r", encoding=encoding) as program:
        while current_state != State.Error:
            match current_state:
                case State.Start:
                    current_symbol = program.read(1)
                    current_char += 1

                    buffer = current_symbol
                    if current_symbol in WHITESPACES:
                        continue

                    if current_symbol in DELIMITERS:
                        current_state = State.Delimiter

                    elif current_symbol in LETTERS:
                        current_state = State.Identifier

                    elif current_state in DIGITS or current_state == ".":
                        current_state = State.Number

                    elif current_symbol in MULDIV:
                        current_state = State.MulDiv

                    elif current_symbol in ADDSUB:
                        current_state = State.AddSub

                    elif current_symbol in RELATION_SYMBOLS:
                        current_state = State.Relation

                    elif current_symbol in TYPES:
                        current_state = State.Type

                    elif current_symbol == "{":
                        current_state = State.Note

                    else:
                        current_state = State.Error

                    continue

                case State.Delimiter:
                    if buffer == "\n":
                        buffer = ":"
                        current_line += 1
                        current_char = 0
                    tokens.put(Token(_value=buffer, _token_type=TokenType.Delimiter,
                                     _line=current_line, _char=current_char - 1))

                    continue

                case State.Identifier:
                    current_symbol = program.read(1)
                    current_char += 1

                    if current_symbol in LETTERS or current_symbol in DIGITS:
                        buffer += current_symbol
                    else:
                        if buffer in KEYWORDS:
                            current_state = State.Keyword

                        elif buffer in BOOLEAN:
                            current_state = State.Boolean

                        elif buffer in LOGICAL_OPERATORS:
                            current_state = State.MulDiv

                        else:
                            tokens.put(Token(_value=buffer, _token_type=TokenType.Identifier,
                                             _line=current_line, _char=current_char - len(buffer)))

                            if current_symbol in DELIMITERS:
                                buffer = current_symbol
                                current_state = State.Delimiter

                            elif current_symbol in WHITESPACES:
                                current_state = State.Start

                            else:
                                current_state = State.Error

                    continue

                case State.Keyword:
                    tokens.put(Token(_value=buffer, _token_type=TokenType.Keyword,
                                     _line=current_line, _char=current_char - len(buffer)))

                    if current_symbol in DELIMITERS:
                        buffer = current_symbol
                        current_state = State.Delimiter

                    elif current_symbol in WHITESPACES:
                        current_state = State.Start

                    else:
                        current_state = State.Error

                    continue

                case State.Number:
                    current_symbol = program.read(1)
                    current_char += 1

                    if current_symbol in EXTENDED_DIGITS:
                        buffer += current_symbol

                    else:

                        """tokens.put(Token(_value=buffer, _token_type=TokenType.Identifier,
                                         _line=current_line, _char=current_char - len(buffer)))"""

                        if current_symbol in DELIMITERS:
                            buffer = current_symbol
                            current_state = State.Delimiter

                        elif current_symbol in WHITESPACES:
                            current_state = State.Start

                        elif current_symbol in RELATION_SYMBOLS:
                            current_state = State.Relation

                        elif current_symbol in ADDSUB:
                            current_state = State.AddSub

                        elif current_symbol in MULDIV:
                            current_state = State.MulDiv

                        else:
                            current_state = State.Error

                    continue

                case State.Boolean:
                    pass
                    continue

                case State.Note:
                    current_symbol = program.read(1)
                    if current_symbol == "}":
                        current_state = State.Start

                    continue

    if buffer != "" and current_symbol != "":
        tokens.put(Token(_value=buffer, _token_type=TokenType.UnexpectedCharacter,
                         _line=current_line, _char=current_char - len(buffer)))

    return tokens


def save_tokens(filename: str, queue: Queue[Token], encoding: str = "utf-8"):
    with open(filename, "w", encoding=encoding) as file:
        while not queue.empty():
            file.write(str(queue.get()) + "\n")
