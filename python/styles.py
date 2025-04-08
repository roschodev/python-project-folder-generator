from tkinter import ttk

def apply_styles():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure('TButton', font=('Arial', 12), padding=10, relief='flat', background='#4CAF50', foreground='white')
    style.map('TButton', background=[('active', '#45a049')])
    # Add other style configurations for widgets as needed

    # Style for TButton (general button style)
    style.configure('TButton',
                    font=('Arial', 12),            
                    padding=10,                 
                    relief='flat',              
                    background='#4CAF50',       
                    foreground='white',           
                    borderwidth=0,               
                    anchor='center')
    
    style.map('TButton',
            background=[('active', '#45a049')],  # Change background color when the button is active
            relief=[('pressed', 'sunken'), ('!pressed', 'flat')])  # Change relief style when pressed  
    
    return style  