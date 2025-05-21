from lexer import lexer
from parser import parser
from semantic import SemanticAnalyzer
from ir_generator import IRGenerator
from optimizer import Optimizer
from executor import Executor

print("enter your c code :")

lines = []
while True:
    line = input()
    if line.strip() == "":
        break
    lines.append(line)

user_code = "\n".join(lines)

try:
    # Parse → AST
    ast = parser.parse(user_code, lexer=lexer)

    # Semantic Check
    SemanticAnalyzer().analyze(ast)

    # IR Generation
    ir = IRGenerator()
    ir.generate(ast)

    print("\n--- Intermediate Code ---")
    ir.print_code()

    # Optimization
    opt = Optimizer(ir.code)
    opt.optimize()

    print("\n--- Optimized Code ---")
    for line in opt.get_code():
        print(line)

    # Execute optimized code
    executor = Executor(opt.get_code())
    executor.run()

except Exception as e:
    print("error :", e)