import tkinter as tk
from ui_components import ProjectUI

def main():
    root = tk.Tk()
    app = ProjectUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
