import os
from typing import List, Dict, Any
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

class NeuralSearch:
    """
    Real-time Information Retrieval Engine for V.E.R.A.
    Optimized for technical, academic, and security-related queries.
    """

    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        # TavilySearchResults is built for LLM compatibility
        self.search_engine = TavilySearchResults(
            k=5, # Top 5 results for deep context
            search_depth="advanced", # "advanced" includes more technical/academic sources
            include_raw_content=False,
            include_images=False
        )

    @tool
    def perform_web_search(self, query: str) -> str:
        """
        Performs an advanced web search to retrieve real-time data.
        Use this for current events, technical documentation, or unsolved math problems.
        """
        try:
            results = self.search_engine.invoke({"query": query})
            
            # Format results into a clean, readable string for the LLM
            formatted_results = []
            for res in results:
                formatted_results.append(f"SOURCE: {res['url']}\nCONTENT: {res['content']}\n")
            
            return "\n---\n".join(formatted_results)
            
        except Exception as e:
            return f"SEARCH_FAILURE: Unable to reach web sensory node. Error: {str(e)}"

# Singleton instance
vera_search_engine = NeuralSearch()

def get_search_tools():
    """Returns the search utility for the V.E.R.A. toolset."""
    return [vera_search_engine.perform_web_search]
