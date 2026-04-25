"""
V.E.R.A. Neural Agent Module
Author: The Hacksmiths (JKIAPT)
Version: 1.0.0
"""

import os
from typing import List
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilyAnswer
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- AGENT INITIALIZATION ---

def initialize_vera_agent():
    """
    Constructs the V.E.R.A. Agent with Groq LPU and Tavily Search.
    Ensures stable connection to the Llama-3-70b-versatile model.
    """
    
    # 1. Setup the Model (Groq LPU)
    # Using 70b for high-quality reasoning in number theory and cybersec
    llm = ChatGroq(
        temperature=0.3,
        model_name="llama3-70b-8192",
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    # 2. Setup the Tools (Real-time Intel)
    # TavilyAnswer provides clean, concise search results
    search_tool = TavilyAnswer(max_results=3)
    tools = [search_tool]

    # 3. Construct the System Prompt
    # This gives V.E.R.A. her specific personality and reasoning constraints
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are V.E.R.A. (Virtual Electronic Risk Assistant).
        Operate as a high-level cognitive architecture for Ayush Tripathi.
        
        CORE PROTOCOLS:
        1. Specialized in Number Theory, Cybersec, and Theoretical CS.
        2. Responses must be technical, precise, and professional.
        3. Use the search tool only when real-time data is required.
        4. Maintain a 'Cyber-Oasis' aesthetic in your reasoning.
        """),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # 4. Bind Agent & Executor
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )

# Export the initializer for main.py to use
__all__ = ["initialize_vera_agent"]
