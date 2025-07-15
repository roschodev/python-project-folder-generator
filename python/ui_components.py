import tkinter as tk

from ProjectfolderGenerator.generate_project_folder import ProjectFolderGenerator
from ConvertPDFtoJPG.convert_pdf import ConvertPDFtoJPG
from DWGZipper.zip_dwg_folders import DWGZipper

class BaseUI:
    def __init__(self, size=(700,700)):
        
        self.tools = {
            # "Zip DWG folders": "Looks for folder names with DWG in it, then zips those.",
            "Convert PDF to JPG": "Checks a folder for PDF file, if it finds any it converts them to JPG files. Converts every page to a separate JPG.",
            "Folder Generator": "Generates a pre-defined folder structure at a specified location using project data. Specifically designed for creating project folder structures using the AGNOVA naming system."
        }
        self.setup_base_gui(size)
        self.root.mainloop()
        
    
    def on_tool_select(self, event):
        widget = event.widget    
        selection = widget.curselection()
        if not selection:
            return  
        index = selection[0]
        selected_tool = widget.get(index)
        description = self.tools.get(selected_tool, "No description available.")
        self.tool_description.config(text=description)
        
        if hasattr(self, 'active_widget') and self.active_widget:
            self.active_widget.destroy()
            self.active_widget = None
        
        self.tool_label.config(text=selected_tool)
        if selected_tool == "Folder Generator":
            self.active_widget = ProjectFolderGenerator(self.tool_frame)
            pass
        elif selected_tool == "Convert PDF to JPG":
            self.active_widget = ConvertPDFtoJPG(self.tool_frame, self.progress_frame)
            pass
        else:
            print("Unknown tool")
        
    def setup_base_gui(self, size=(500,500)):
       #Setting the root
        self.root = tk.Tk()
        self.root.title("AGNOVA Tools")
        self.root.geometry(f"{size[0]}x{size[1]}")
        
        #Configuring the root
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1) 
        
        #Dividing the screeen into two, 1:3
        
        #left frame size 1
        self.left_frame = tk.Frame(self.root, bg='gray85', padx=20, pady=20)
        self.left_frame.place(relx=0, rely=0, relwidth=0.25, relheight=1.0)
        
        #right frame size 3
        self.right_frame = tk.Frame(self.root, bg="gray85")
        self.right_frame.place(relx=0.25, rely=0, relwidth=0.75, relheight=1.0)
        self.right_frame.grid_rowconfigure(0, weight=1) 
        self.right_frame.grid_rowconfigure(1, weight=4)
        self.right_frame.grid_columnconfigure(0, weight=1) 
        
        
        #dividing right frame into 1:4
        #create tool info frame size 1
        self.tool_info_frame = tk.Frame(self.right_frame, bg='gray85')
        self.tool_info_frame.place(relx=0, rely=0, relwidth=1.0, relheight=0.15)
        #create tool frame size 4
        self.tool_frame = tk.Frame(self.right_frame, bg='gray95')
        self.tool_frame.place(relx=0, rely=0.15, relwidth=1.0, relheight=0.8)
         
        self.progress_frame = tk.Frame(self.right_frame, bg="gray90")
        self.progress_frame.place(relx=0, rely=0.95, relwidth=1.0, relheight=0.05)
        
        
        #Dividing tool info frame
        #create tool label size 0.2
        self.tool_label = tk.Label(
            self.tool_info_frame,
            text="Please select a tool",
            font=("Helvetica", 22),
            bg=self.tool_info_frame["bg"] 
        )
        self.tool_label.place(relx=0.5, rely=0.2, anchor="center")
        
        #create tool description size 0.7
        self.tool_description = tk.Label(
            self.tool_info_frame,
            text="When a tool has been selected, the description describing the tools intended purpose will be displayed here",
            wraplength=600,  
            height=3,      
            justify="center",
            anchor="center",
            bg=self.tool_info_frame["bg"]        
        )   
        self.tool_description.place(relx=0.5, rely=0.7, anchor="center", relwidth=0.9, relheight=0.6)  
        
        #Setting up the list
        listlabel = tk.Label(
            self.left_frame, 
            text="Available tools:", 
            font=("Helvetica", 14), 
            bg=self.left_frame["bg"],
            fg="black",
            anchor="center",
            
            )
        listlabel.place(relx=0, rely=0, relwidth=1, relheight=0.05)
        
        listbox = tk.Listbox(self.left_frame)
        listbox.place(relx=0, rely=0.075, relwidth=1, relheight=0.95)
        listbox.bind('<<ListboxSelect>>', self.on_tool_select)
        
        #Add tools to list
        for tool in self.tools:
            listbox.insert(tk.END, tool)
   
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(2, weight=1)
        
        
        
    
   
