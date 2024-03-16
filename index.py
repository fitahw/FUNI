import gui
import func
import tkinter as tk

def main():
    root = tk.Tk()
    app = gui.GUI(root)
    app.setButtonFunctions(lambda: func.clipper(app.getOutT(), app.getClipT(), app.getPathT()))
    root.mainloop()

if __name__ == "__main__":
    main()