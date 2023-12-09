from enum import Enum
from os import path, SEEK_SET
import re


def tokenize(filepath: str) -> dict:
    buffer: str
    states = Enum('state', ['h', 'id', 'nm', 'dlm', 'asgn', 'err'])
    tokens = {
        'KEYWORDS': [],
        'DELIMITERS': [],
        'ASSIGN': [],
        'IDs': [],
        'NUMBERS': [],
        'UNKNOWN': []
    }

    with open(filepath, 'r') as file:
        current_state = states['h']
        while symbol := file.read(1):

            match current_state.name:
                case 'h':
                    while symbol in [' ', '\t', '\n']:
                        symbol = file.read(1)
                    if symbol == ':':
                        current_state = states['asgn']
                    elif symbol.isalpha() or symbol == '_':
                        current_state = states['id']
                    elif symbol.isdigit() or symbol in ['-', '+', '.']:
                        current_state = states['nm']
                    elif symbol in ['(', ')', ';', '<', '>', '=']:
                        current_state = states['dlm']
                    buffer = symbol

                case 'asgn':
                    buffer += symbol
                    if symbol == '=':
                        tokens['ASSIGN'].append(buffer)
                    else:
                        tokens['UNKNOWN'].append(buffer)

                    buffer = ''
                    current_state = states['h']

                case 'id':
                    while symbol.isalnum() or symbol == '_':
                        buffer += symbol
                        symbol = file.read(1)

                    if buffer in ['for', 'do']:
                        tokens['KEYWORDS'].append(buffer)
                    else:
                        tokens['IDs'].append(buffer)

                    file.seek(file.tell() - 1, SEEK_SET)
                    current_state = states['h']

                case 'nm':
                    while symbol.isdigit() or symbol in ['.', 'e', 'E', '-', '+']:
                        buffer += symbol
                        symbol = file.read(1)

                    if re.match('^(?!^\s*$)\d*(\.\d+)?((e|E)(-|\+)?\d+)?$', buffer):
                        tokens['NUMBERS'].append(buffer)
                    else:
                        tokens['UNKNOWN'].append(buffer)

                    file.seek(file.tell() - 1, SEEK_SET)
                    current_state = states['h']

                case 'dlm':
                    tokens['DELIMITERS'].append(buffer)
                    file.seek(file.tell() - 1, SEEK_SET)
                    current_state = states['h']

    return tokens


def main():
    filepath = path.abspath(input('Enter filepath: '))  # files/test.txt
    if path.exists(filepath):
        tokens = tokenize(filepath)
    else:
        exit(f"Path {filepath} doesn't exists.")

    for (key, value) in tokens.items():
        print(key, ":", value)


if __name__ == "__main__":
    main()
