import os
from typing import List, Dict
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

class SensoryEngine:
    """
    Sensing & Intel Gathering Module for V.E.R.A.
    Powered by Tavily for AI-optimized web crawling.
    """

    def __init__(self):
        # Initializing the Tavily tool
        # k=5 ensures enough context without blowing the token budget
        self.search = TavilySearchResults(
            k=5,
            search_depth="advanced", # Deep crawl for technical accuracy
            include_raw_content=False,
            include_images=False
        )

    @tool
    def perform_web_search(self, query: str) -> str:
        """
        Executes a deep web search to gather real-time data.
        Ideal for: Latest CVEs, academic conjectures, or stock trends.
        """
        try:
            # Check for API Key presence
            if not os.getenv("TAVILY_API_KEY"):
                return "SEARCH_ERROR: API_KEY_MISSING in JKIAPT Node."

            # Execute search
            results = self.search.invoke({"query": query})
            
            if not results:
                return "No real-time data found for this specific query."

            # Synthesis of results into a readable format for the Agent
            summary = []
            for i, res in enumerate(results):
                summary.append(f"[{i+1}] SOURCE: {res['url']}\nCONTENT: {res['content']}\n")

            return "\n".join(summary)

        except Exception as e:
            return f"SENSOR_FAILURE: {str(e)}"

# Singleton instance
vera_search_engine = SensoryEngine()
