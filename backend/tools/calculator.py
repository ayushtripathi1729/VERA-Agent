import math
import re
from langchain_core.tools import tool

# 🔐 Strict allowed math functions
SAFE_FUNCTIONS = {
    "abs": abs,
    "round": round,
    "sqrt": math.sqrt,
    "log": math.log,
    "log10": math.log10,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "pi": math.pi,
    "e": math.e,
    "pow": pow
}

# 🔍 Safe expression validation
SAFE_PATTERN = re.compile(r"^[0-9\.\+\-\*\/\^\(\)\s,a-zA-Z]+$")


# -------------------- TOOLS --------------------

@tool
def basic_compute(expression: str) -> str:
    """
    Safely evaluates mathematical expressions.
    Example: 'sqrt(144) + log10(100)'
    """
    try:
        if not expression or not SAFE_PATTERN.match(expression):
            return "COMPUTE_ERROR: Invalid or unsafe expression."

        expression = expression.replace("^", "**")

        result = eval(expression, {"__builtins__": None}, SAFE_FUNCTIONS)
        return str(result)

    except Exception as e:
        return f"COMPUTE_ERROR: {str(e)}"


@tool
def modular_inverse(a: int, m: int) -> str:
    """
    Computes modular inverse using Python's pow().
    """
    try:
        if m == 0:
            return "ERROR: Modulus cannot be zero."

        result = pow(a, -1, m)
        return str(result)

    except ValueError:
        return f"No modular inverse exists (gcd({a}, {m}) ≠ 1)."
    except Exception as e:
        return f"ERROR: {str(e)}"


@tool
def primality_test(n: int) -> str:
    """
    Efficient primality test.
    """
    try:
        if n < 2:
            return f"{n} is not prime."

        if n in (2, 3):
            return f"{n} is prime."

        if n % 2 == 0:
            return f"{n} is composite (divisible by 2)."

        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return f"{n} is composite."
            i += 6

        return f"{n} is prime."

    except Exception as e:
        return f"ERROR: {str(e)}"


@tool
def erdos_straus_check(n: int) -> str:
    """
    Attempts Erdős–Straus decomposition: 4/n = 1/x + 1/y + 1/z
    """
    try:
        if n < 2:
            return "Invalid input: n must be ≥ 2."

        LIMIT = 500

        for x in range(1, LIMIT):
            for y in range(x, LIMIT):
                denom = (4 * x * y) - (n * y) - (n * x)
                if denom <= 0:
                    continue

                if (n * x * y) % denom == 0:
                    z = (n * x * y) // denom
                    return f"4/{n} = 1/{x} + 1/{y} + 1/{z}"

        return f"No solution found within limit ({LIMIT})."

    except Exception as e:
        return f"ERROR: {str(e)}"


# -------------------- EXPORT --------------------

def get_calculator_tools():
    return [
        basic_compute,
        modular_inverse,
        primality_test,
        erdos_straus_check
    ]
