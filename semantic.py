from parser import parser
from lexer import lexer
from parser import Program, Function, Declaration, Return, BinOp, Number, Var

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, node):
        if isinstance(node, Program):
            for fn in node.functions:
                self.analyze(fn)

        elif isinstance(node, Function):
            print(f"Checking function: {node.name}")
            self.symbol_table.clear()
            for stmt in node.body:
                self.analyze(stmt)

        elif isinstance(node, Declaration):
            if node.var_name in self.symbol_table:
                raise Exception(f"Variable '{node.var_name}' already declared")
            self.symbol_table[node.var_name] = node.var_type
            self.analyze(node.value)

        elif isinstance(node, Return):
            self.analyze(node.value)

        elif isinstance(node, BinOp):
            self.analyze(node.left)
            self.analyze(node.right)

        elif isinstance(node, Number):
            pass  # Numbers are valid

        elif isinstance(node, Var):
            if node.name not in self.symbol_table:
                raise Exception(f"Variable '{node.name}' used before declaration")

# --------------- Test ----------------
if __name__ == '__main__':
    code = '''
    int main() {
        int a = 5;
        return a + 10;
    }
    '''
    ast = parser.parse(code, lexer=lexer)
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    print("Semantic Analysis Passed ✅")
