"""
V.E.R.A. Tool Distribution Hub
Organizes and exposes sensory and logical capabilities.
NODE: JKIAPT_PRAYAGRAJ
"""

from typing import List
from langchain_core.tools import BaseTool

# FIXED IMPORTS: 
# Since these files are in the same 'tools' folder, 
# we import directly from the local modules.
from tools.search import vera_search_engine
from tools.calculator import get_calculator_tools
from tools.reporter import vera_reporter

def get_default_tools() -> List[BaseTool]:
    """
    Assembles the primary toolset for the V.E.R.A. Neural Core.
    Combines web search, mathematical logic, and synthesis tools.
    """
    
    # 1. Sensory Tools (Web Search via Tavily)
    search_tools = [vera_search_engine.perform_web_search]
    
    # 2. Logic Tools (Number Theory, Modular Arithmetic, Primality)
    math_tools = get_calculator_tools()
    
    # Combined registry for the Agent Executor
    combined_tools = search_tools + math_tools
    
    return combined_tools

# Metadata for system diagnostics
TOTAL_ACTIVE_TOOLS = len(get_default_tools())
__all__ = ["get_default_tools", "vera_reporter"]
