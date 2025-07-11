from pdf2image import convert_from_path
import tkinter as tk
import os


class ConvertPDFtoJPG():
    def __init__(self, parent_frame):
        self.setup_gui()
        
        
        self.source_folder = ""
        self.output_folder = ""
        self.DPI = 100
        self.tool_frame = parent_frame
        
    
    def setup_gui(self):
        self.source_label = tk.Label(self.tool_frame, text="Source path: ")
        self.source_label.grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.source_entry = tk.Entry(self.tool_frame)
        self.source_entry.grid(row=0, column=1, columnspan=3, sticky='ew')
            
        self.output_label = tk.Label(self.tool_frame, text="Output path: ")
        self.output_label.grid(row=1, column=0, padx=5, pady=3,  sticky="w")
        self.output_entry = tk.Entry(self.tool_frame)
        self.output_entry.grid(row=1, column=1,columnspan=3, sticky='ew')
        pass
    
    def convert(self):
        for root, dirs, files in os.walk(self.source_folder):
            for file in files:
                if file.lower().endswith('.pdf'):
                    file_path = os.path.join(root, file)
                    pages = convert_from_path(file_path, dpi=self.DPI)
                    for count, page in enumerate(pages):
                        if os.path.exists(os.path.join(root, self.output_folder)):
                            page.save(f'{root}/zipped/{file}_pag{count}.jpg', 'JPEG')
                        else:
                            os.makedirs(f"{root}/zipped")


        




