from course_work.tools.file_methods import (save_tokens,
                                            load_tokens,
                                            save_tokens_json,
                                            load_tokens_json)
from course_work.tokenizer import get_tokens
from course_work.parser import Parser
import os
import sys


def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        # filename = input()
        filename = "language_files/test/test.lang"

    if not os.path.exists(filename):
        exit("Path doesn't exist.")

    tokens = get_tokens(filename)
    # get tokens from program in the filename.lang
    # then write tokens to file, get tokens from the filename.tokenlist or filename.json
    # and parse it

    # save_tokens(''.join(filename.split(".")[:-1:]) + ".tokenlist", tokens)
    save_tokens_json(''.join(filename.split(".")[:-1:]) + ".json", tokens)

    # tokens = load_tokens(''.join(filename.split(".")[:-1:]) + ".tokenlist")
    tokens = load_tokens_json(''.join(filename.split(".")[:-1:]) + ".json")

    """while not tokens.is_empty():
        print(tokens.get().__repr__())"""

    parser = Parser(tokens)
    parser()


if __name__ == '__main__':
    main()
