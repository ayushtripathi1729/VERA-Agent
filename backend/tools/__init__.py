"""
V.E.R.A. Tool Registry
Centralized hub for all external capabilities (Search, Math, Security).
"""

from langchain_community.tools.tavily_search import TavilyAnswer
from langchain_core.tools import tool
from agent.tools.search import get_search_tools


# --- CUSTOM TOOL DEFINITIONS ---

@tool
def calculate_mod_inverse(a: int, m: int) -> str:
    """
    Calculates the modular multiplicative inverse of a modulo m.
    Essential for Number Theory and RSA cryptography problems.
    """
    try:
        # Using the extended Euclidean Algorithm logic via pow()
        result = pow(a, -1, m)
        return f"The modular inverse of {a} mod {m} is {result}."
    except ValueError:
        return f"The modular inverse does not exist for {a} mod {m}."

@tool
def system_diagnostic() -> str:
    """
    Returns the current operational status of the V.E.R.A. Neural Core.
    Usage: When the user asks about system health or node location.
    """
    return (
        "NODE_STATUS: OPTIMAL\n"
        "LOCATION: PRAYAGRAJ_JKIAPT_NODE_01\n"
        "LATENCY: < 50ms (LPU Optimized)\n"
        "SECURITY_LEVEL: 05 (PROMPT_GUARD_ACTIVE)"
    )

# --- TOOL COLLECTION ---

def get_default_tools():
    """
    Returns the primary toolset for the V.E.R.A. agent.
    Combines real-time web search with specialized local utilities.
    """
    # 1. Real-time Intel Tool
    search = TavilyAnswer(max_results=3)
    
    # 2. Add your custom tools here
    return [
        search,
        calculate_mod_inverse,
        system_diagnostic
    ]

def get_default_tools():
    search_tools = get_search_tools()
    calc_tools = get_calculator_tools()
    
    return [
        *search_tools,
        *calc_tools,
        system_diagnostic
    ]

# Exporting for stable imports in executor.py
__all__ = ["get_default_tools", "calculate_mod_inverse", "system_diagnostic"]
