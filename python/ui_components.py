import tkinter as tk

from ProjectfolderGenerator.generate_project_folder import ProjectFolderGenerator
from ConvertPDFtoJPG.convert_pdf import ConvertPDFtoJPG

class BaseUI:
    def __init__(self, size=(700,700)):
        self.setup_base_gui(size)
        self.root.mainloop()
    
    def on_tool_select(self, event):
        widget = event.widget    
        selection = widget.curselection()
        if not selection:
            return  
        index = selection[0]
        selected_tool = widget.get(index)
        
        if hasattr(self, 'active_widget') and self.active_widget:
            self.active_widget.destroy()
            self.active_widget = None
        
        self.tool_label.config(text=selected_tool)
        if selected_tool == "Zip DWG folders":
            #self.show_zip_ui()
            pass
        elif selected_tool == "Convert PDF to JPG":
            self.active_widget = ConvertPDFtoJPG(self.tool_frame)
            pass
        elif selected_tool == "Create new Project folder":
            self.active_widget = ProjectFolderGenerator(self.tool_frame)
        
        else:
            print("Unknown tool")
        
    def setup_base_gui(self, size=(700,700)):
       #Setting the root
        self.root = tk.Tk()
        self.root.title("Project Data Entry Form")
        self.root.geometry(f"{size[0]}x{size[1]}")
        
        #Setting up the frames
        self.root.grid_columnconfigure(1, weight=1)  # 1 par
        self.root.grid_columnconfigure(1, weight=3)  # 3 parts
        self.root.grid_rowconfigure(0, weight=1)
        
        self.left_frame = tk.Frame(self.root, bg='gray95', padx=20, pady=20, width=size[0]*0.33)
        self.right_frame = tk.Frame(self.root)
        self.left_frame.grid_propagate(False)
        self.left_frame.grid(row=0, column=0, sticky='nsw')
        self.right_frame.grid(row=0, column=1, sticky='nsew')
        self.left_frame.grid_rowconfigure(1, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)
        
        
        #Setting up the list
        listlabel = tk.Label(self.left_frame, text="Available tools:", font=("Helvetica", 14), bg='gray95')
        listlabel.grid(row=0, column=0, sticky='nsew', padx=10, pady=(10, 0))
        listbox = tk.Listbox(self.left_frame)
        listbox.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        listbox.bind('<<ListboxSelect>>', self.on_tool_select)
        
        #Add tools to list
        tools = [
            "Zip DWG folders",
            "Convert PDF to JPG",
            "Create new Project folder",
        ]
        for tool in tools:
            listbox.insert(tk.END, tool)
            
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(2, weight=1)
        
        #setting up title
        self.tool_label = tk.Label(
            self.right_frame,
            text="[TOOLNAME]",
            font=("Helvetica", 22),
        )
        self.right_frame.grid_rowconfigure(0, weight=0) 
        self.tool_label.grid(row=0, column=0, columnspan=3, sticky='nsew', padx=50, pady=20)
        
        self.tool_frame = tk.Frame(self.right_frame)
        self.tool_frame.grid(row=1, column=0)
        
        self.tool_frame.columnconfigure(0, weight=1)
        self.tool_frame.columnconfigure(1, weight=9)
        
   
