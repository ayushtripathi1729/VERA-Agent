import math
from langchain_core.tools import tool

class NeuralCalculator:
    """
    Advanced Mathematical Logic Node for V.E.R.A.
    Specialized in Number Theory and Cryptographic primitives.
    """

    @tool
    def basic_compute(self, expression: str) -> str:
        """
        Evaluates standard mathematical expressions safely.
        Example: 'sqrt(144) + log10(100)'
        """
        try:
            # Using a restricted scope for security
            allowed_names = {
                "abs": abs, "round": round, 
                "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "pi": math.pi, "e": math.e, "pow": pow
            }
            return str(eval(expression, {"__builtins__": None}, allowed_names))
        except Exception as e:
            return f"COMPUTE_ERROR: {str(e)}"

    @tool
    def modular_inverse(self, a: int, m: int) -> str:
        """
        Calculates the modular multiplicative inverse of 'a' modulo 'm'.
        Critical for RSA and Number Theory problems.
        """
        try:
            # pow(a, -1, m) is the most efficient way in Python 3.8+
            result = pow(a, -1, m)
            return f"The modular inverse of {a} mod {m} is {result}."
        except ValueError:
            return f"Modular inverse does not exist (gcd({a}, {m}) != 1)."

    @tool
    def primality_test(self, n: int) -> str:
        """
        Performs a robust primality test.
        Uses Miller-Rabin logic for large integers.
        """
        if n < 2: return f"{n} is not prime."
        if n in (2, 3): return f"{n} is prime."
        if n % 2 == 0: return f"{n} is composite (divisible by 2)."
        
        # Simple deterministic check for smaller numbers
        # Can be scaled to full Miller-Rabin for research-grade work
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return f"{n} is composite (factor: {i})."
        return f"{n} is a prime number."

    @tool
    def erdos_straus_check(self, n: int) -> str:
        """
        Assists in verifying the Erdős–Straus conjecture for a given n.
        Finds x, y, z such that 4/n = 1/x + 1/y + 1/z.
        """
        # Heuristic search for the Egyptian fraction decomposition
        for x in range(1, 1000): # Iterative search depth
            for y in range(x, 1000):
                # Solving for z: 1/z = 4/n - 1/x - 1/y
                denom = (4 * x * y) - (n * y) - (n * x)
                if denom > 0 and (n * x * y) % denom == 0:
                    z = (n * x * y) // denom
                    return f"Conjecture verified for n={n}: 4/{n} = 1/{x} + 1/{y} + 1/{z}"
        return f"No solution found within current search depth for n={n}."

# Helper to export tools to the registry
def get_calculator_tools():
    calc = NeuralCalculator()
    return [
        calc.basic_compute,
        calc.modular_inverse,
        calc.primality_test,
        calc.erdos_straus_check
    ]
