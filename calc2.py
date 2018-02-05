#code adapted from github: rspivak/lsbasi

INTEGER, PLUS, MINUS, EOF, WHITESPACE = 'INTEGER', 'PLUS', 'MINUS', 'EOF', ' '

class Token(object):
    def __init__(self, type, value):
        #token type: INTEGER, PLUS or EOF
        self.type = type
        #token value: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+' and None
        self.value = value

    def __str__(self):
        """ string representation of the class instance
        Examples: Token(PLUS, +), Token(INTEGER, 9)
        """
        return 'Token({type}, {value})'.format(
            type = self.type, value=self.value)

    def __repr__(self):
        return self.__str__()



class Interpreter(object):
    def __init__(self, text):
        #client input string e.g. "3 + 5" "45 - 78" etc
        self.text = text
        #self.pos in an index into self.text
        self.pos = 0
        #current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        """ advance the pos pointer and set the current_char variable """
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """ Return a multidigit integer consumed from the input """
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """ Lexical analyzer that breaks a text up into tokens """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            self.error()

        return Token(EOF, None)

    def eat(self, token_type):
        """ verify the type of the token. If
        token is of the correct type then get the
        next token, otherwise raise an exception """
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """ parser/Interpreter
        expr -> INTEGER PLUS INTEGER
        expr -> INTEGER MINUS INTEGER
        """
        self.current_token = self.get_next_token()

        #the current token should be an integer
        left = self.current_token
        self.eat(INTEGER)

        #this token should be a plus or minus
        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        else:
            self.eat(MINUS)

        #this token should be an integer
        right = self.current_token
        self.eat(INTEGER)
        #after the above call the current_token is set to be EOF

        #At this point INTEGER PLUS INTEGER or INTEGER MINUS INTEGER 
        #sequence of tokens has been found.
        if op.type == PLUS:
            result = left.value + right.value
        else:
            result = left.value - right.value
        return result



def main():
    while True:
        try:
            text = raw_input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)



if __name__ == '__main__':
    main()


