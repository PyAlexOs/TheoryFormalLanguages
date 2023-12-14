from consts import (KEYWORDS, RELATION_SYMBOLS, LOGICAL_OPERATORS, TYPES, ADDSUB, MULDIV, DELIMITERS,
                    WHITESPACES, BOOLEAN, DIGITS, EXTENDED_DIGITS, LETTERS)
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

    current_line: int = 1
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
                    current_state = State.Start

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
                            current_state = State.Logical

                        else:
                            tokens.put(Token(_value=buffer, _token_type=TokenType.Identifier,
                                             _line=current_line, _char=current_char - len(buffer)))

                            if current_symbol in DELIMITERS:
                                buffer = current_symbol
                                current_state = State.Delimiter

                            elif current_symbol in ADDSUB:
                                buffer = current_symbol
                                current_state = State.AddSub

                            elif current_symbol in MULDIV:
                                buffer = current_symbol
                                current_state = State.MulDiv

                            elif current_symbol in LOGICAL_OPERATORS:
                                buffer = current_symbol
                                current_state = State.Logical

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
                        number_type = TokenType.UnexpectedCharacter
                        if is_binary(buffer):
                            number_type = TokenType.Binary

                        elif is_octal(buffer):
                            number_type = TokenType.Octal

                        elif is_decimal(buffer):
                            number_type = TokenType.Decimal

                        elif is_hexadecimal(buffer):
                            number_type = TokenType.Hexadecimal

                        elif is_real(buffer):
                            number_type = TokenType.Real

                        if number_type == TokenType.UnexpectedCharacter:
                            current_state = State.Error
                            continue

                        tokens.put(Token(_value=buffer, _token_type=number_type,
                                         _line=current_line, _char=current_char - len(buffer)))

                        if current_symbol in DELIMITERS:
                            buffer = current_symbol
                            current_state = State.Delimiter

                        elif current_symbol in RELATION_SYMBOLS:
                            buffer = current_symbol
                            current_state = State.Relation

                        elif current_symbol in ADDSUB:
                            buffer = current_symbol
                            current_state = State.AddSub

                        elif current_symbol in MULDIV:
                            buffer = current_symbol
                            current_state = State.MulDiv

                        elif current_symbol in WHITESPACES:
                            current_state = State.Start

                        else:
                            current_state = State.Error

                    continue

                case State.Boolean:
                    tokens.put(Token(_value=buffer, _token_type=TokenType.Boolean,
                                     _line=current_line, _char=current_char - len(buffer)))

                    if current_symbol in DELIMITERS:
                        buffer = current_symbol
                        current_state = State.Delimiter

                    elif current_symbol in LOGICAL_OPERATORS:
                        buffer = current_symbol
                        current_state = State.Logical

                    elif current_symbol in WHITESPACES:
                        current_state = State.Start

                    else:
                        current_state = State.Error

                    continue

                case State.MulDiv:
                    tokens.put(Token(_value=buffer, _token_type=TokenType.MulDiv,
                                     _line=current_line, _char=current_char - 1))
                    current_state = State.Start

                    continue

                case State.AddSub:
                    tokens.put(Token(_value=buffer, _token_type=TokenType.AddSub,
                                     _line=current_line, _char=current_char - 1))
                    current_state = State.Start

                    continue

                case State.Relation:
                    current_symbol = program.read(1)
                    current_char += 1

                    if buffer + current_symbol in RELATION_SYMBOLS:
                        buffer += current_symbol
                        tokens.put(Token(_value=buffer, _token_type=TokenType.Relation,
                                         _line=current_line, _char=current_char - 2))
                        current_state = State.Start

                    else:
                        if buffer in RELATION_SYMBOLS:
                            tokens.put(Token(_value=buffer, _token_type=TokenType.Relation,
                                             _line=current_line, _char=current_char - 1))

                        else:
                            current_state = State.Error
                            continue

                        if current_symbol in LETTERS:
                            buffer = current_symbol
                            current_state = State.Identifier

                        elif current_symbol in DIGITS or current_symbol == ".":
                            buffer = current_symbol
                            current_state = State.Number

                        elif current_symbol in WHITESPACES:
                            current_state = State.Start

                        else:
                            current_state = State.Error

                    continue

                case State.Type:
                    tokens.put(Token(_value=buffer, _token_type=TokenType.VariableType,
                                     _line=current_line, _char=current_char - 1))
                    current_state = State.Start

                    continue

                case State.Note:
                    current_symbol = program.read(1)
                    if current_symbol == "}":
                        current_state = State.Start

                    continue

    return tokens


def save_tokens(filename: str, queue: Queue[Token], encoding: str = "utf-8"):
    with open(filename, "w", encoding=encoding) as file:
        while not queue.empty():
            file.write(str(queue.get()) + "\n")
