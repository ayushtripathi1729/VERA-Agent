import os
from typing import List, Dict
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool


class SensoryEngine:
    """
    Sensing & Intel Gathering Module for V.E.R.A.
    Optimized for clean, structured outputs for LLM reasoning.
    """

    def __init__(self):
        self.search = TavilySearchResults(
            k=5,
            search_depth="advanced",
            include_raw_content=False,
            include_images=False
        )

    @tool
    def perform_web_search(self, query: str) -> str:
        """
        Executes a web search and returns structured, concise results.
        """

        try:
            # 🔐 API Key Check
            if not os.getenv("TAVILY_API_KEY"):
                return "SEARCH_ERROR: Missing Tavily API key."

            # 🌐 Execute Search
            results = self.search.invoke({"query": query})

            if not results:
                return "No relevant real-time results found."

            # 🧠 Format results for LLM consumption
            formatted_results = []

            for i, res in enumerate(results):
                url = res.get("url", "N/A")
                content = res.get("content", "")

                # ✂️ Trim long content (important for token control)
                content = content.strip()
                if len(content) > 300:
                    content = content[:300] + "..."

                formatted_results.append(
                    f"[Result {i+1}]\n"
                    f"Source: {url}\n"
                    f"Summary: {content}\n"
                )

            # 📦 Final structured output
            return "\n".join(formatted_results)

        except Exception as e:
            print(f"[!] SEARCH_ENGINE_ERROR: {str(e)}")
            return f"SENSOR_FAILURE: {str(e)}"


# Singleton instance
vera_search_engine = SensoryEngine()
