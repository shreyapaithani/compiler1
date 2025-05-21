import ply.yacc as yacc
from lexer import tokens

# AST Node Classes
class Program:  # Root node
    def __init__(self, functions):
        self.functions = functions

class Function:
    def __init__(self, name, body):
        self.name = name
        self.body = body

class Declaration:
    def __init__(self, var_type, var_name, value=None):
        self.var_type = var_type
        self.var_name = var_name
        self.value = value

class Return:
    def __init__(self, value):
        self.value = value

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number:
    def __init__(self, value):
        self.value = value

class Var:
    def __init__(self, name):
        self.name = name

# --------------------- Grammar Rules ---------------------

def p_program(p):
    '''program : function'''
    p[0] = Program([p[1]])

def p_function(p):
    '''function : INT ID LPAREN RPAREN LBRACE statements RBRACE'''
    p[0] = Function(p[2], p[6])

def p_statements_multiple(p):
    '''statements : statements statement'''
    p[0] = p[1] + [p[2]]

def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]]

def p_statement_declaration(p):
    '''statement : INT ID ASSIGN expression SEMICOLON'''
    p[0] = Declaration("int", p[2], p[4])

def p_statement_return(p):
    '''statement : RETURN expression SEMICOLON'''
    p[0] = Return(p[2])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULT expression
                  | expression DIVIDE expression'''
    p[0] = BinOp(p[1], p[2], p[3])

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = Number(p[1])

def p_expression_var(p):
    '''expression : ID'''
    p[0] = Var(p[1])

def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at '{p.value}' on line {p.lineno}")
    else:
        raise SyntaxError("Syntax error at EOF")


# --------------------- Build Parser ---------------------

parser = yacc.yacc()

# --------------------- Test Parser ----------------------

if __name__ == '__main__':
    code = '''
    int main() {
        int a = 5;
        return a + 10;
    }
    '''
    result = parser.parse(code)
    print("Parsed Successfully!")

    # Debug AST print
    def print_ast(node, indent=0):
        prefix = "  " * indent
        if isinstance(node, Program):
            print(prefix + "Program")
            for fn in node.functions:
                print_ast(fn, indent + 1)
        elif isinstance(node, Function):
            print(prefix + f"Function: {node.name}")
            for stmt in node.body:
                print_ast(stmt, indent + 1)
        elif isinstance(node, Declaration):
            print(prefix + f"Declaration: {node.var_type} {node.var_name} =")
            print_ast(node.value, indent + 1)
        elif isinstance(node, Return):
            print(prefix + "Return")
            print_ast(node.value, indent + 1)
        elif isinstance(node, BinOp):
            print(prefix + f"BinOp: {node.op}")
            print_ast(node.left, indent + 1)
            print_ast(node.right, indent + 1)
        elif isinstance(node, Number):
            print(prefix + f"Number: {node.value}")
        elif isinstance(node, Var):
            print(prefix + f"Var: {node.name}")

    print_ast(result)
