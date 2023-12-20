from course_work.tools.file_methods import save_tokens, load_tokens
from course_work.tokenizer import get_tokens
from course_work.parser import Parser
import sys


def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        # exit("Filename wasn't given.")
        filename = "language_files/test/test.lang"

    # get tokens from program in the "filename".lang and write it down to the "filename".tokenlist
    tokens = get_tokens(filename)
    save_tokens(''.join(filename.split(".")[:-1:]) + ".tokenlist", tokens)

    # get tokens from the "filename".tokenlist and parse it
    tokens = load_tokens(''.join(filename.split(".")[:-1:]) + ".tokenlist")

    """while not tokens.is_empty():
        print(tokens.get().__repr__())"""

    parser = Parser(tokens)
    parser.parse()


if __name__ == '__main__':
    main()
