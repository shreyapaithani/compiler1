import ply.lex as lex

# List of token names
tokens = [
    'ID', 'NUMBER',
    'PLUS', 'MINUS', 'MULT', 'DIVIDE',
    'ASSIGN', 'EQ', 'LT', 'GT',
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'SEMICOLON', 'COMMA',
    'STRING',
]

# Reserved words (keywords)
reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'return': 'RETURN',
    'void': 'VOID',
}

# Merge reserved with tokens
tokens += list(reserved.values())

# Regular expressions for simple tokens
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_MULT     = r'\*'
t_DIVIDE   = r'/'
t_ASSIGN   = r'='
t_EQ       = r'=='
t_LT       = r'<'
t_GT       = r'>'
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_SEMICOLON= r';'
t_COMMA    = r','

# Strings in double quotes
def t_STRING(t):
    r'\".*?\"'
    t.value = t.value[1:-1]  # remove quotes
    return t

# Identifier and reserved keywords
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for keywords
    return t

# Integer numbers
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignored characters
t_ignore = ' \t\r'

# Newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Error handling
def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")

# Build the lexer
lexer = lex.lex()

# ----------- Test it --------------
if __name__ == '__main__':
    code = '''
    int main() {
        int a = 10;
        printf("Value is %d", a);
        return 0;
    }
    '''
    lexer.input(code)

    for tok in lexer:
        print(tok)




