import tkinter as tk
import pyautogui

# Create the main window
root = tk.Tk()
root.title("Cursor Position Display")

# Set window size and make it non-resizable
root.geometry("300x100")
root.resizable(False, False)

# Label to display the cursor position
label = tk.Label(root, text="Cursor Position: (0, 0)", font=("Helvetica", 14))
label.pack(pady=20)

# Function to update the cursor position
def update_position():
    # Get current mouse cursor position
    x, y = pyautogui.position()
    # Update the label with the cursor position
    label.config(text=f"Cursor Position: ({x}, {y})")
    # Call the update_position function every 100ms
    root.after(100, update_position)

# Start the position updates
update_position()

# Run the Tkinter event loop
root.mainloop()
