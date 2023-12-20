from course_work.tools.tokenQueue import TokenQueue


class Parser:
    """ Implementation of the syntactic and semantic analyzer """
    def __init__(self, _tokens: TokenQueue):
        self.tokens = _tokens
        self.IdTable = set()

    def parse(self):
        """ Checks whether the program matches the grammar of the language """
        pass

    def check_description(self):
        """ Checks whether the description operation matches the grammar of the language """
        pass
