import os
import zipfile
import tkinter as tk
from tkinter import ttk

class DWGZipper():
    def __init__(self, parent_frame):
        self.tool_frame = parent_frame
        self.setup_gui()
        pass
        
    def destroy(self):
        for child in self.tool_frame.winfo_children():
            child.destroy()
            
    def setup_gui(self):
        self.source_label = tk.Label(self.tool_frame, text="Source path: ")
        self.source_label.grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.source_entry = tk.Entry(self.tool_frame, width=75)
        self.source_entry.grid(row=0, column=1, columnspan=3, sticky='ew')
        
        self.source_browse_button = ttk.Button(
            self.tool_frame, style="TButton", text="Browse", command=lambda: self.create_file_dialog(self.source_entry)
        )
        self.source_browse_button.grid(row=0, column=4, padx=10, pady=5)

    def execute(self):
        output_folder = "zipped_dwg"
        os.makedirs(output_folder, exist_ok=True)
        
        for root, dirs, files in os.walk(base_folder):
            for dir in dirs:
                if "dwg" in dir or "DWG" in dir:
                    zip_path = os.path.join(output_folder, f"{dir}.zip")
                    self.zip_folder(os.path.join(root, dir), zip_path)
            
    def zip_folder(self, folder_path, zip_path):
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    # Preserve the folder structure inside the zip
                    arcname = os.path.relpath(full_path, start=folder_path)
                    zipf.write(full_path, arcname)

base_folder = "ziptest"



