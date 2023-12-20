from course_work.tools.tokenQueue import TokenQueue
from course_work.tools.structures import (TokenType,
                                          Token,
                                          IdentifierType,
                                          Identifier)
from course_work.tools.Exceptions import (EmptyProgramError,
                                          EndOfProgramError,
                                          UnexpectedTokenError,
                                          UnexpectedCharacterSequenceError)


class Parser:
    """ Implementation of the syntactic and semantic analyzer """

    def __init__(self, _tokens: TokenQueue):
        self.tokens = _tokens
        self.IdentifierTable: set[Identifier] = set()
        self.previousToken: Token

    def parse(self):
        """ Starts analyzing the program, checks if the program is empty """
        # TODO NOTE HANDLING
        if self.tokens.is_empty() or self.tokens.size() == 1 and self.tokens.front().token_type == TokenType.END:
            raise EmptyProgramError

        self.check_program()
        if self.tokens.is_empty():
            raise EndOfProgramError()

        self.tokens.get()
        if not self.tokens.is_empty():
            raise EndOfProgramError(self.tokens.get().value)

    def check_program(self):
        """ Checks whether the program matches the grammar of the language """
        while not self.tokens.is_empty() and self.tokens.front().token_type != TokenType.END:
            if self.tokens.front().token_type == TokenType.OPERATOR_DELIMITER:
                self.tokens.get()
                continue

            if self.tokens.front().token_type == TokenType.DIM:
                self.check_description()

            elif (self.tokens.front().token_type in [TokenType.BLOCK_START, TokenType.IDENTIFIER,
                                                     TokenType.IF, TokenType.FOR, TokenType.WHILE,
                                                     TokenType.READ, TokenType.WRITE]):
                self.check_operator()

            else:
                if self.tokens.front().token_type == TokenType.UNEXPECTED_CHARACTER_SEQUENCE:
                    raise UnexpectedCharacterSequenceError(self.tokens.get())
                raise UnexpectedTokenError(self.tokens.get())

    def check_description(self):
        """ Checks whether the description operation matches the grammar of the language """
        self.tokens.get()

    def check_operator(self):
        """ Checks whether the operator matches the grammar of the language """
        self.tokens.get()
