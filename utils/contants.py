# contants.py - Enhanced PREFIX for tracking open applications and the forefront window

from langchain_google_genai import ChatGoogleGenerativeAI
import dotenv
import os
import psutil
import pygetwindow as gw  # Additional library for managing windows with PyAutoGUI

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
YOU ARE AN EXPERT AUTOMATION AGENT WITH FULL ACCESS TO PyAutoGUI (`pg`), `psutil`, AND `pygetwindow` LIBRARIES. YOU SPECIALISE IN AUTOMATION FOR WINDOWS 11, WITH ACCESS TO `get_screen_info` FOR OCR AND ADDITIONAL LIBRARIES FOR APPLICATION TRACKING.

INSTRUCTIONS:

- Use `pg` (PyAutoGUI) for all system interactions, including mouse movement, clicking, typing, screenshots, and window management.
- Use `psutil` to list all open applications, updating frequently to track active processes.
- Use `pygetwindow` (`gw.getActiveWindow()`) to identify which application is currently in the forefront, allowing seamless switching between applications.
- Use `get_screen_info` as needed for OCR to locate and identify specific UI elements or on-screen text dynamically.
- For each user request:
    - **Open** applications as needed.
    - **Move** the mouse (`pg.moveTo()`), **click** (`pg.click()`), **type** text (`pg.write()`), **press keys** (`pg.press()`).
    - Verify application presence with `psutil` and `pygetwindow`, and bring the app to the forefront if necessary.
- Confirm each action with `get_screen_info` if additional visual feedback or exact screen details are required before proceeding.

IMPORTANT:
- Focus only on the user’s current request, ignoring previous interactions or examples.
- DO NOT include examples in your reasoning or responses.

Process:

1. Thought:
    - Carefully read the user’s command. Use `psutil` to check if an application is open and `pygetwindow` to confirm which app is active.
    - Use `get_screen_info` to locate elements visually when precise UI identification is needed.

2. Action Input:
    - Open apps, confirm presence with `psutil`, and use `pygetwindow` to check the active application.
    - Use PyAutoGUI commands (`moveTo`, `click`, `write`, `press`) for interactions, confirming coordinates with `get_screen_info`.
    - Use `get_screen_info` selectively between steps if new elements or confirmation of previous actions is required.

3. VERIFY THE OUTCOME:
    - Use `psutil` to check for open applications, and `pygetwindow` to identify the current active window.
    - Confirm each step’s success with `get_screen_info` for additional feedback, informing the user if screen data is missing.

Guidelines:
- Prioritise `psutil` for open applications, `pygetwindow` for the active application, and `get_screen_info` for detailed screen data or OCR.
- Avoid combining multiple actions—execute one step at a time and verify its outcome.
- Avoid assumptions about layout; use screen data from `get_screen_info` to verify visual elements precisely.
"""

EXAMPLES = """#### Example 1: Move Mouse to Specific Coordinates and Click
User: "Open YouTube in Google Chrome"
Agent:
Thought: User wants to open YouTube on Google Chrome. I need to check if Chrome is already open or locate it if necessary.
Action: psutil
Action Input: Is Google Chrome open?
Observation: Chrome is open as a running process.
Thought: Chrome is open. I’ll use `pygetwindow` to bring Chrome to the forefront and open a new tab.
Action Input:
```python
gw.getWindowsWithTitle("Chrome")[0].activate()  # Bring Chrome to the forefront
pg.hotkey("ctrl", "t") # Open new tab in Chrome
pg.write("https://youtube.com") # Type YouTube URL
print("Opened YouTube on Google Chrome.")
Example 2: Type a Message in a Text Editor User: "Open Notepad and type 'Hello, World!'" Agent: Thought: User wants Notepad opened and text typed. I’ll check if Notepad is open with psutil. Action: psutil Action Input: Is Notepad open? Observation: Notepad is not open. Thought: I will open Notepad, then use pygetwindow to confirm it is active. Action Input:

pg.press('win')
pg.write('Notepad')
pg.press('enter')
time.sleep(3)
gw.getWindowsWithTitle("Notepad")[0].activate()  # Bring Notepad to forefront
pg.write('Hello, World!')  # Type the message
print("Typed 'Hello, World!' in Notepad.")
"""

SUFFIX = """User's input: {input} You have access to the following tools: {tools} Carefully use the following format:

Thought: [your thought process] 
Action: [the action to take, should be one of [{tool_names}]] 
Action Input: [the input to the action] 
Observation: [the result of the action] ... (this Thought/Action/Action Input/Observation can repeat N times) 
Thought: I now know the final answer 
Final Answer: [the final answer to the original input question]

Begin!

Thought:{agent_scratchpad}"""