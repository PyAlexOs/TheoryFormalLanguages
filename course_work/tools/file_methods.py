from course_work.tools.tokenQueue import TokenQueue
from course_work.tools.structures import TokenType, Token


def save_tokens(filename: str, queue: TokenQueue, encoding: str = "utf-8"):
    with open(filename, "w", encoding=encoding) as file:
        while not queue.is_empty():
            file.write(str(queue.get()) + "\n")


def load_tokens(filename: str, encoding: str = "utf-8") -> TokenQueue:
    tokens = TokenQueue()

    with open(filename, "r", encoding=encoding) as file:
        for line in file.readlines():
            if line != "\n":
                _type, _value, _line, _char = line.split(" ")
                _type, _line, _char = int(_type), int(_line), int(_char)
                tokens.put(Token(_value=_value, _token_type=TokenType(_type), _line=_line, _char=_char))

    return tokens
