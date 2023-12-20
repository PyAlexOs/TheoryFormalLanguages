from course_work.structures import (State,
                                    Token,
                                    TokenType,
                                    DELIMITERS,
                                    LETTERS,
                                    DIGITS,
                                    EXTENDED_DIGITS,
                                    WHITESPACES,
                                    TYPES,
                                    KEYWORDS,
                                    IdentifierType,
                                    Identifier)
from course_work.tokenQueue import TokenQueue


def parse(tokens: str, encoding: str = "utf-8"):
    tokens: InspectedQueue[Lexem] = load_lexems_list(tokens_filename, encoding)
    parser: Parser = Parser(tokens)
    parser.parse()
