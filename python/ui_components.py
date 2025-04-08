import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from folder_manager import FolderManager
from project_model import Project
from utils import read_folder_structure
from styles import apply_styles


class ProjectUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Data Entry Form")
        self.root.config(padx=20, pady=20, height=500, width=750)
        
    
        style = apply_styles()
                
        # Folder manager
        self.folder_manager = FolderManager(base_dir="") 
        self.lines = read_folder_structure("folder_structure.txt")  

        # Project Data Entry Form
        self.setup_form()

    def setup_form(self):
        
        #set up the tab notebook
        notebook = ttk.Notebook(self.root)
        notebook.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        
        # --> Setting up Tab 1 ---------------------------------------------
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Create Project")      
        
        #Label and entry field for the project code
        code_label = tk.Label(tab1, text="Project Code: ")
        code_label.grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.code_entry = tk.Entry(tab1)
        self.code_entry.grid(row=0, column=1, columnspan=3, sticky='ew')
        
        #Label and entry field for the project location
        location_label = tk.Label(tab1, text="Location: ")
        location_label.grid(row=1, column=0, padx=5, pady=3,  sticky="w")
        self.location_entry = tk.Entry(tab1)
        self.location_entry.grid(row=1, column=1, columnspan=3, sticky='ew')
         
        #Label and entry field for the project name
        name_label = tk.Label(tab1, text="Name: ")
        name_label.grid(row=2, column=0, padx=5, pady=3, sticky="w")
        self.name_entry = tk.Entry(tab1)
        self.name_entry.grid(row=2, column=1, columnspan=3, sticky='ew')
        
        #Label and entry field for the client name
        client_label = tk.Label(tab1, text="Client: ")
        client_label.grid(row=3, column=0, padx=5, pady=3,  sticky="w")
        self.client_entry = tk.Entry(tab1)
        self.client_entry.grid(row=3, column=1, columnspan=3, sticky='ew')
        
        #Label and entry field for the path name
        path_label = tk.Label(tab1, text="Path: ")
        path_label.grid(row=4, column=0, padx=5, pady=3,  sticky="w")
        self.path_entry = tk.Entry(tab1)
        self.path_entry.grid(row=4, column=1, sticky='ew')
        
        #Toggle editablitity of path entry        
        toggle_button = ttk.Button(tab1, style="TButton", text="Edit", command=self.toggle_editability)
        toggle_button.grid(row=4, column=2)
        #Opens file dialog for selecting a folder
        browse_button = ttk.Button(tab1,style="TButton", text="Browse", command=self.create_file_dialog)
        browse_button.grid(row=4, column=3, padx=10, pady=5)
        
        #submits the data to be created
        submit_button = ttk.Button(tab1,style="TButton", text="Submit", command=self.submit_form)
        submit_button.grid(row=5, column=0, columnspan=3, pady=5)
        
      
        tab1.grid_columnconfigure(1, weight=1)  
        tab1.grid_columnconfigure(2, weight=2)  
        tab1.grid_rowconfigure(0, weight=1)
        tab1.grid_rowconfigure(1, weight=1)
        tab1.grid_rowconfigure(2, weight=1)
        tab1.grid_rowconfigure(3, weight=1)
        tab1.grid_rowconfigure(4, weight=1)
        tab1.grid_rowconfigure(5, weight=1)
        
         # --> Setting up Tab 2 ---------------------------------------------
        #tab2 = ttk.Frame(notebook)
        #notebook.add(tab2, text="Folder Structure")
  

    def submit_form(self):
        try:
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
            project = Project(code=int(code), location=location, name=name, client=client)

            # Create folder structure
            self.folder_manager.create_folders(self.lines, project, folder_path)

            messagebox.showinfo("Success", "Project data submitted successfully!")
    
        except:
            messagebox.showerror("Unknown Error", "An Unknown Error has occured. :(")   
     

    def toggle_editability(self):
        current_state = self.path_entry.cget('state')
        new_state = 'normal' if current_state == 'disabled' else 'disabled'
        self.path_entry.config(state=new_state)

    def create_file_dialog(self):
        folder = filedialog.askdirectory()
        if folder:
            self.path_entry.config(state='normal')
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)
            self.path_entry.config(state='disabled')

