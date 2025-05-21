import tkinter as tk
from tkinter import scrolledtext, messagebox, font
from lexer import lexer
from parser import parser
from semantic import SemanticAnalyzer
from ir_generator import IRGenerator
from optimizer import Optimizer
from executor import Executor

def compile_and_run():
    user_code = code_text.get("1.0", tk.END).strip()
    if not user_code:
        messagebox.showwarning("Warning", "Please enter some C code.")
        return

    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)  # Clear output box

    try:
        ast = parser.parse(user_code, lexer=lexer)
        SemanticAnalyzer().analyze(ast)

        ir = IRGenerator()
        ir.generate(ast)

        output_text.insert(tk.END, "--- Intermediate Code ---\n", "header")
        for line in ir.code:
            output_text.insert(tk.END, line + "\n")

        opt = Optimizer(ir.code)
        opt.optimize()

        output_text.insert(tk.END, "\n--- Optimized Code ---\n", "header")
        for line in opt.get_code():
            output_text.insert(tk.END, line + "\n")

        executor = Executor(opt.get_code())
        result = executor.run()

        output_text.insert(tk.END, f"\nProgram Returned: {result}\n", "result")

    except Exception as e:
        # Try to get line info from error message if possible
        err_msg = str(e)
        line_info = ""
        # Example parsing for ply yacc errors like 'Syntax error at line 3'
        import re
        m = re.search(r'line (\d+)', err_msg, re.IGNORECASE)
        if m:
            line_no = m.group(1)
            line_info = f" on line {line_no}"
        output_text.insert(tk.END, f"\nError{line_info}: {err_msg}\n", "error")

    output_text.config(state=tk.DISABLED)

# Tkinter window setup
root = tk.Tk()
root.title("Mini C Compiler")

# Fonts
header_font = ("Consolas", 12, "bold")
normal_font = ("Consolas", 11)

# Input label
tk.Label(root, text="Enter C code here:", font=header_font).pack(anchor='w', padx=10, pady=(10,0))

# Input text box
code_text = scrolledtext.ScrolledText(root, width=90, height=15, font=normal_font, undo=True)
code_text.pack(padx=10, pady=(0,10))

# Compile & Run button with styling
run_button = tk.Button(root, text="Compile & Run", command=compile_and_run, bg="#4CAF50", fg="white", font=header_font, padx=15, pady=7)
run_button.pack(pady=10)

# Output label
tk.Label(root, text="Output:", font=header_font).pack(anchor='w', padx=10, pady=(10,0))

# Output text box (read-only)
output_text = scrolledtext.ScrolledText(root, width=90, height=15, font=normal_font, state=tk.DISABLED)
output_text.pack(padx=10, pady=(0,10))

# Text tag configurations for coloring output
output_text.tag_config("header", foreground="#0B5394")  # Blue-ish
output_text.tag_config("result", foreground="#38761D")  # Green-ish
output_text.tag_config("error", foreground="#CC0000")   # Red

# Set minimum window size
root.minsize(700, 600)

root.mainloop()
