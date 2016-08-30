# EOF (end-of-file) indicates no more input for lexical analysis.
INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'


class ParserError(Exception):
    """Exception raised when the parser encounters an error."""
    pass


class Token:
    """A calculator token.

    Attributes:
        kind (str): The kind, or type, of the token. Valid kinds are currently
            ``INTEGER``, ``PLUS``, and ``EOF``.
        value (str): The value of the token. Valid values are currently
            integers 0-9, +, or None.
    """

    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __repr__(self):
        """The unambiguous string representation of a ``Token``."""

        return "Token({kind}, {value})".format(kind=self.kind,
                                               value=repr(self.value))

    def __eq__(self, other):
        """Test ``Token`` equality."""

        if self.kind == other.kind and self.value == other.value:
            return True
        else:
            return False


class Interpreter:
    """An interpreter for a simple calculator.

    Attributes:
        text (str): The input string, e.g. ``'3+5'``.
        pos (int): An index into ``text`` indicating the intepreter's position.
        current_token (Token): The current ``Token`` instance.
    """

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None

    def __repr__(self):
        """The unambiguous string representation of an ``Interpreter``."""

        return "Interpreter({text}, {pos}, {current_token})".format(
            text=repr(self.text),
            pos=repr(self.pos),
            current_token=repr(self.current_token)
        )

    def get_next_token(self):
        """Tokenize the next token in the input string.

        Returns:
            token (Token): The next token.

        Raises:
            ParserError: If the next token is not a valid token. The position of
                the invalid token is also given by this ``ParserError``.
        """

        # Is self.pos past the end of self.text? If so, then return EOF, because
        # there is no more input to tokenize.
        if self.pos > len(self.text) - 1:
            return Token(EOF, None)

        # Get the current character at the self.pos index in self.text.
        current_char = self.text[self.pos]

        # If the character is a digit, then convert it to an integer, create an
        # INTEGER token, increment self.pos, and return the INTEGER token.
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        # If the character is a + operator, then create a PLUS token, increment
        # self.pos, and return the PLUS token.
        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        raise ParserError("Invalid token at position {pos}".format(
            pos=self.pos
        ))

    def _consume(self, token_kind):
        """Consume the current token if its kind matches ``token_kind``.

        Args:
            token_kind (str): The expected kind of the current_token. Valid
                kinds are currently ``INTEGER``, ``PLUS``, and ``EOF``.

        Raises:
            ParserError: If the ``current_token`` kind does not match
                ``token_kind``.
        """

        if self.current_token.kind == token_kind:
            self.current_token = self.get_next_token()
        else:
            raise ParserError(("Expected {token_kind} at position {pos}, "
                               "found {current_token}").format(
                                   token_kind=token_kind,
                                   pos=self.pos,
                                   current_token=self.current_token.kind))

    def parse(self):
        """Parse arithmetic expressions.

        Returns:
            result (int): The result of evaluating the arithmetic expression.
        """

        # Get the first token.
        self.current_token = self.get_next_token()

        # We expect the next token to be a single-digit integer.
        left = self.current_token
        self._consume(INTEGER)

        # We expect the next token to be a '+' operator. Since we don't
        # currently use the operator we simply consume the token and move on.
        self._consume(PLUS)

        # We expect the next token to be a single-digit integer.
        right = self.current_token
        self._consume(INTEGER)

        result = left.value + right.value
        return result
