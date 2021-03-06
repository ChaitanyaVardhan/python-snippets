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
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """ Lexical analyzer
        This breaks up a sentence into tokens
        """
        text = self.text

        #return EOF at end of text
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        #get character in sentence
        current_char = text[self.pos]

        #decide the type of token like INTEGER or PLUS
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token

        if current_char == ' ':
            token = Token(WHITESPACE, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.int_tokens.append(self.current_token)
            self.current_token = self.get_next_token()
        else:
            self.error()

    def eat_ints(self):
        if self.current_token.type == INTEGER:
            self.int_tokens.append(self.current_token)
            self.current_token = self.get_next_token()
            self.eat_ints()

    def eat_oper(self):
        if self.current_token.type == PLUS or MINUS:
            self.current_token = self.get_next_token()
        else:
            self.error()        

    def skip_whitespace(self):
        if self.current_token.type == WHITESPACE:
            self.current_token = self.get_next_token()
            self.skip_whitespace()

    def expr(self):
        """ expr -> INTEGER PLUS INTEGER """
        # get the first token from the input
        self.current_token = self.get_next_token()
        self.skip_whitespace()

        # check if first token is a single digit integer
        self.int_tokens = []
        self.eat(INTEGER)
        self.eat_ints()
        self.left = self.int_tokens
        left = ''
        for token in self.left:
            left += str(token.value)
        self.skip_whitespace()

        # next token should be '+" or "-"
        self.op = self.current_token
        self.eat_oper()
        self.skip_whitespace()

        # next token after '+' should be a single digit integer
        self.int_tokens = []
        self.eat(INTEGER)
        self.eat_ints()
        self.right = self.int_tokens
        right = ''
        for token in self.right:
            right += str(token.value)

        if self.op.type == PLUS:
            result = int(left) + int(right)

        if self.op.type == MINUS:
            result = int(left) - int(right)
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
        print result

if __name__ == '__main__':
    main()
