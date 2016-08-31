import unittest

from calc.interpreter import (INTEGER, PLUS, MINUS, EOF, Token, Interpreter,
                              ParserError)


class TestInterpreter(unittest.TestCase):
    def test_addition(self):
        interpreter = Interpreter('4 + 3')
        result = interpreter.parse()
        self.assertEqual(result, 7)

    def test_subtraction(self):
        interpreter = Interpreter('4 - 3')
        result = interpreter.parse()
        self.assertEqual(result, 1)

    def test_raises_parser_error_on_invalid_input(self):
        interpreter = Interpreter('a')
        self.assertRaises(ParserError, interpreter._get_next_token)

    def test_raises_parser_error_on_unexpected_token(self):
        # Instantiate an "empty" ``Interpreter`` and manually set its token.
        interpreter = Interpreter('')
        interpreter.current_token = Token(INTEGER, 0)

        # Assert a ``ParserError`` is raised if the wrong token is consumed.
        self.assertRaises(ParserError, interpreter._consume, PLUS)
