import json
from .tokenQueue import TokenQueue
from .structures import (IdentifierType,
                        TYPES,
                        TokenType,
                        Token)


def save_tokens(filename: str, queue: TokenQueue, encoding: str = "utf-8"):
    """ Writes the transferred tokens to a file with the possibility of recovery in memory """
    with open(filename, "w", encoding=encoding) as file:
        while not queue.is_empty():
            file.write(str(queue.get()) + "\n")


def load_tokens(filename: str, encoding: str = "utf-8") -> TokenQueue:
    """ Downloads (restores) tokens from the file """
    tokens = TokenQueue()

    with open(filename, "r", encoding=encoding) as file:
        for line in file.readlines():
            if line != "\n":
                _type, _value, _line, _char = line.split(" ")
                _type, _line, _char = int(_type), int(_line), int(_char)

                if _value in TYPES.keys():
                    tokens.put(Token(_value=_value, _token_type=IdentifierType(_type), _line=_line, _char=_char))
                else:
                    tokens.put(Token(_value=_value, _token_type=TokenType(_type), _line=_line, _char=_char))

    return tokens


def save_tokens_json(filename, queue: TokenQueue, encoding: str = "utf-8"):
    """ Writes the transferred tokens to a json-file with the possibility of recovery in memory """
    with open(filename, 'w', encoding=encoding) as file:
        token_dict = dict()

        count = 0
        while not queue.is_empty():
            token = queue.get()
            token_dict[count] = {"value": token.value,
                                 "type": token.token_type.value,
                                 "line": token.line,
                                 "char": token.char}
            count += 1

        json.dump(token_dict, file)


def load_tokens_json(filename: str, encoding: str = "utf-8") -> TokenQueue:
    """ Downloads (restores) tokens from the json-file """
    tokens = TokenQueue()

    with open(filename, "r", encoding=encoding) as file:
        token_dict = json.load(file)

    for token in token_dict.values():
        _type = TokenType(token["type"])
        if token["value"] in TYPES:
            _type = IdentifierType(token["type"])

        tokens.put(Token(_value=token["value"],
                         _token_type=_type,
                         _line=token["line"],
                         _char=token["char"]))

    return tokens
