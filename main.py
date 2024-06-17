import tkinter as tk
from gui import GUI
from logic import Logic

def main():
    # Initialize the main window for the application
    root = tk.Tk()
    # Create an instance of the logic class
    logic = Logic()  
    # Create an instance of the GUI, passing both root and logic to the GUI
    app = GUI(root, logic)
    # Start the application's main event loop, waiting for user interaction
    app.run()

# Ensure that this script runs only when it is executed directly, not when imported
if __name__ == "__main__":
    main()