# main.py - Updated to include only GUI-related code using PyAutoGUI and Gemini API for OCR functionality

# Import the required modules
from utils.agent import create_clevrr_agent
from utils.prompt import prompt
from utils.constants import GEMINI, BG_COLOR, TEXT_COLOR, FONT, FONT_BOLD, BG_GRAY

import time
import pyautogui as pg
pg.PAUSE = 2

import tkinter as tk
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to initialize the application with GUI settings.
    The application provides a graphical interface for interacting with an automated agent (Clevrr).
    """

    # Print out the configurations for better debugging
    print("Using model: GEMINI")
    print("Float UI is enabled")
    print("GUI is enabled")

    # Create the Clevrr agent using the provided model and prompt
    try:
        global agent_executor  # Declare agent_executor as a global variable for use in other functions
        agent_executor = create_clevrr_agent(GEMINI, prompt)
    except Exception as ex:
        logging.error(f"Error initializing agent: {str(ex)}")
        return

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
            # Perform the action based on the user's input
            response = agent_executor.invoke({"input": user_input})
            txt.insert(tk.END, f"\nBot -> {response.get('output')}")

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
    root.attributes('-topmost', True)
    root.mainloop()

if __name__ == "__main__":
    main()
