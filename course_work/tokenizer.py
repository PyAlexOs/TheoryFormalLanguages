from course_work.tools.structures import (State,
                                          Token,
                                          TokenType,
                                          DELIMITERS,
                                          LETTERS,
                                          DIGITS,
                                          EXTENDED_DIGITS,
                                          WHITESPACES,
                                          TYPES,
                                          KEYWORDS)
from course_work.tools.tokenQueue import TokenQueue
import re


def is_binary(token: str) -> bool:
    """ Checks if the token is binary """
    return re.match(r"^[01]+[Bb]$", token) is not None


def is_octal(token: str) -> bool:
    """ Checks if the token is octal """
    return re.match(r"^[0-7]+[Oo]$", token) is not None


def is_decimal(token: str) -> bool:
    """ Checks if the token is decimal """
    return re.match(r"^\d+[Dd]?$", token) is not None


def is_hexadecimal(token: str) -> bool:
    """ Checks if the token is hexadecimal """
    return re.match(r"^\d[0-9a-fA-F]*[Hh]$", token) is not None


def is_real(token: str) -> bool:
    """ Checks if the token is real """
    return re.match(r"^(\d+[Ee][+-]?\d+)|(\d*\.\d+([Ee][+-]?\d+)?)$", token) is not None


def get_tokens(filename: str, encoding: str = "utf-8") -> TokenQueue:
    """ Splits the source code of the program into tokens """
    tokens = TokenQueue()
    current_state = State.Start
    current_symbol = ""
    buffer = ""

    current_line = 1
    current_char = 0

    with (open(filename, "r", encoding=encoding) as program):
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
                        tokens.put(Token(_value=buffer, _token_type=TokenType.NOTE_START,
                                         _line=current_line, _char=current_char - 1))
                        current_state = State.Note

                    elif current_symbol == "" and buffer == "":
                        current_state = State.EOF

                    else:
                        current_state = State.Undefined

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

                        else:
                            tokens.put(Token(_value=buffer, _token_type=TokenType.IDENTIFIER,
                                             _line=current_line, _char=current_char - len(buffer)))

                        buffer = current_symbol
                        current_state = State.Start

                    continue

                case State.Delimiter:
                    current_symbol = program.read(1)
                    current_char += 1

                    if buffer + current_symbol in ["<>", "<=", ">="]:
                        tokens.put(Token(_value=buffer + current_symbol,
                                         _token_type=DELIMITERS[buffer + current_symbol],
                                         _line=current_line, _char=current_char - 2))
                        buffer = ""

                    else:
                        if buffer == "\n":
                            buffer = ":"
                            tokens.put(Token(_value=buffer, _token_type=DELIMITERS[buffer],
                                             _line=current_line, _char=current_char - 1))

                            current_line += 1
                            current_char = 0
                        else:
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
                    current_char += 1

                    if current_symbol == "\n":
                        current_line += 1
                        current_char = 0

                    if current_symbol == "}":
                        buffer = current_symbol
                        tokens.put(Token(_value=buffer, _token_type=TokenType.NOTE_END,
                                         _line=current_line, _char=current_char - 1))
                        buffer = ""
                        current_state = State.Start

                    elif current_symbol == "":
                        buffer = ""
                        current_state = State.Start

                    continue

                case State.Undefined:
                    current_symbol = program.read(1)
                    current_char += 1

                    if (current_symbol in DELIMITERS.keys() or current_symbol in LETTERS
                            or current_symbol in TYPES.keys() or current_symbol in DIGITS
                            or current_symbol in WHITESPACES or current_symbol in ["{", "."]):
                        tokens.put(Token(_value=buffer, _token_type=TokenType.UNEXPECTED_CHARACTER_SEQUENCE,
                                         _line=current_line, _char=current_char - len(buffer)))
                        buffer = current_symbol
                        current_state = State.Start
                    else:
                        if current_symbol == "":
                            tokens.put(Token(_value=buffer, _token_type=TokenType.UNEXPECTED_CHARACTER_SEQUENCE,
                                             _line=current_line, _char=current_char - len(buffer)))
                            current_state = State.EOF
                        buffer += current_symbol

                    continue

    return tokens
