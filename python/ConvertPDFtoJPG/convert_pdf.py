from pdf2image import convert_from_path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import platform
import subprocess


class ConvertPDFtoJPG():
    def __init__(self, parent_frame, progress_frame):
        
        self.tool_frame = parent_frame
        self.progress_frame = progress_frame
        
        self.progress_label = tk.Label(self.progress_frame, text="Progress: 0/0", font=("Helvetica", 10), anchor="center")
        self.progress_label.pack(fill="both", padx=10, pady=5)
        
        self.setup_gui()
        
      
        
        
        self.DPI = 100
        
    def open_folder(self, path):
        try:
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", path])
            else:  # Linux
                subprocess.run(["xdg-open", path])
        except Exception as e:
            print(f"Could not open folder: {e}")  
                  
    def destroy(self):
        self.container.destroy()
        for child in self.progress_frame.winfo_children():
            child.destroy()     
        
    def setup_gui(self):
        self.container = tk.Frame(self.tool_frame)
        self.container.grid(row=0, column=0, sticky="nsew")
        
        self.source_label = tk.Label(self.container, text="Source path: ")
        self.source_label.grid(row=0, column=0, padx=5, pady=3, sticky="w")
        self.source_entry = tk.Entry(self.container, width=75)
        self.source_entry.grid(row=0, column=1, columnspan=3, sticky='ew')
        
        self.source_browse_button = ttk.Button(
            self.container, style="TButton", text="Browse", command=lambda: 
                self.create_file_dialog(self.source_entry)
                
        )
        self.source_browse_button.grid(row=0, column=4, padx=10, pady=5)
            
        self.output_label = tk.Label(self.container, text="Output path: ")
        self.output_label.grid(row=1, column=0, padx=5, pady=3,  sticky="w")
        self.output_entry = tk.Entry(self.container,width=75)
        self.output_entry.grid(row=1, column=1,columnspan=3, sticky='ew')
        
        self.template_browse_button = ttk.Button(
            self.container, style="TButton", text="Browse", command=lambda: self.create_file_dialog(self.output_entry)
        )
        self.template_browse_button.grid(row=1, column=4, padx=10, pady=5)
        
        self.convert_button = ttk.Button(
            self.container, style="TButton", text="Convert", command=self.convert
            )
        
        self.convert_button.grid(row=3, column=0, padx=1, pady=5)
        
        self.open_folder_button = ttk.Button(
            self.container,
            style="TButton",
            text="Open Destination Folder",
            command=lambda: self.open_folder(self.output_entry.get())
        )
        self.open_folder_button.grid(row=3, column=1, padx=1, pady=5)
        self.open_folder_button["state"] = "disabled"
        
    def get_pdfs(self):
        pdf_files = []
        for root, dirs, files in os.walk(self.source_folder):
            for file in files:
                if file.lower().endswith('.pdf') and not file.startswith("._"):
                    pdf_files.append(os.path.join(root, file))
        return pdf_files            
     
    def create_file_dialog(self, field):
        folder = filedialog.askdirectory(mustexist=True)
        if folder:
            field.delete(0, tk.END)
            field.insert(0, folder)
            
        if field == self.source_entry:
            source_folder = os.path.normpath(folder)
            pdf_count = sum(
                1 for root, _, files in os.walk(source_folder)
                for file in files if file.lower().endswith('.pdf')
            )
            self.progress_label.config(text=f"Found {pdf_count} PDFs")    
    
    def convert(self):
        raw_source = self.source_entry.get().strip()
        raw_output = self.output_entry.get().strip()
      
        
        error_messages = [] 
        if not raw_source:
            error_messages.append("Please input a source destination!")
        if not raw_output:
            error_messages.append("Please input an output destination!")
            
        if error_messages:
            messagebox.showerror("Validation Errors", "\n".join(error_messages))
            return
        
        self.source_folder = os.path.normpath(self.source_entry.get().strip())
        self.output_folder = os.path.normpath(self.output_entry.get().strip())    

        print(f"Looking in source folder: {self.source_folder}")
        print(f"Folder exists? {os.path.exists(self.source_folder)}")

        pdf_files = self.get_pdfs()

        self.number_of_pdfs = len(pdf_files)
        
        if self.number_of_pdfs == 0:
            self.progress_label.config(text="No PDF files found.")
            return
        
        
        self.progress_label.config(text=f"Progress: 0/{self.number_of_pdfs}")
        self.progress_frame.update_idletasks()  # Force update

        for i, pdf_path in enumerate(pdf_files, start=1):
            print(f"Processing: {pdf_path}")
            pages = convert_from_path(pdf_path, dpi=100)
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]

            for count, page in enumerate(pages):
                os.makedirs(self.output_folder, exist_ok=True)
                output_file = os.path.join(self.output_folder, f"{base_name}_page{count}.jpg")
                page.save(output_file, 'JPEG')

            self.progress_label.config(text=f"Progress: {i}/{self.number_of_pdfs}")
            self.progress_frame.update_idletasks()
            if self.number_of_pdfs == i:
                self.progress_label.config(text=f"Done! {i}/{self.number_of_pdfs}")
                self.open_folder_button["state"] = "active"
                


        




