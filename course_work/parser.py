from course_work.tools.tokenQueue import TokenQueue
from course_work.tools.structures import (TokenType,
                                          Token,
                                          IdentifierType,
                                          Identifier,
                                          OPERATIONS)
from course_work.tools.exceptions import (ModelLanguageError,
                                          EmptyProgramError,
                                          EndOfProgramError,
                                          UnexpectedTokenError,
                                          UnexpectedCharacterSequenceError,
                                          AssignmentTypeError,
                                          DeclarationError)


class Parser:
    """ Implementation of the syntactic and semantic analyzer """
    tokens: TokenQueue
    auxiliary_token: Token
    identifier_table: list[Identifier]
    operators_average: int
    note_ongoing: bool

    def __init__(self, _tokens: TokenQueue):
        self.tokens = _tokens
        self.identifier_table = list()

        self.operators_average = 0
        self.note_ongoing = False

    def __call__(self):
        try:
            self.parse()
            print("The program analysis has been successfully completed. No problems were found.")
        except ModelLanguageError as error:
            print(str(error))
            print("The program analysis was terminated with an error.")

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
        identifier_list = list()
        identifiers_type = None

        while not self.tokens.is_empty() and self.tokens.front().token_type == TokenType.IDENTIFIER:
            self.auxiliary_token = self.tokens.front()
            identifier_list.append(self.tokens.get())
            if not self.tokens.is_empty() and self.tokens.front().token_type == TokenType.ARGUMENT_DELIMITER:
                self.tokens.get()

            elif not self.tokens.is_empty() and self.tokens.front().token_type in IdentifierType:
                identifiers_type = self.tokens.get().token_type
                break

            else:
                message = "Identifier or type"
                if not self.tokens.is_empty() and self.tokens.front().token_type == TokenType.IDENTIFIER:
                    message = "Comma"

                raise UnexpectedTokenError(self.tokens.get() if not self.tokens.is_empty()
                                           else Token(_value="nothing was",
                                                      _token_type=TokenType.UNEXPECTED_CHARACTER_SEQUENCE,
                                                      _line=self.auxiliary_token.line,
                                                      _char=self.auxiliary_token.char + len(
                                                          self.auxiliary_token.value)),
                                           message)

        if len(identifier_list) == 0:
            raise UnexpectedTokenError(self.tokens.get() if not self.tokens.is_empty()
                                       else Token(_value="nothing was",
                                                  _token_type=TokenType.UNEXPECTED_CHARACTER_SEQUENCE,
                                                  _line=self.auxiliary_token.line,
                                                  _char=self.auxiliary_token.char + len(self.auxiliary_token.value)),
                                       "Identifier")

        if not identifiers_type:
            raise UnexpectedTokenError(self.tokens.get() if not self.tokens.is_empty()
                                       else Token(_value="nothing was",
                                                  _token_type=TokenType.UNEXPECTED_CHARACTER_SEQUENCE,
                                                  _line=self.auxiliary_token.line,
                                                  _char=self.auxiliary_token.char + len(self.auxiliary_token.value)),
                                       "Type")

        for identifier in identifier_list:
            for existing_id in self.identifier_table:
                if identifier.value == existing_id.name:
                    self.identifier_table.remove(existing_id)
                    break
            self.identifier_table.append(Identifier(_name=identifier.value, _type=identifiers_type))

        if not self.tokens.is_empty() and self.tokens.front().token_type != TokenType.OPERATOR_DELIMITER:
            raise UnexpectedTokenError(self.tokens.get(), "Operator delimiter")

    def check_operator(self):
        """ Checks whether the operator matches the grammar of the language """
        token = self.tokens.front()
        if token == TokenType.BLOCK_START:
            self.check_compound()

        elif token == TokenType.IDENTIFIER:
            self.check_assignment()

        elif token == TokenType.IF:
            self.check_conditional()

        elif token == TokenType.FOR:
            self.check_fixed_cycle()

        elif token == TokenType.WHILE:
            self.check_conditional_cycle()

        elif token == TokenType.READ or token == TokenType.WRITE:
            self.check_read_write()

        if not self.tokens.is_empty() and self.tokens.front().token_type != TokenType.OPERATOR_DELIMITER:
            raise UnexpectedTokenError(self.tokens.get(), "Operator delimiter")

    def check_compound(self):
        """ Checks whether the compound operator matches the grammar of the language """
        pass

    def check_assignment(self):
        """ Checks whether the assignment operator matches the grammar of the language """
        identifier = self.tokens.get()
        if not self.tokens.is_empty() and self.tokens.front().token_type != TokenType.AS:
            raise UnexpectedTokenError(self.tokens.get(), "assignment operator")

        self.tokens.get()
        new_value = None
        if not self.tokens.is_empty():
            new_value = self.check_expression()

        if new_value:
            flag = False
            for existing_id in self.identifier_table:
                if identifier.value == existing_id.name:
                    flag = True
                    existing_id.is_assigned = True
                    existing_id.value = new_value.value
                    if existing_id.type != new_value.type:
                        raise AssignmentTypeError(identifier, new_value.type)

            if not flag:
                raise DeclarationError(identifier)

    def check_conditional(self):
        """ Checks whether the conditional operator matches the grammar of the language """
        pass

    def check_fixed_cycle(self):
        """ Checks whether the fixed cycle operator matches the grammar of the language """
        pass

    def check_conditional_cycle(self):
        """ Checks whether the conditional cycle operator matches the grammar of the language """
        pass

    def check_read_write(self):
        """ Checks whether the read or write operator matches the grammar of the language """
        self.tokens.get()
        if not self.tokens.is_empty() and self.tokens.front().token_type != TokenType.ARGUMENT_START:
            message = "arguments"
            if self.tokens.front().token_type == TokenType.IDENTIFIER:
                message = "opening bracket"

            raise UnexpectedTokenError(self.tokens.get(), message)

        self.tokens.get()
        count = 0
        while not self.tokens.is_empty() and self.tokens.front().token_type == TokenType.IDENTIFIER:
            count += 1
            self.auxiliary_token = self.tokens.get()
            if not self.tokens.is_empty() and self.tokens.front().token_type == TokenType.ARGUMENT_DELIMITER:
                self.tokens.get()

            elif not self.tokens.is_empty() and self.tokens.front().token_type == TokenType.ARGUMENT_END:
                self.tokens.get()
                break

            else:
                message = "Identifier or closing bracket"
                if not self.tokens.is_empty() and self.tokens.front().token_type == TokenType.IDENTIFIER:
                    message = "Comma"

                raise UnexpectedTokenError(self.tokens.get() if not self.tokens.is_empty()
                                           else Token(_value="nothing was",
                                                      _token_type=TokenType.UNEXPECTED_CHARACTER_SEQUENCE,
                                                      _line=self.auxiliary_token.line,
                                                      _char=self.auxiliary_token.char + len(
                                                          self.auxiliary_token.value)),
                                           message)

        if count == 0:
            raise UnexpectedTokenError(self.tokens.get() if not self.tokens.is_empty()
                                       else Token(_value="nothing was",
                                                  _token_type=TokenType.UNEXPECTED_CHARACTER_SEQUENCE,
                                                  _line=self.auxiliary_token.line,
                                                  _char=self.auxiliary_token.char + len(self.auxiliary_token.value)),
                                       "Identifier")

    def check_expression(self) -> Identifier:
        """ Checks if tokens represents an expression, returns expression result (value and type) """
        identifier1 = self.check_operand()
        if (self.tokens.is_empty() or self.tokens.front().token_type not in [TokenType.NOT_EQUALS, TokenType.EQUALS,
                                                                             TokenType.LESS, TokenType.LESS_EQUALS,
                                                                             TokenType.GREATER,
                                                                             TokenType.GREATER_EQUALS]):
            return identifier1

        identifier2 = self.check_operand()

        result = Identifier(_name="", _type=IdentifierType.BOOLEAN)

        return result

    def check_operand(self) -> Identifier:
        """ Checks if tokens represents an operand """
        summand1 = self.check_summand()
        if (self.tokens.is_empty() or self.tokens.front().token_type not in [TokenType.SUBTRACTION,
                                                                             TokenType.ADDITION,
                                                                             TokenType.OR]):
            return summand1

        summand2 = self.check_summand()
        _type = IdentifierType.BOOLEAN
        if summa

        result = Identifier(_name="", _type=_type)
        return result

    def check_summand(self) -> Identifier:
        """ Checks if tokens represents a summand """
        pass

    def check_multiplier(self):
        """ Checks if tokens represents a multiplier """
        token = self.tokens.front()

        if token.token_type != TokenType.ARGUMENT_START:
            if token.token_type != TokenType.NOT:
                if (token.token_type not in [TokenType.IDENTIFIER, TokenType.TRUE, TokenType.FALSE] and
                        not self.check_number()):
                    raise UnexpectedTokenError(token, "identifier or logical constant")
            else:
                self.tokens.get()
                self.check_multiplier()

        else:
            pass

    def check_number(self):
        """ Checks if the token represents a number """
        token = self.tokens.front()
        if not (token.token_type == TokenType.BINARY or token.token_type == TokenType.OCTAL or
                token.token_type == TokenType.DECIMAL or token.token_type == TokenType.HEXADECIMAL or
                token.token_type == TokenType.REAL):
            raise UnexpectedTokenError(token, "number")
