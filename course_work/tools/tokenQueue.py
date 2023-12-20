from course_work.tools.structures import Token


class TokenQueue:
    """ Implements a token queue """

    def __init__(self):
        self.queue: list[Token] = []

    def put(self, token: Token):
        """ Adds an item to the end of the queue """
        self.queue.append(token)

    def get(self) -> Token:
        """ Returns the first item in the queue and deletes it """
        return self.queue.pop(0)

    def front(self) -> Token:
        """ Returns the first item in the queue """
        return self.queue[0]

    def is_empty(self) -> bool:
        """ Check if the queue is empty """
        return len(self.queue) == 0
