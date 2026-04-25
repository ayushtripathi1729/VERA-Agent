"""
V.E.R.A. Tool Distribution Hub
Organizes and exposes sensory and logical capabilities.
"""

from typing import List
from langchain_core.tools import BaseTool

# Internal imports from sub-modules
from agent.tools.search import vera_search_engine
from agent.tools.calculator import get_calculator_tools
from agent.tools.reporter import vera_reporter

def get_default_tools() -> List[BaseTool]:
    """
    Assembles the primary toolset for the V.E.R.A. Neural Core.
    Combines web search, mathematical logic, and synthesis tools.
    """
    
    # 1. Sensory Tools (Web Search)
    search_tools = [vera_search_engine.perform_web_search]
    
    # 2. Logic Tools (Number Theory & Math)
    math_tools = get_calculator_tools()
    
    # 3. System Tools (Internal Synthesis)
    # We don't always pass the reporter as a tool to the agent,
    # but we expose it here for the Executor to use post-process.
    
    combined_tools = search_tools + math_tools
    
    return combined_tools

# Metadata for system diagnostics
TOTAL_ACTIVE_TOOLS = len(get_default_tools())
__all__ = ["get_default_tools", "vera_reporter"]
