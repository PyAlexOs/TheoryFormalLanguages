from tokenizer import get_tokens, save_tokens
import sys


def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        exit("Filename wasn't given.")

    tokens = get_tokens(filename)
    save_tokens(filename, tokens)


if __name__ == '__main__':
    main()
