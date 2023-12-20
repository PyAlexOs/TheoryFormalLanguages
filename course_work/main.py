from course_work.file_methods import save_tokens, load_tokens
from course_work.tokenizer import get_tokens
import sys


def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        # exit("Filename wasn't given.")
        filename = "language_files/test/test.lang"

    tokens = get_tokens(filename)
    save_tokens(''.join(filename.split(".")[:-1:]) + ".tokenlist", tokens)
    tokens = load_tokens(''.join(filename.split(".")[:-1:]) + ".tokenlist")
    while not tokens.is_empty():
        a = tokens.get()
        print(a.__repr__())


if __name__ == '__main__':
    main()
