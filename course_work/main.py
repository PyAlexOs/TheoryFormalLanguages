from course_work.tools.file_methods import (save_tokens,
                                            load_tokens,
                                            save_tokens_json,
                                            load_tokens_json)
from course_work.tokenizer import get_tokens
from course_work.parser import Parser
import os
import sys


def main():
    """
        python ./course_work/main.py course_work/language_files/is_even/is_even.lang
        python ./course_work/main.py course_work/language_files/all_tokens/all_tokens.lang
        python ./course_work/main.py course_work/language_files/conditionals/conditionals.lang
        python ./course_work/main.py course_work/language_files/factorial/factorial.lang
        python ./course_work/main.py course_work/language_files/search_for_fraction/search_for_fraction.lang

        for on-go test_module:
        python ./course_work/main.py course_work/language_files/temp/temp.lang
    """
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = input("Enter filename: ")

    if not os.path.exists(filename):
        exit("Path doesn't exist.")

    tokens = get_tokens(filename)
    name = ''.join(filename.split(".")[:-1:])
    # get tokens from program in the filename.lang
    # then write tokens to file, get tokens from the filename.tokenlist or filename.json
    # and parse it

    # save_tokens(name + ".tokenlist", tokens)
    save_tokens_json(name + ".json", tokens)

    # tokens = load_tokens(name + ".tokenlist")
    tokens = load_tokens_json(name + ".json")

    """while not tokens.is_empty():
        print(tokens.get().__repr__())"""

    parser = Parser(tokens)
    parser()


if __name__ == '__main__':
    main()
