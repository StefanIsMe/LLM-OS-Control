# main.py

# Import the required modules
from utils.agent import create_clevrr_agent
from utils.prompt import prompt
from utils.constants import GEMINI, BG_COLOR, TEXT_COLOR, FONT, FONT_BOLD, BG_GRAY

import time
import pyautogui as pg
pg.PAUSE = 2

import argparse
import logging

# Import tkinter at the module level
import tkinter as tk

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to initialize the application with optional arguments for UI settings and model.

    The application provides a graphical interface for interacting with an automated agent (Clevrr).
    The float UI setting controls whether the application window stays on top of other windows.
    """

    # Initialize the argument parser with improved documentation
    parser = argparse.ArgumentParser(
        description="Launch the Clevrr application with optional settings for the model and user interface."
    )

    # Add arguments for controlling the floating UI state
    parser.add_argument('--float-ui', type=int, default=1, choices=[0, 1],
                        help="Enable or disable the float UI window setting. Default is 1 (enabled). Pass 0 to disable.")

    parser.add_argument('--no-gui', action='store_true',
                        help="Run the application in console-only mode without GUI.")

    # Parse the arguments
    args = parser.parse_args()

    # Convert float-ui argument to a boolean
    float_ui = bool(args.float_ui)
    no_gui = args.no_gui

    # Print out the configurations for better debugging
    print("Using model: GEMINI")
    print(f"Float UI is {'enabled' if float_ui else 'disabled'}")
    print(f"GUI is {'disabled' if no_gui else 'enabled'}")

    # Create the Clevrr agent using the provided model and prompt
    try:
        global agent_executor  # Declare agent_executor as a global variable for use in other functions
        agent_executor = create_clevrr_agent(GEMINI, prompt)
    except Exception as ex:
        logging.error(f"Error initializing agent: {str(ex)}")
        return

    if no_gui:
        # Run in console-only mode
        while True:
            user_input = input("You -> ").strip()
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting...")
                break
            try:
                # Perform the action based on the user's input without reinitializing the agent
                response = agent_executor.invoke({"input": user_input})
                print(f"Bot -> {response.get('output')}")

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
                        print("Verification -> Action was successful.")
                        success = True
                        break
                    elif "failed" in verification_output:
                        print(f"Verification (Attempt {attempt + 1}) -> Action failed. Retrying...")
                    else:
                        print(f"Verification (Attempt {attempt + 1}) -> Could not determine the outcome.")

                if not success:
                    print("Verification -> Action could not be verified after multiple attempts.")

            except Exception as ex:
                # Improved error handling to provide better feedback to the user
                error_message = f"Error: {str(ex)}"
                logging.error(error_message)
                print(error_message)
    else:
        # Initialize the GUI
        root = tk.Tk()
        root.title("Clevrr Computer")

        # Set the window size to fill the whole screen vertically and 30% horizontally
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.3)
        window_height = screen_height - 150
        root.geometry(f"{window_width}x{window_height}")

        # Declare global variables before use
        global e
        global txt

        # Define the Entry widget and other GUI components
        e = tk.Entry(root, bg="#FCFCFC", fg=TEXT_COLOR, font=FONT, width=30)
        e.grid(row=2, column=0)

        txt = tk.Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=40, height=30)
        txt.grid(row=1, column=0, columnspan=2)

        def send():
            """
            Function to handle the user input, pass it to the agent, and display the response in the GUI.
            """
            user_input = e.get().lower()
            txt.insert(tk.END, f"\nYou -> {user_input}")
            time.sleep(1.5)

            try:
                # Perform the action based on the user's input without reinitializing the agent
                response = agent_executor.invoke({"input": user_input})
                txt.insert(tk.END, f"\nBot -> {response.get('output')}")

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
                        txt.insert(tk.END, "\nVerification -> Action was successful.")
                        success = True
                        break
                    elif "failed" in verification_output:
                        txt.insert(tk.END, f"\nVerification (Attempt {attempt + 1}) -> Action failed. Retrying...")
                    else:
                        txt.insert(tk.END, f"\nVerification (Attempt {attempt + 1}) -> Could not determine the outcome.")

                if not success:
                    txt.insert(tk.END, "\nVerification -> Action could not be verified after multiple attempts.")

            except Exception as ex:
                # Improved error handling to provide better feedback to the user
                error_message = f"\nError: {str(ex)}"
                logging.error(error_message)  # Log error to console for debugging purposes
                txt.insert(tk.END, error_message)

            # Clear the entry widget after processing
            e.delete(0, tk.END)

        # Set up the remaining GUI components
        tk.Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome to Clevrr Computer", font=FONT_BOLD, pady=10, width=30, height=2).grid(row=0)

        # Add a scrollbar for the text widget
        scrollbar = tk.Scrollbar(txt)
        scrollbar.place(relheight=1, relx=0.974)

        # Define the send button, linked to the send function
        tk.Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send).grid(row=2, column=1)

        # Set window attributes and start the main loop
        root.attributes('-topmost', float_ui)
        root.mainloop()

if __name__ == "__main__":
    main()
