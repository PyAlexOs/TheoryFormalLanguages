from structures import (Token, TokenType, KEYWORDS, DELIMITERS, WHITESPACES, TYPES, DIGITS, EXTENDED_DIGITS,
                        LETTERS, IdentifierType, Identifier)
from states import State
from queue import Queue
import re


def is_identifier(token: str) -> bool:
    """ Checks if the token is identifier """
    return re.match(r"^[a-zA-Z][0-9a-zA-Z]*$", token) is not None


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
    """ Splits the source code of the program into tokens """

    tokens: Queue[Token] = Queue()
    current_state = State.Start
    current_symbol: str = ""
    buffer: str = ""

    current_line: int = 1
    current_char: int = 0

    with open(filename, "r", encoding=encoding) as program:
        while current_state != State.EOF:
            match current_state:
                case State.Start:
                    current_symbol = buffer
                    if current_symbol == "":
                        current_symbol = program.read(1)
                        current_char += 1

                    buffer = current_symbol
                    if current_symbol in WHITESPACES:
                        buffer = ""
                        continue

                    elif current_symbol in LETTERS:
                        current_state = State.Identifier

                    elif current_symbol in DIGITS or current_state == ".":
                        current_state = State.Number

                    elif current_symbol in DELIMITERS.keys():
                        current_state = State.Delimiter

                    elif current_symbol in TYPES.keys():
                        current_state = State.Type

                    elif current_symbol == "{":
                        current_state = State.Note

                    elif current_symbol == "" and buffer == "":
                        current_state = State.EOF

                    else:
                        tokens.put(Token(_value=buffer, _token_type=TokenType.UNEXPECTED_CHARACTER_SEQUENCE,
                                         _line=current_line, _char=current_char - len(buffer)))

                    continue

                case State.Identifier:
                    current_symbol = program.read(1)
                    current_char += 1

                    if current_symbol in LETTERS or current_symbol in DIGITS:
                        buffer += current_symbol
                    else:
                        if buffer in KEYWORDS.keys():
                            tokens.put(Token(_value=buffer, _token_type=KEYWORDS[buffer],
                                             _line=current_line, _char=current_char - len(buffer)))

                        elif is_identifier(buffer):
                            tokens.put(Token(_value=buffer, _token_type=TokenType.IDENTIFIER,
                                             _line=current_line, _char=current_char - len(buffer)))

                        else:
                            tokens.put(Token(_value=buffer, _token_type=TokenType.UNEXPECTED_CHARACTER_SEQUENCE,
                                             _line=current_line, _char=current_char - len(buffer)))

                        buffer = current_symbol
                        current_state = State.Start

                    continue

                case State.Delimiter:
                    current_symbol = program.read(1)
                    current_char += 1

                    if buffer + current_symbol in ["<>", "<=", ">="]:
                        tokens.put(Token(_value=buffer, _token_type=DELIMITERS[buffer + current_symbol],
                                         _line=current_line, _char=current_char - 2))
                        buffer = ""

                    else:
                        if buffer == "\n":
                            buffer = ":"
                            current_line += 1
                            current_char = 0
                        tokens.put(Token(_value=buffer, _token_type=DELIMITERS[buffer],
                                         _line=current_line, _char=current_char - 1))
                        buffer = current_symbol

                    current_state = State.Start

                    continue

                case State.Number:
                    current_symbol = program.read(1)
                    current_char += 1

                    if current_symbol in EXTENDED_DIGITS:
                        buffer += current_symbol

                    else:
                        number_type = TokenType.UNEXPECTED_CHARACTER_SEQUENCE
                        if is_binary(buffer):
                            number_type = TokenType.BINARY

                        elif is_octal(buffer):
                            number_type = TokenType.OCTAL

                        elif is_decimal(buffer):
                            number_type = TokenType.DECIMAL

                        elif is_hexadecimal(buffer):
                            number_type = TokenType.HEXADECIMAL

                        elif is_real(buffer):
                            number_type = TokenType.REAL

                        tokens.put(Token(_value=buffer, _token_type=number_type,
                                         _line=current_line, _char=current_char - len(buffer)))

                        buffer = current_symbol
                        current_state = State.Start

                    continue

                case State.Type:
                    tokens.put(Token(_value=buffer, _token_type=TYPES[buffer],
                                     _line=current_line, _char=current_char - 1))
                    buffer = ""
                    current_state = State.Start

                    continue

                case State.Note:
                    current_symbol = program.read(1)
                    if current_symbol == "}":
                        buffer = ""
                        current_state = State.Start

                    continue

    return tokens


def save_tokens(filename: str, queue: Queue[Token], encoding: str = "utf-8"):
    with open(filename, "w", encoding=encoding) as file:
        while not queue.empty():
            file.write(str(queue.get()) + "\n")
