import math
from langchain_core.tools import tool

class NeuralCalculator:
    """
    Specialized Mathematical Engine for V.E.R.A.
    Handles Number Theory, Primality Testing, and Cryptographic math.
    """

    @tool
    def prime_check(n: int) -> str:
        """
        Determines if a number is prime. 
        Crucial for Number Theory and Cryptography tasks.
        """
        if n < 2: return f"{n} is not prime."
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return f"{n} is not prime (divisible by {i})."
        return f"{n} is a PRIME number."

    @tool
    def modular_exponentiation(base: int, exp: int, mod: int) -> str:
        """
        Calculates (base^exp) % mod efficiently. 
        Used in RSA encryption/decryption logic.
        """
        try:
            res = pow(base, exp, mod)
            return f"Result of ({base}^{exp}) mod {mod} is {res}."
        except Exception as e:
            return f"Error in modular calculation: {str(e)}"

    @tool
    def extended_gcd(a: int, b: int) -> str:
        """
        Calculates the Extended Euclidean Algorithm.
        Returns gcd, x, and y such that ax + by = gcd(a, b).
        """
        def egcd(a, b):
            if a == 0:
                return b, 0, 1
            else:
                gcd, y, x = egcd(b % a, a)
                return gcd, x - (b // a) * y, y
        
        g, x, y = egcd(a, b)
        return f"GCD: {g}, coefficients x: {x}, y: {y} (for {a}x + {b}y = {g})"

# Instance for internal logic if needed
calc_engine = NeuralCalculator()

def get_calculator_tools():
    """Returns a list of all mathematical tools for the agent."""
    return [
        NeuralCalculator.prime_check,
        NeuralCalculator.modular_exponentiation,
        NeuralCalculator.extended_gcd
    ]
