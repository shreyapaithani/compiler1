import re



# ------------------  Lexical Analysis ------------------ #
def tokenize(code):
    token_specification = [
        ('NUMBER',   r'\d+'),
        ('ADD',      r'\+'),
        ('SUB',      r'-'),
        ('MUL',      r'\*'),
        ('DIV',      r'/'),
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('SKIP',     r'[ \t]+'),
        ('MISMATCH', r'.')
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            tokens.append(('NUMBER', int(value)))
        elif kind in ('ADD', 'SUB', 'MUL', 'DIV', 'LPAREN', 'RPAREN'):
            tokens.append((kind, value))
        elif kind == 'SKIP':
            continue
        else:
            raise RuntimeError(f'Unexpected character: {value}')
    return tokens


