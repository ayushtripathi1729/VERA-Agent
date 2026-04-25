"""
V.E.R.A. Tool Registry
Centralized hub for all external capabilities (Search, Math, Security).
"""

from langchain_core.tools import tool
from agent.tools.search import get_search_tools
from agent.tools.calculator import get_calculator_tools

# --- CUSTOM SYSTEM TOOLS ---

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

# --- CONSOLIDATED TOOL COLLECTION ---

def get_default_tools():
    """
    Assembles the complete neural toolset for the V.E.R.A. agent.
    Combines sensory (search), logic (calculator), and system diagnostics.
    """
    # 1. Fetch search capabilities (from search.py)
    search_tools = get_search_tools()
    
    # 2. Fetch mathematical capabilities (from calculator.py)
    calc_tools = get_calculator_tools()
    
    # 3. Combine everything into a single operational list
    return [
        *search_tools,
        *calc_tools,
        system_diagnostic
    ]

# Exporting for stable imports in executor.py
__all__ = ["get_default_tools", "system_diagnostic"]
