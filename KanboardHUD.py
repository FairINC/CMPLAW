import requests
import tkinter as tk
from tkinter import ttk

class ProjectHUD:
    def __init__(self, root):
        self.root = root
        self.root.title("Project HUD")

        self.username = "CHANGEME"
        self.password = None  # Prompt for password later
        self.base_url = "CHANGEME/jsonrpc.php"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        self.create_widgets()

    def create_widgets(self):
        # Dropdown for users
        self.user_label = ttk.Label(self.root, text="Select User:")
        self.user_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.user_var = tk.StringVar()
        self.user_dropdown = ttk.Combobox(self.root, textvariable=self.user_var)
        self.user_dropdown.grid(row=0, column=1, padx=10, pady=5)
        self.user_dropdown.bind("<<ComboboxSelected>>", self.get_projects)

        # Dropdown for projects
        self.project_label = ttk.Label(self.root, text="Select Project:")
        self.project_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.project_var = tk.StringVar()
        self.project_dropdown = ttk.Combobox(self.root, textvariable=self.project_var)
        self.project_dropdown.grid(row=1, column=1, padx=10, pady=5)
        self.project_dropdown.bind("<<ComboboxSelected>>", self.get_board)

        # Back button
        self.back_button = ttk.Button(self.root, text="Back", command=self.clear_selection)
        self.back_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    def clear_selection(self):
        self.user_dropdown.set("")
        self.project_dropdown.set("")

    def get_projects(self, event):
        user = self.user_var.get()
        # Make API call to get all projects for the selected user
        # Use HTTP Basic Authentication with username and password
        # Update project dropdown with the retrieved projects

    def get_board(self, event):
        project_name = self.project_var.get()
        # Make API call to get board information for the selected project
        # Update GUI to display board information

def main():
    root = tk.Tk()
    app = ProjectHUD(root)
    root.mainloop()

if __name__ == "__main__":
    main()
