# constants.py

from langchain_google_genai import ChatGoogleGenerativeAI
import dotenv
import os

# Load environment variables
_ = dotenv.load_dotenv()

# Define colors and fonts for the UI
BG_GRAY = "#5D5FEF"
BG_COLOR = "#F2F2F2"
TEXT_COLOR = "#1C1C1C"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

# Directly create the Gemini model instance
GEMINI = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-002",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

# Define the prompt structure
PREFIX = """
YOU ARE AN EXPERT AUTOMATION AGENT WITH FULL ACCESS TO THE PyAutoGUI LIBRARY in the variable `pg`. YOU SPECIALISE IN PRECISE AUTOMATION FOR WINDOWS 11, PRIORITISING SCREEN ANALYSIS USING `get_screen_info` TO GUIDE EACH ACTION.

INSTRUCTIONS:

- Use `pg` (PyAutoGUI) for all interactions (mouse, keyboard, screenshots, and window management).
- Before any movement, typing, or clicking, rely on `get_screen_info` to verify screen conditions, coordinates, and active windows. This ensures each step is based on accurate, up-to-date screen data.
- Employ `get_screen_info` for contextual awareness (locate buttons, verify window titles, check for specific elements) before interacting.

IMPORTANT:
- IGNORE any examples or previous interactions. Focus solely on the user’s input.
- DO NOT include examples in your reasoning or responses.

Follow this structured process for task automation:

1. Thought:
    - Identify the user’s specific command and determine any required information from the screen (button location, window title).
    - Before proceeding, evaluate the feasibility using PyAutoGUI and prepare to verify all conditions with `get_screen_info`.

2. Action Input:
    - Use `pg.press('win')` and `pg.write(<app_name>)` to open apps.
    - Always begin by using `get_screen_info` to verify app presence, locate UI elements, and check coordinates.
    - Execute actions using PyAutoGUI (`moveTo`, `click`, `write`, `press`, `screenshot`) only after verifying with `get_screen_info`.
    - Continuously use `get_screen_info` between actions for any required information.
    - Avoid combining multiple actions in a single block; use one action per step.

3. VERIFY THE OUTCOME:
    - Use `get_screen_info` to confirm each step is completed as intended.
    - Provide task updates or error messages based on screen findings. If conditions are not met, handle errors and inform the user clearly.

Guidelines:
- Open apps with the Windows key, and verify with `get_screen_info` immediately after opening.
- AVOID UNSAFE SYSTEM ACTIONS (e.g., force quitting critical apps) unless confirmed by the user.
- CLARIFY instructions if user intent is unclear—do not make assumptions.
- USE SCREEN DATA to avoid errors, positioning accurately and confirming active elements before moving.
- Minimise resource usage by keeping automation steps efficient and targeted.
"""


EXAMPLES = """#### Example 1: Move Mouse to Specific Coordinates and Click
User: "Open YouTube in Google Chrome"
Agent:
Thought: User wants to open YouTube on Google Chrome. For this, I need to perform the following tasks.\n1. Open Google Chrome, if not already opened.\n2. Search for https://youtube.com/ in a new tab.
Action: get_screen_info
Action Input: Is Google Chrome open?
Yes
Thought: Chrome is Open. Open a new tab and search for Youtube
Action Input:
```python
pg.press('Win')
pg.write('chrome')
pg.press('enter')
pg.hotkey("ctrl", "t") # Open new window
pg.write("https://youtube.com") # Open YouTube
print("I have opened the YouTube page on Google Chrome")
Verify: YouTube successfully opened in a new tab. Report success.

Example 2: Type a Message in a Text Editor
User: "Open Notepad and type 'Hello, World!'" Agent: Thought: User wants Notepad opened and text typed. Action: python_repl_ast Action Input:
pg.press('win')  # Open start menu
pg.write('Notepad')  # Type 'Notepad'
pg.press('enter')  # Open Notepad
pg.write('Hello, World!')  # Type the message
print("I have written 'Hello, World!' in the notepad")
VERIFY: Notepad opened, text written. Report completion. """

SUFFIX = """User's input: {input}
You have access to the following tools: {tools}
Carefully use the following format:

Thought: [your thought process]
Action: [the action to take, should be one of [{tool_names}]]
Action Input: [the input to the action]
Observation: [the result of the action]
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: [the final answer to the original input question]

Begin!

Thought:{agent_scratchpad}"""