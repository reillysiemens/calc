import os
import sys
import stat
import argparse
import calc
from calc.interpreter import Interpreter, ParserError


def interpret(text):
    """Pass input ``text`` to a new ``Interpreter``.

    Args:
        text (str): The text to be interpreted.
    """

    interpreter = Interpreter(text)
    try:
        result = interpreter.parse()
        print(result)
    except ParserError as error:
        print(error)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-v', '--version', action='version',
                            version=calc.__version__)
    arg_parser.parse_args()

    # If input is coming from stdin interpret that, otherwise be interactive.
    # Much thanks to Stack Overflow: http://stackoverflow.com/a/13443424/3288364
    mode = os.fstat(0).st_mode
    if stat.S_ISFIFO(mode):
        text = ''.join(line for line in sys.stdin)
        interpret(text)
    else:
        while True:
            try:
                text = input('calc> ')
            except EOFError:
                break

            if not text:
                continue

            interpret(text)


if __name__ == '__main__':
    main()
