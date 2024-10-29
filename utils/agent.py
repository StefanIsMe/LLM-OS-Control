# agent.py

# Import necessary modules
from langchain.agents import AgentExecutor, create_react_agent
from langchain_experimental.tools.python.tool import PythonAstREPLTool  # Updated import

from utils.constants import GEMINI
from utils.tools import get_screen_info

import pyautogui as pg  # type: ignore
import time  # Import time module
import logging

pg.PAUSE = 2

def create_clevrr_agent(model, prompt):
    try:
        print("============================================\nInitialising Clevrr Agent\n============================================")
        
        # Initialize the PythonAstREPLTool
        repl_tool = PythonAstREPLTool()
        
        # Set the globals for the tool
        repl_tool.globals["pg"] = pg
        repl_tool.globals["time"] = time  # Include time module if needed

        tools = [repl_tool, get_screen_info]

        agent = create_react_agent(model, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )
        return agent_executor
    except Exception as ex:
        logging.error(f"Error creating agent: {str(ex)}")
        raise
