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
                                          OperationError,
                                          PredicateTypeError,
                                          AssignmentTypeError,
                                          DeclarationError,
                                          ReferencedBeforeAssignmentError)


# TODO переделать чтобы тип результата брался по другому


class Parser:
    """ Implementation of the syntactic and semantic analyzer """
    tokens: TokenQueue
    auxiliary_token: Token
    identifier_table: list[Identifier]
    operators_average: int
    note_ongoing: bool
    waiting_for: IdentifierType

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
                print(self.tokens.front().token_type)
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
        if token.token_type == TokenType.BLOCK_START:
            self.check_compound()

        elif token.token_type == TokenType.IDENTIFIER:
            self.check_assignment()

        elif token.token_type == TokenType.IF:
            self.check_conditional()

        elif token.token_type == TokenType.FOR:
            self.check_fixed_cycle()

        elif token.token_type == TokenType.WHILE:
            self.check_conditional_cycle()

        elif token.token_type == TokenType.READ or token == TokenType.WRITE:
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
        flag = False
        for existing_id in self.identifier_table:
            if identifier.value == existing_id.name:
                flag = True
                self.waiting_for = existing_id.type

        if not flag:
            raise DeclarationError(identifier)

        new_value = self.check_expression()
        if new_value:
            for existing_id in self.identifier_table:
                if identifier.value == existing_id.name:
                    existing_id.is_assigned = True
                    if existing_id.type != new_value.type:
                        raise AssignmentTypeError(identifier, new_value.type, existing_id.type)

    def check_conditional(self):
        """ Checks whether the conditional operator matches the grammar of the language """
        line = self.tokens.front().line
        char = self.tokens.get().char
        expression = self.check_expression()

        if expression.type != IdentifierType.BOOLEAN:
            raise PredicateTypeError(expression.type, line, char)

        if not self.tokens.is_empty() and self.tokens.front().token_type != TokenType.THEN:
            raise UnexpectedTokenError(self.tokens.get(), "then")

        self.tokens.get()
        self.check_operator()
        if not self.tokens.is_empty() and self.tokens.front().token_type == TokenType.ELSE:
            self.tokens.get()
            self.check_operator()

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

        operator = self.tokens.get()
        identifier2 = self.check_operand()
        result = Identifier(_name="",
                            _type=OPERATIONS[operator.token_type][1][
                                OPERATIONS[operator.token_type][0].index(
                                    [identifier1.type.name, identifier2.type.name])])

        return result

    def check_operand(self) -> Identifier:
        """ Checks if tokens represents an operand """
        summand1 = self.check_summand()
        if (self.tokens.is_empty() or self.tokens.front().token_type not in [TokenType.SUBTRACTION,
                                                                             TokenType.ADDITION,
                                                                             TokenType.OR]):
            return summand1

        operator = self.tokens.get()
        summand2 = self.check_summand()
        result = Identifier(_name="",
                            _type=OPERATIONS[operator.token_type][1][
                                OPERATIONS[operator.token_type][0].index([summand1.type.name, summand2.type.name])])

        return result

    def check_summand(self) -> Identifier:
        """ Checks if tokens represents a summand """
        multiplier1 = self.check_multiplier()
        if (self.tokens.is_empty() or self.tokens.front().token_type not in [TokenType.MULTIPLICATION,
                                                                             TokenType.DIVISION,
                                                                             TokenType.AND]):
            return multiplier1

        operator = self.tokens.get()
        multiplier2 = self.check_multiplier()
        result = Identifier(_name="",
                            _type=OPERATIONS[operator.token_type][1][
                                OPERATIONS[operator.token_type][0].index(
                                    [multiplier1.type.name, multiplier2.type.name])])

        return result

    def check_multiplier(self) -> Identifier:
        """ Checks if tokens represents a multiplier """
        if not self.tokens.is_empty() and self.tokens.front() == TokenType.ARGUMENT_START:
            self.tokens.get()
            multiplier = self.check_expression()
            if not self.tokens.is_empty() and not self.tokens.front() == TokenType.ARGUMENT_END:
                raise UnexpectedTokenError(self.tokens.get(), "closing bracket")

            return multiplier

        elif not self.tokens.is_empty() and self.tokens.front() == TokenType.NOT:
            self.tokens.get()
            return self.check_multiplier()

        elif not self.tokens.is_empty() and self.tokens.front() in [TokenType.FALSE, TokenType.TRUE]:
            self.tokens.get()
            return Identifier(_name="", _type=IdentifierType.BOOLEAN)

        elif not self.tokens.is_empty() and self.tokens.front().token_type == TokenType.IDENTIFIER:
            token = self.tokens.get()
            _type = None
            flag = False

            for existing_id in self.identifier_table:
                if existing_id.name == token.value:
                    flag = True
                    _type = existing_id.type
                    break

            if not flag:
                raise ReferencedBeforeAssignmentError(token)

            return Identifier(_name="", _type=_type)

        elif not self.tokens.is_empty() and self.tokens.front().token_type in [TokenType.BINARY, TokenType.OCTAL,
                                                                               TokenType.DECIMAL, TokenType.HEXADECIMAL,
                                                                               TokenType.REAL]:
            token = self.tokens.get()
            _type = IdentifierType.INTEGER
            if token.token_type == TokenType.REAL:
                _type = IdentifierType.REAL

            return Identifier(_name="", _type=_type)

        else:
            raise UnexpectedTokenError(self.tokens.get() if not self.tokens.is_empty()
                                       else Token(_value="nothing was",
                                                  _token_type=TokenType.UNEXPECTED_CHARACTER_SEQUENCE,
                                                  _line=-1,
                                                  _char=-1),
                                       self.waiting_for.name.lower())
