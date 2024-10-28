# main.py

# Import the required modules
from utils.agent import create_clevrr_agent
from utils.prompt import prompt
from utils.contants import GEMINI, BG_COLOR, TEXT_COLOR, FONT, FONT_BOLD, BG_GRAY

import time
import pyautogui as pg
pg.PAUSE = 2

import argparse
from tkinter import *

def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Launch the application with optional model and UI settings.")
    
    # Add arguments
    parser.add_argument('--float-ui', type=int, default=1, choices=[0, 1],
                        help="Enable or disable the float UI. Default is 1 (enabled). Pass 0 to disable.")
    
    # Parse the arguments
    args = parser.parse_args()

    # Convert float-ui argument to boolean
    float_ui = bool(args.float_ui)

    # Print out the configurations
    print("Using model: gemini")
    print(f"Float UI is {'enabled' if float_ui else 'disabled'}")

    # Use the GEMINI model directly
    global agent_executor  # Declare agent_executor as global
    agent_executor = create_clevrr_agent(GEMINI, prompt)

    # Initialize the GUI
    root = Tk()
    root.title("Clevrr Computer")
    
    # Set the window size to fill the whole screen vertically and 30% horizontally
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.3)
    window_height = screen_height - 150
    root.geometry(f"{window_width}x{window_height}")

    # Define the Entry widget and other GUI components
    global e, txt
    e = Entry(root, bg="#FCFCFC", fg=TEXT_COLOR, font=FONT, width=30)
    e.grid(row=2, column=0)
    
    txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=40, height=30)
    txt.grid(row=1, column=0, columnspan=2)

    def send():
        global e, txt, agent_executor  # Add agent_executor to the global scope
        user_input = e.get().lower()
        txt.insert(END, f"\nYou -> {user_input}")
        time.sleep(1.5)
        
        try:
            # Perform the action based on the user's input without reinitializing the agent
            response = agent_executor.invoke({"input": user_input})
            txt.insert(END, f"\nBot -> {response.get('output')}")

            # Attempt verification of the last action with a limited number of retries
            verification_attempts = 3
            success = False
            for attempt in range(verification_attempts):
                time.sleep(2)  # Allow time for the action to take effect
                # Pass the user's input as context for verification
                verification_response = agent_executor.invoke({"input": f"Verify if the action '{user_input}' was successful."})
                verification_output = verification_response.get('output', '').lower()

                # Adjust behavior based on the verification response
                if "success" in verification_output:
                    txt.insert(END, "\nVerification -> Action was successful.")
                    success = True
                    break
                elif "failed" in verification_output:
                    txt.insert(END, f"\nVerification (Attempt {attempt + 1}) -> Action failed. Retrying...")
                else:
                    txt.insert(END, f"\nVerification (Attempt {attempt + 1}) -> Could not determine the outcome.")
            
            if not success:
                txt.insert(END, "\nVerification -> Action could not be verified after multiple attempts.")
        
        except Exception as e:
            txt.insert(END, f"\nError: {str(e)}")
        
        e.delete(0, END)

    # Set up the remaining GUI components
    Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome to Clevrr Computer", font=FONT_BOLD, pady=10, width=30, height=2).grid(row=0)
    
    # Add a scrollbar for the text widget
    scrollbar = Scrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)
    
    # Define the send button, linked to the send function
    Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send).grid(row=2, column=1)

    # Set window attributes and start the main loop
    root.attributes('-topmost', float_ui)
    root.mainloop()

if __name__ == "__main__":
    main()
