import tkinter as tk
from gui import create_gui

if __name__ == "__main__":
    #execute_python_code()
    root = tk.Tk()
    root.title('Solution Visualizer')
    create_gui(root)
    root.mainloop()
