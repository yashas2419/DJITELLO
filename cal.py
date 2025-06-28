import math
from fractions import Fraction

def custom_calculator(expr):
    try:
        x = float(Fraction(expr))
        if x <= 0:
            return "x must be greater than 0"
        return x * math.log2(x)
    except:
        return "Invalid input"

# Infinite loop
while True:
    expr = input("Enter value of x (e.g., 3/4) or type 'exit' to quit: ").strip()
    if expr.lower() == 'exit':
        break
    result = custom_calculator(expr)
    print(f"x * log2(x) = {result}\n")
