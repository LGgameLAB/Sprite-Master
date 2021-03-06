from components import Part

def importPart(master):
    import tkinter as tk
    from tkinter import filedialog
    import os

    root = tk.Tk()
    root.withdraw() #use to hide tkinter window

    currdir = os.getcwd()
    tempdir = filedialog.askopenfile(parent=root, initialdir=currdir, title='Please select a directory')

    return Part(master.editor.canvas, tempdir)