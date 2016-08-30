import unittest

from calc.interpreter import INTEGER, PLUS, EOF, Token, Interpreter, ParserError


class TestInterpreter(unittest.TestCase):
    def test_tokenizes_single_digits(self):
        interpreter = Interpreter('0')
        self.assertEqual(interpreter.get_next_token(), Token(INTEGER, 0))
        interpreter = Interpreter('9')
        self.assertEqual(interpreter.get_next_token(), Token(INTEGER, 9))

    def test_tokenizes_plus(self):
        interpreter = Interpreter('+')
        self.assertEqual(interpreter.get_next_token(), Token(PLUS, '+'))

    def test_tokenizes_eof(self):
        interpreter = Interpreter('')
        self.assertEqual(interpreter.get_next_token(), Token(EOF, None))

    def test_raises_parser_error_on_invalid_input(self):
        interpreter = Interpreter('a')
        self.assertRaises(ParserError, interpreter.get_next_token)

    def test_raises_parser_error_on_unexpected_token(self):
        # Instantiate an "empty" ``Interpreter`` and manually set its token.
        interpreter = Interpreter('')
        interpreter.current_token = Token(INTEGER, 0)

        # Assert a ``ParserError`` is raised if the wrong token is consumed.
        self.assertRaises(ParserError, interpreter._consume, PLUS)
