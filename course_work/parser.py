from course_work.tools.tokenQueue import TokenQueue
from course_work.tools.structures import (TokenType,
                                          Token,
                                          IdentifierType,
                                          Identifier)
from course_work.tools.Exceptions import (ModelLanguageError,
                                          EmptyProgramError,
                                          EndOfProgramError,
                                          UnexpectedTokenError,
                                          UnexpectedCharacterSequenceError)


class Parser:
    """ Implementation of the syntactic and semantic analyzer """
    tokens: TokenQueue
    auxiliary_token: Token
    identifier_table: set[Identifier]
    operators_average: int
    note_ongoing: bool

    def __init__(self, _tokens: TokenQueue):
        self.tokens = _tokens
        self.identifier_table = set()

        self.operators_average = 0
        self.note_ongoing = False

    def __call__(self):
        try:
            self.parse()
        except ModelLanguageError as error:
            print(str(error))
        print("The program analysis has been successfully completed. No problems were found.")

    def parse(self):
        """ Starts analyzing the program, checks if the program is empty """
        if self.tokens.is_empty() or self.tokens.size() == 1 and self.tokens.front().token_type == TokenType.END:
            raise EmptyProgramError

        self.check_program()
        # There are no more tokens in the program or a final token has been detected,
        # after which only operator separators can be used

        if self.tokens.is_empty():
            raise EndOfProgramError

        elif self.operators_average < 1:
            raise EmptyProgramError

        self.tokens.get()
        while not self.tokens.is_empty():
            next_token = self.tokens.get()
            if next_token.token_type != TokenType.OPERATOR_DELIMITER:
                raise EndOfProgramError(next_token)

    def check_program(self):
        """ Checks whether the program matches the grammar of the language """
        while not self.tokens.is_empty() and self.tokens.front().token_type != TokenType.END:
            self.note_ongoing = False
            if self.tokens.front().token_type == TokenType.OPERATOR_DELIMITER:
                self.tokens.get()
                continue

            if self.tokens.front().token_type == TokenType.DIM:
                self.operators_average += 1
                self.check_description()

            elif (self.tokens.front().token_type in [TokenType.BLOCK_START, TokenType.IDENTIFIER,
                                                     TokenType.IF, TokenType.FOR, TokenType.WHILE,
                                                     TokenType.READ, TokenType.WRITE]):
                self.operators_average += 1
                self.check_operator()

            elif self.tokens.front().token_type == TokenType.NOTE_START:
                self.note_ongoing = True
                self.tokens.get()
                if not self.tokens.is_empty():
                    next_token = self.tokens.get()
                    if next_token.token_type != TokenType.NOTE_END:
                        raise UnexpectedTokenError(next_token, "End of note")

            else:
                if self.tokens.front().token_type == TokenType.UNEXPECTED_CHARACTER_SEQUENCE:
                    raise UnexpectedCharacterSequenceError(self.tokens.get())
                raise UnexpectedTokenError(self.tokens.get(), "Description or operator")

    def check_description(self):
        """ Checks whether the description operation matches the grammar of the language """
        self.auxiliary_token = self.tokens.get()
        identifier_set = list()
        identifiers_type = None

        while not self.tokens.is_empty() and self.tokens.front().token_type == TokenType.IDENTIFIER:
            identifier_set.append(self.tokens.get())
            if not self.tokens.is_empty() and self.tokens.front().token_type == TokenType.ARGUMENT_DELIMITER:
                self.tokens.get()

            elif not self.tokens.is_empty() and self.tokens.front().token_type in IdentifierType:
                identifiers_type = self.tokens.get().token_type
                break

            else:
                raise UnexpectedTokenError(self.tokens.get() if not self.tokens.is_empty()
                                           else Token(_value="nothing was",
                                                      _token_type=TokenType.UNEXPECTED_CHARACTER_SEQUENCE,
                                                      _line=self.auxiliary_token.line,
                                                      _char=self.auxiliary_token.char + len(
                                                          self.auxiliary_token.value)),
                                           "identifier or type")

        if len(identifier_set) == 0:
            raise UnexpectedTokenError(self.tokens.get() if not self.tokens.is_empty()
                                       else Token(_value="nothing was",
                                                  _token_type=TokenType.UNEXPECTED_CHARACTER_SEQUENCE,
                                                  _line=self.auxiliary_token.line,
                                                  _char=self.auxiliary_token.char + len(self.auxiliary_token.value)),
                                       "identifier")

        if not identifiers_type:
            raise UnexpectedTokenError(self.tokens.get() if not self.tokens.is_empty()
                                       else Token(_value="nothing was",
                                                  _token_type=TokenType.UNEXPECTED_CHARACTER_SEQUENCE,
                                                  _line=self.auxiliary_token.line,
                                                  _char=self.auxiliary_token.char + len(self.auxiliary_token.value)),
                                       "type")

        for identifier in set(identifier_set):
            for existing_id in self.identifier_table:
                if identifier.value == existing_id.name:
                    self.identifier_table.remove(existing_id)
                    break
            self.identifier_table.add(Identifier(_name=identifier.value, _type=identifiers_type))

    def check_operator(self):
        """ Checks whether the operator matches the grammar of the language """
        self.tokens.get()
