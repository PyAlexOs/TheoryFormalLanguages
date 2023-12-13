import re


class Checker:
    @staticmethod
    def is_identifier(token: str) -> bool:
        """ Checks if the token is identifier """
        return re.match(r"^[a-zA-Z][a-zA-Z0-9]*]$", token) is not None

    @staticmethod
    def is_binary(token: str) -> bool:
        """ Checks if the token is binary """
        return re.match(r"^[01]+[Bb]$", token) is not None

    @staticmethod
    def is_octal(token: str) -> bool:
        """ Checks if the token is octal """
        return re.match(r"^[0-7]+[Oo]$", token) is not None

    @staticmethod
    def is_decimal(token: str) -> bool:
        """ Checks if the token is decimal """
        return re.match(r"^\d+[Dd]$", token) is not None

    @staticmethod
    def is_hexadecimal(token: str) -> bool:
        """ Checks if the token is hexadecimal """
        return re.match(r"^\d[0-9a-fA-F]*[Hh]$", token) is not None

    @staticmethod
    def is_integer(token: str) -> bool:
        """ Checks if the token is integer """
        return (Checker.is_binary(token) or Checker.is_octal(token)
                or Checker.is_decimal(token) or Checker.is_hexadecimal(token))

    @staticmethod
    def is_real(token: str) -> bool:
        """ Checks if the token is real """
        return re.match(r"^(\d+[Ee][+-]?\d+)|(\d*\.\d+([Ee][+-]?\d+)?)$", token) is not None

    @staticmethod
    def is_number(token: str) -> bool:
        """ Checks if the token is number """
        return Checker.is_integer(token) or Checker.is_real(token)

    @staticmethod
    def is_logical_constant(token: str) -> bool:
        """ Checks if the token is logical constant """
        return re.match(r"^true|false$", token) is not None

    @staticmethod
    def is_multiplier(token: str) -> bool: # TODO not - проверяй следующий
        pass

    @staticmethod
    def is_summand(token: str) -> bool:
        pass

    @staticmethod
    def is_operand(token: str) -> bool:
        pass

    @staticmethod
    def is_expression(token: str) -> bool:
        pass
