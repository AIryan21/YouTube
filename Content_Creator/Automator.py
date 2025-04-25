import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import json

class TaskAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Automation")
        self.root.geometry("400x600")
        self.root.attributes('-topmost', True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.tasks = []

        # Add Task Button
        self.add_task_button = ttk.Button(self.root, text="+ Add Task", command=self.add_task)
        self.add_task_button.pack(pady=10)

        # Task List Frame
        self.task_frame = tk.Frame(self.root)
        self.task_frame.pack(fill=tk.BOTH, expand=True)

        # Save Button
        self.save_button = ttk.Button(self.root, text="Save Tasks", command=self.save_tasks)
        self.save_button.pack(pady=10)

    def add_task(self):
        task_frame = tk.Frame(self.task_frame, bd=2, relief=tk.SUNKEN, padx=5, pady=5)
        task_frame.pack(fill=tk.X, pady=5)

        # Sleep Time Entry
        tk.Label(task_frame, text="Sleep Time (s):").pack(side=tk.LEFT, padx=5)
        sleep_time_entry = tk.Entry(task_frame, width=5)
        sleep_time_entry.pack(side=tk.LEFT, padx=5)

        # Action Dropdown
        tk.Label(task_frame, text="Action:").pack(side=tk.LEFT, padx=5)
        action_var = tk.StringVar()
        action_dropdown = ttk.Combobox(task_frame, textvariable=action_var, values=["Mouse Click"], state="readonly")
        action_dropdown.pack(side=tk.LEFT, padx=5)

        # Action Details Entry
        tk.Label(task_frame, text="Details:").pack(side=tk.LEFT, padx=5)
        action_details_entry = tk.Entry(task_frame, width=20)
        action_details_entry.pack(side=tk.LEFT, padx=5)

        # Bind Mouse Click Detection
        action_dropdown.bind("<<ComboboxSelected>>", lambda e: self.start_mouse_position_detection(action_details_entry) if action_var.get() == "Mouse Click" else None)

        # Remove Task Button
        remove_button = ttk.Button(task_frame, text="Remove", command=lambda: self.remove_task(task_frame))
        remove_button.pack(side=tk.LEFT, padx=5)

        self.tasks.append({
            "frame": task_frame,
            "sleep_time": sleep_time_entry,
            "action": action_var,
            "details": action_details_entry
        })

    def start_mouse_position_detection(self, details_entry):
        messagebox.showinfo("Info", "Click anywhere on the screen to save the cursor position.")
        while True:
            x, y = pyautogui.position()
            if pyautogui.mouseDown(button='left'):
                details_entry.delete(0, tk.END)
                details_entry.insert(0, f"{x},{y}")
                break

    def remove_task(self, task_frame):
        for task in self.tasks:
            if task["frame"] == task_frame:
                self.tasks.remove(task)
                break
        task_frame.destroy()

    def save_tasks(self):
        task_data = []
        for task in self.tasks:
            try:
                sleep_time = float(task["sleep_time"].get())
                action = task["action"].get()
                details = task["details"].get()
                if not action or not details:
                    raise ValueError("Incomplete task details.")
                task_data.append({
                    "sleep_time": sleep_time,
                    "action": action,
                    "details": details
                })
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid task data: {e}")
                return

        with open("tasks.json", "w") as f:
            json.dump(task_data, f, indent=4)

        messagebox.showinfo("Success", "Tasks saved successfully!")

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskAutomationApp(root)
    root.mainloop()
