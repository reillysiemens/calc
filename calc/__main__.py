import argparse
import calc
from calc.interpreter import Interpreter, ParserError


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-v', '--version', action='version',
                            version=calc.__version__)
    arg_parser.parse_args()

    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break

        if not text:
            continue

        interpreter = Interpreter(text)

        try:
            result = interpreter.parse()
            print(result)
        except ParserError as error:
            print(error)


if __name__ == '__main__':
    main()
