# EOF (end-of-file) indicates no more input for lexical analysis.
INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'


class ParserError(Exception):
    """Exception raised when the parser encounters an error."""
    pass


class Token:
    """A calculator token.

    Attributes:
        kind (str): The kind, or type, of the token. Valid kinds are currently
            ``INTEGER``, ``PLUS``, ``MINUS``, and ``EOF``.
        value (str): The value of the token. Valid values are currently
            non-negative integers, ``+``, ``-``, or ``None``.
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
        current_char (str): The character in ``text`` indexed by ``pos``.
    """

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos] if self.text else None

    def __repr__(self):
        """The unambiguous string representation of an ``Interpreter``."""

        return "Interpreter({text}, {pos}, {current_token})".format(
            text=repr(self.text),
            pos=repr(self.pos),
            current_token=repr(self.current_token)
        )

    def _advance(self):
        """Advance the ``pos`` index and set the ``current_char`` variable."""

        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def _skip_whitespace(self):
        """Ignore whitespace in ``text``."""

        while self.current_char is not None and self.current_char.isspace():
            self._advance()

    def _integer(self):
        """Consume a integer from ``text``.

        Note:
            Handles single and multidigit integers.

        Returns:
            result (int): The integer value of a contiguous set of digits.
        """

        result = []
        while self.current_char is not None and self.current_char.isdigit():
            result.append(self.current_char)
            self._advance()
        return int(''.join(result))

    def _get_next_token(self):
        """Tokenize the next token in the input string.

        Returns:
            token (Token): The next token.

        Raises:
            ParserError: If the next token is not a valid token. The position of
                the invalid token is also given by this ``ParserError``.
        """

        while self.current_char is not None:

            # If the current character is a space, then ignore it and any
            # additional spaces until the next token of consequence.
            if self.current_char.isspace():
                self._skip_whitespace()
                continue

            # If the current character is a digit, then convert it to an
            # integer, create an INTEGER token, advance self.pos, and return the
            # INTEGER token.
            if self.current_char.isdigit():
                return Token(INTEGER, self._integer())

            # If the current character is a + operator, then create a PLUS
            # token, advance self.pos, and return the PLUS token.
            if self.current_char == '+':
                self._advance()
                return Token(PLUS, '+')

            # If the current character is a - operator, then create a MINUS
            # token, advance self.pos, and return the MINUS token.
            if self.current_char == '-':
                self._advance()
                return Token(MINUS, '-')

            raise ParserError("Invalid token at position {pos}".format(
                pos=self.pos
            ))

        # If the current character is None, then self.pos is beyond the end of
        # self.text. We should return EOF, because nothing remains to tokenize.
        return Token(EOF, None)

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
            self.current_token = self._get_next_token()
        else:
            raise ParserError(("Expected {token_kind} at position {pos}, "
                               "found {current_token}").format(
                                   token_kind=token_kind,
                                   pos=self.pos,
                                   current_token=self.current_token.kind))

    def parse(self):
        """Parse arithmetic expressions.

        Note:
            Valid expressions are currently of the form
                INTEGER PLUS INTEGER
            or
                INTEGER MINUS INTEGER

        Returns:
            result (int): The result of evaluating the arithmetic expression.
        """

        # Get the first token.
        self.current_token = self._get_next_token()

        # We expect the next token to be an integer.
        left = self.current_token
        self._consume(INTEGER)

        # We expect the next token to be a + or - operator.
        op = self.current_token
        if op.kind == PLUS:
            self._consume(PLUS)
        else:
            self._consume(MINUS)

        # We expect the next token to be an integer.
        right = self.current_token
        self._consume(INTEGER)

        # At this point we have successfully found a sequence of tokens
        # representing either integer addition or integer subtraction and can
        # perform the corresponding operation, thereby interpretting the input.
        if op.kind == PLUS:
            result = left.value + right.value
        else:
            result = left.value - right.value
        return result
