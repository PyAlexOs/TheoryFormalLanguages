def transform(input: list, params: dict = {}) -> list:
    signs = {"*": 3, "/": 3, "+": 2, "-": 2, "(": 1}
    stack = list()
    output = list()

    for symbol in input:
        if symbol == " ":
            continue

        symbol = symbol.strip()
        if symbol.isdigit() or symbol in params.keys():
            output.append(symbol)

        elif symbol == "(":
            stack.append(symbol)

        elif symbol == ")":
            temp = stack.pop()
            while temp != "(":
                output.append(temp)
                temp = stack.pop()

        elif symbol in signs.keys():
            while len(stack) != 0 and signs[stack[-1]] >= signs[symbol]:
                output.append(stack.pop())

            stack.append(symbol)

        else:
            print(f"Can't parse symbol while transforming: {symbol}.")
            exit(0)

    while len(stack) != 0:
        output.append(stack.pop())

    return output


def count_res(input: list, params: dict = {}) -> float:
    stack = list()
    for symbol in input:
        if symbol.isdigit() or symbol in params.keys():
            stack.append(symbol)

        elif symbol in ["*", "/", "+", "-"]:
            a = stack.pop()
            b = stack.pop()

            if a.isalpha():
                a = params[a]
            if b.isalpha():
                b = params[b]

            stack.append(str(eval(b + symbol + a)))

        else:
            print(f"Can't parse symbol while counting: {symbol}.")
            exit(0)

    return float(stack.pop())


def prepare(string: str) -> list:
    substr = ""
    in_list = list()

    for symbol in string:
        if symbol in ["*", "/", "+", "-", "(", ")"]:
            if len(substr) != 0:
                in_list.append(substr)

            in_list.append(symbol)
            substr = ""

        else:
            substr += symbol

    if len(substr) != 0:
        in_list.append(substr)

    return in_list


def main():
    expression = input('Input your equation: ')
    expression = prepare(expression)
    print('enter the values of all variables that participate in the expression (then enter "\\)')

    params = {}
    # params = {'a': '2', 'b': '3'}
    key = input('Enter variable: ')
    while key != "\\":
        params[key] = input('Enter value: ')
        key = input('Enter variable: ')

    result = transform(expression, params)
    print(' '.join(result))
    print(count_res(result, params))


if __name__ == '__main__':
    main()
