"""
V.E.R.A. Tool Distribution Hub
Organizes and exposes sensory and logical capabilities.
NODE: JKIAPT_PRAYAGRAJ
"""

from typing import List
from langchain_core.tools import BaseTool

# --- TOOL IMPORTS ---
from tools.search import vera_search_engine
from tools.calculator import get_calculator_tools
from tools.reporter import vera_reporter


def get_default_tools() -> List[BaseTool]:
    """
    Builds and validates the tool registry for the agent.
    Ensures only valid tools are returned.
    """

    tools: List[BaseTool] = []

    try:
        # 🌐 Search Tool
        search_tool = vera_search_engine.perform_web_search
        if search_tool:
            tools.append(search_tool)
    except Exception as e:
        print(f"[!] TOOL_LOAD_ERROR (Search): {str(e)}")

    try:
        # 🔢 Calculator Tools
        math_tools = get_calculator_tools()
        if math_tools:
            tools.extend(math_tools)
    except Exception as e:
        print(f"[!] TOOL_LOAD_ERROR (Calculator): {str(e)}")

    # 🔍 Final validation (filter None or invalid tools)
    valid_tools = [t for t in tools if t is not None]

    return valid_tools


# --- METADATA ---
def get_tool_names() -> List[str]:
    """
    Returns names of active tools (useful for debugging/demo).
    """
    try:
        return [tool.name for tool in get_default_tools()]
    except Exception:
        return []


TOTAL_ACTIVE_TOOLS = len(get_default_tools())

__all__ = ["get_default_tools", "vera_reporter", "get_tool_names"]
