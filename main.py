import os
import sys
from pydantic import BaseModel, ValidationError

import tkinter as tk
from tkinter import messagebox

if getattr(sys, 'frozen', False):
    # If the app is running as a frozen app (i.e., .app bundle)
    base_dir = os.path.dirname(sys.executable)
    os.chdir(base_dir)  # Change working directory to the folder where the executable resides
else:
    # If running in normal Python environment
    base_dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(base_dir)

class Project(BaseModel):
    Nummer: int
    Plaats: str
    Naam: str
    Opdrachtgever: str

# Function to create directories based on the folder structure
def create_folders(lines, project):
    base_path = str(base_dir) + f"/{project.Nummer}_{project.Plaats}_{project.Naam}_{project.Opdrachtgever}"

    current_indent_level = 0
    path_stack = [base_path]
      
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:  # Ignore empty lines
            indent_level = len(line) - len(stripped_line)
            folder_name = stripped_line.strip()

            # Adjust the path stack based on indentation (nesting level)
            if indent_level > current_indent_level:
                path_stack.append(os.path.join(path_stack[-1], folder_name))
            elif indent_level < current_indent_level:
                path_stack = path_stack[:indent_level//4 + 1]  # Adjust the path stack
                path_stack.append(os.path.join(path_stack[-1], folder_name))
            else:
                path_stack[-1] = os.path.join(os.path.dirname(path_stack[-1]), folder_name)

            current_indent_level = indent_level

            # Create the directory
            os.makedirs(path_stack[-1], exist_ok=True)
            #print(f"Created directory: {path_stack[-1]}")

# Define the path to the text file with the folder structure
folder_structure_file = 'folder_structure.txt'

# Read the folder structure from the file
with open(folder_structure_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()


     
# Function to handle form submission
def submit_form():
    try:
        nummer = nummer_entry.get()
        plaats = plaats_entry.get()
        naam = naam_entry.get()
        opdrachtgever = opdrachtgever_entry.get()
        global base_dir
        base_dir = entry_box.get()
        project = Project(Nummer=int(nummer), Plaats=plaats, Naam=naam, Opdrachtgever=opdrachtgever)

        create_folders(lines, project)
       
        # Update the entry box with the base path after it's created
        entry_box.config(state='normal')  # Enable the entry box temporarily
        
        entry_box.config(state='disabled')  # Disable it again
        
        messagebox.showinfo("Success", "Project data submitted successfully!")
    except ValidationError as e:
        messagebox.showerror("Error", f"Validation Error: {e}")
    except ValueError:
        messagebox.showerror("Error", "Number can only contain numeric values. Please enter valid data.")

def toggle_editability():
    if entry_box.cget('state') == 'disabled':  # If entry is disabled
        entry_box.config(state='normal')  # Enable editing
        toggle_button.config(text='Save')  # Change button text to 'Save'
    else:
        entry_box.config(state='disabled')  # Disable editing
        toggle_button.config(text='Edit')  # Change button text back to 'Edit'


# Create the main Tkinter window
root = tk.Tk()
root.title("Project Data Entry Form")
root.config(padx=20, pady=20)

# Create labels and entry fields for each attribute
tk.Label(root, text="Nummer:").grid(row=0, column=0)
nummer_entry = tk.Entry(root, width=30)
nummer_entry.grid(row=0, column=1)

tk.Label(root, text="Plaats:").grid(row=1, column=0)
plaats_entry = tk.Entry(root, width=30)
plaats_entry.grid(row=1, column=1)

tk.Label(root, text="Naam:").grid(row=2, column=0)
naam_entry = tk.Entry(root, width=30)
naam_entry.grid(row=2, column=1)

tk.Label(root, text="Opdrachtgever:").grid(row=3, column=0)
opdrachtgever_entry = tk.Entry(root, width=30)
opdrachtgever_entry.grid(row=3, column=1)

# Create an Entry widget (initially disabled)
tk.Label(root, text="Folder Path:").grid(row=4, column=0)
entry_box = tk.Entry(root, width=30)
entry_box.insert(0, base_dir)
entry_box.config(state='disabled')
entry_box.grid(row=4, column=1)

# Create the button with a pencil icon to toggle editability
#pencil_icon = PhotoImage(file='pencil_icon.png')  # Ensure the image file exists
toggle_button = tk.Button(root, text="Edit", command=toggle_editability)
toggle_button.grid(row=4, column=3, padx=5)


# Create a submit button
submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.grid(row=5, column=1)

# Start the Tkinter event loop
root.mainloop()    
    



