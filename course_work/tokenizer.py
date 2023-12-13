from queue import Queue
from token_struct import Token
from states import State
from language_model import KEYWORDS, TYPES, RELATION_SYMBOLS, ADDSUB, MULDIV, DELIMITERS, WHITESPACES, DIGITS, LETTERS


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

                    if current_symbol in WHITESPACES:
                        continue

                    buffer = current_symbol
                    if current_symbol in DELIMITERS:
                        current_state = State.Delimiter

                    elif current_symbol in LETTERS:
                        current_state = State.Identifier

                    elif current_state in DIGITS:
                        current_state = State.Number

                    elif current_symbol in MULDIV:
                        current_state = State.MulDiv

                    elif current_symbol in ADDSUB:
                        current_state = State.AddSub

                    elif current_symbol in RELATION_SYMBOLS:
                        current_state = State.Relation

                    elif current_symbol in TYPES:
                        current_state = State.Type

                    else:
                        current_state = State.Error

                    continue

                case State.Delimiter:
                    tokens.put(Token())

    return tokens


def save_tokens(filename: str, queue: Queue[Token], encoding: str = "utf-8"):
    with open(filename, "w", encoding=encoding) as file:
        while not queue.empty():
            file.write(str(queue.get()) + "\n")
