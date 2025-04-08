
"""import os
import sys
from pydantic import BaseModel, ValidationError

import tkinter as tk
from tkinter import messagebox, filedialog, ttk


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
    
def add_folder():
    folder_name = folder_name_entry.get()
    if folder_name:  # Ensure the folder name is not empty
        # Add the folder to the tree under the "root" level (or under the selected parent folder)
        tree.insert('', 'end', text=folder_name, open=True)
        

def add_subfolder():
    folder_name = subfolder_name_entry.get()
    selected_item = tree.selection()
    if folder_name and selected_item:  # Ensure both a folder name and a selected folder exist
        tree.insert(selected_item, 'end', text=folder_name, open=True)
        

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
        base_dir = folderpath_entry.get()
        project = Project(Nummer=int(nummer), Plaats=plaats, Naam=naam, Opdrachtgever=opdrachtgever)

        create_folders(lines, project)
       
        # Update the entry box with the base path after it's created
        folderpath_entry.config(state='normal')  # Enable the entry box temporarily
        
        folderpath_entry.config(state='disabled')  # Disable it again
        
        messagebox.showinfo("Success", "Project data submitted successfully!")
    except ValidationError as e:
        messagebox.showerror("Error", f"Validation Error: {e}")
    except ValueError:
        messagebox.showerror("Error", "Number can only contain numeric values. Please enter valid data.")

def toggle_editability():
    if folderpath_entry.cget('state') == 'disabled':  # If entry is disabled
        folderpath_entry.config(state='normal')  # Enable editing
        toggle_button.config(text='Save')  # Change button text to 'Save'
    else:
        folderpath_entry.config(state='disabled')  # Disable editing
        toggle_button.config(text='Edit')  # Change button text back to 'Edit'

def create_file_dialog():
    folder = filedialog.askdirectory()
    print(folder)
    if folder:
        folderpath_entry.config(state='normal')
        folderpath_entry.delete(0, tk.END)
        folderpath_entry.insert(0, folder)
        folderpath_entry.config(state='disabled')


# Create the main Tkinter window
root = tk.Tk()
root.title("Project Data Entry Form")
root.config(padx=20, pady=20, height=500, width=500)



# Create a Notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Tab 2 - Folder Selector
tab2 = ttk.Frame(notebook, style="TButton")
notebook.add(tab2, text="Folder Structure")

# Treeview widget to display folders and subfolders
tree = ttk.Treeview(tab2)
tree.grid(column=0, row=1)

# Entry and button to add a new folder
folder_name_label = tk.Label(tab2, text="Enter Folder Name:")
folder_name_label.grid(padx=10, pady=5)
folder_name_entry = tk.Entry(tab2)
folder_name_entry.pack(padx=10, pady=5)
add_folder_button = tk.Button(tab2, text="Add Folder", command=add_folder)
add_folder_button.pack(padx=10, pady=5)

# Entry and button to add a subfolder
subfolder_name_label = tk.Label(tab2, text="Enter Subfolder Name:")
subfolder_name_label.pack(padx=10, pady=5)
subfolder_name_entry = tk.Entry(tab2)
subfolder_name_entry.pack(padx=10, pady=5)
add_subfolder_button = tk.Button(tab2, text="Add Subfolder", command=add_subfolder)
add_subfolder_button.pack(padx=10, pady=5)

# Tab 1 - Folder Selector
tab1 = ttk.Frame(notebook, style="TButton")
notebook.add(tab1, text="Create")

# Create labels and entry fields for each attribute
tk.Label(tab1, text="Nummer:").grid(row=0, column=0)
nummer_entry = tk.Entry(tab1, width=30)
nummer_entry.grid(row=0, column=1)

tk.Label(tab1, text="Plaats:").grid(row=1, column=0)
plaats_entry = tk.Entry(tab1, width=30)
plaats_entry.grid(row=1, column=1)

tk.Label(tab1, text="Naam:").grid(row=2, column=0)
naam_entry = tk.Entry(tab1, width=30)
naam_entry.grid(row=2, column=1)

tk.Label(tab1, text="Opdrachtgever:").grid(row=3, column=0)
opdrachtgever_entry = tk.Entry(tab1, width=30)
opdrachtgever_entry.grid(row=3, column=1)

# Create an Entry widget (initially disabled)
tk.Label(tab1, text="Folder Path:").grid(row=4, column=0)
folderpath_entry = tk.Entry(tab1, width=30)
folderpath_entry.insert(0, base_dir)
folderpath_entry.config(state='disabled')
folderpath_entry.grid(row=4, column=1)

toggle_button = tk.Button(tab1, text="Edit", command=toggle_editability)
toggle_button.grid(row=4, column=3, padx=5)
browse_button = tk.Button(tab1, text="Browse",command=create_file_dialog)
browse_button.grid(row=4, column=4, padx=5)

# Create a submit button
submit_button = tk.Button(tab1, text="Submit", command=submit_form)
submit_button.grid(row=5, column=1)

# Start the Tkinter event loop
root.mainloop()    
    



"""