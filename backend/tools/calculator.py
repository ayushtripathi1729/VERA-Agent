import math
import re
from langchain_core.tools import tool


class NeuralCalculator:
    """
    Advanced Mathematical Logic Node for V.E.R.A.
    Specialized in Number Theory and safe computation.
    """

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

    # 🔍 Safe expression validation (only math chars)
    SAFE_PATTERN = re.compile(r"^[0-9\.\+\-\*\/\^\(\)\s,a-zA-Z]+$")

    @tool
    def basic_compute(self, expression: str) -> str:
        """
        Safely evaluates mathematical expressions.
        Example: 'sqrt(144) + log10(100)'
        """
        try:
            if not expression or not self.SAFE_PATTERN.match(expression):
                return "COMPUTE_ERROR: Invalid or unsafe expression."

            # Replace ^ with ** for exponentiation
            expression = expression.replace("^", "**")

            result = eval(expression, {"__builtins__": None}, self.SAFE_FUNCTIONS)
            return f"Result: {result}"

        except Exception as e:
            return f"COMPUTE_ERROR: {str(e)}"

    @tool
    def modular_inverse(self, a: int, m: int) -> str:
        """
        Computes modular inverse using Python's optimized pow().
        """
        try:
            if m == 0:
                return "ERROR: Modulus cannot be zero."

            result = pow(a, -1, m)
            return f"mod_inverse({a}, {m}) = {result}"

        except ValueError:
            return f"No modular inverse exists (gcd({a}, {m}) ≠ 1)."
        except Exception as e:
            return f"ERROR: {str(e)}"

    @tool
    def primality_test(self, n: int) -> str:
        """
        Efficient primality test (optimized trial division).
        """
        try:
            if n < 2:
                return f"{n} is not prime."

            if n in (2, 3):
                return f"{n} is prime."

            if n % 2 == 0:
                return f"{n} is composite (divisible by 2)."

            # Optimized loop (6k ± 1)
            i = 5
            while i * i <= n:
                if n % i == 0 or n % (i + 2) == 0:
                    return f"{n} is composite (factor found)."
                i += 6

            return f"{n} is prime."

        except Exception as e:
            return f"ERROR: {str(e)}"

    @tool
    def erdos_straus_check(self, n: int) -> str:
        """
        Attempts to verify Erdős–Straus conjecture: 4/n = 1/x + 1/y + 1/z
        Uses optimized bounded search.
        """
        try:
            if n < 2:
                return "Invalid input: n must be ≥ 2."

            LIMIT = 500  # reduced for performance

            for x in range(1, LIMIT):
                for y in range(x, LIMIT):
                    denom = (4 * x * y) - (n * y) - (n * x)
                    if denom <= 0:
                        continue

                    if (n * x * y) % denom == 0:
                        z = (n * x * y) // denom
                        return f"4/{n} = 1/{x} + 1/{y} + 1/{z}"

            return f"No solution found within search limit ({LIMIT})."

        except Exception as e:
            return f"ERROR: {str(e)}"


# --- TOOL EXPORT ---

def get_calculator_tools():
    calc = NeuralCalculator()
    return [
        calc.basic_compute,
        calc.modular_inverse,
        calc.primality_test,
        calc.erdos_straus_check
    ]
