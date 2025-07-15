import tkinter as tk
from tkinter import filedialog, messagebox, ttk, RAISED
import traceback
from enum import Enum
from pydantic import BaseModel
import os



class Project(BaseModel):
    code: int
    location: str
    name: str
    client: str
    
class Type(Enum):
    TEXT_FILE = "Text File"
    TEMPLATE = "Template folder"

class ProjectFolderGenerator():
    def __init__(self, parent_frame):
        self.tool_frame = parent_frame
        self.ROOT_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.mode_var = tk.StringVar(value="folder")     
        self.setup_gui()
        self.type = Type.TEXT_FILE
        if self.type == Type.TEXT_FILE:
            self.template_path =os.path.abspath(os.path.join(self.ROOT_FOLDER, "ProjectFolderGenerator/folder_structure.txt"))
            print(self.template_path)
            self.lines = self.read_folder_structure(self.template_path)
       
     
        self.tool_description = ""      
        
    def destroy(self):
        for child in self.tool_frame.winfo_children():
            child.destroy()
            
    def create_folders(self, lines, project, path):
        base_path = os.path.join(path, f"{project.code}_{project.location}_{project.name}_{project.client}")
        print(base_path)
        os.mkdir(base_path)       
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
                    path_stack = path_stack[:indent_level // 4 + 1]  # Adjust the path stack
                    path_stack.append(os.path.join(path_stack[-1], folder_name))
                else:
                    path_stack[-1] = os.path.join(os.path.dirname(path_stack[-1]), folder_name)

                current_indent_level = indent_level

                # Create the directory
                os.makedirs(path_stack[-1], exist_ok=True)
    
    def read_folder_structure(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()

    def setup_gui(self):
        self.code_label = tk.Label(self.tool_frame, text="Project Code: ")
        self.code_label.grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.code_entry = tk.Entry(self.tool_frame)
        self.code_entry.grid(row=0, column=1, columnspan=8, sticky='ew')
            
        self.location_label = tk.Label(self.tool_frame, text="Location: ")
        self.location_label.grid(row=1, column=0, padx=5, pady=3,  sticky="w")
        self.location_entry = tk.Entry(self.tool_frame)
        self.location_entry.grid(row=1, column=1,columnspan=8, sticky='ew')
            
        self.name_label = tk.Label(self.tool_frame, text="Naam: ")
        self.name_label.grid(row=2, column=0, padx=5, pady=3, sticky="w")
        self.name_entry = tk.Entry(self.tool_frame)
        self.name_entry.grid(row=2, column=1,columnspan=8, sticky='ew', ipadx=100)
            
        self.client_label = tk.Label(self.tool_frame, text="Client: ")
        self.client_label.grid(row=3, column=0, padx=5, pady=3,  sticky="w")
        self.client_entry = tk.Entry(self.tool_frame)
        self.client_entry.grid(row=3, column=1, columnspan=8,  sticky="ew")
                
        self.path_label = tk.Label(self.tool_frame, text="Destination Path: ")
        self.path_label.grid(row=4, column=0, padx=5, pady=3,  sticky="w")
        self.path_entry = tk.Entry(self.tool_frame)
        self.path_entry.grid(row=4, column=1, columnspan=6, sticky='ew')
        
        
        self.path_browse_button = ttk.Button(
            self.tool_frame, style="TButton", text="Browse", command=lambda: self.create_file_dialog()
        )
        self.path_browse_button.grid(row=4, column=7, padx=1, pady=5)
        
        
        self.submit_button = ttk.Button(
            self.tool_frame, style="TButton", text="Create Folder", command=self.submit_form
        )
        self.submit_button.grid(row=5, column=0, padx=1, pady=5)
 
        
    def submit_form(self):
        try:
            print("try!")
            # Get data from entries
            code = self.code_entry.get()                
            location = self.location_entry.get()
            name = self.name_entry.get()
            client = self.client_entry.get()
            folder_path = self.path_entry.get()
                
            error_messages = [] 
            if not code:
                error_messages.append("Project Code is required.")
            elif not code.isdigit(): 
                error_messages.append("Project Code must be a number.")

            if not location:
                error_messages.append("Location is required.")
            elif not location.isalpha():
                error_messages.append("Location should only consist of letters.")
                
            if not name:
                error_messages.append("Name is required.")
            elif not location.isalpha():
                error_messages.append("Name should only consist of letters.")    
                
            if not client:
                error_messages.append("Client is required.")
            elif not location.isalpha():
                error_messages.append("Client should only consist of letters.")    
                
            if not folder_path:
                error_messages.append("Folder Path is required.")     
            
            if error_messages:
                messagebox.showerror("Validation Errors", "\n".join(error_messages))
                return 
                
            # Create Project object
            self.project = Project(code=int(code), location=location, name=name, client=client)

            # Create folder structure
            self.create_folders(self.lines, self.project, folder_path)

            messagebox.showinfo("Success", "Project data submitted successfully!")
            
        except Exception as e:   
            traceback.print_exc()
            messagebox.showerror("Unknown Error", f"An error occurred:\n{e}")
            
    def create_file_dialog(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.config(state='normal')
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)
            self.path_entry.config(state='disabled')
