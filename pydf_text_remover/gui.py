#!/usr/bin/env python
"""
GUI for text remover app
"""
import tkinter as tk
import tkinter.ttk as ttk
import os

from tkinterdnd2 import TkinterDnD

import pydf_text_remover.gui_classes as gui

# from . import __IMG_LOGO__


def main():
    """
    GUI for remover text app

    Returns:
        NONE: _description_
    """
    root = TkinterDnD.Tk()

    root.geometry('800x800')

    root.minsize(width=600, height=400)

    root.style = ttk.Style()

    root.style.theme_use('clam')
    root.style.configure(
        'status_bar.TLabel', background='green', bordercolor='red'
    )
    root.style.configure(
        'status_bar.TFrame', background='green', bordercolor='red'
    )
    root.style.configure(
        'replace_border.TLabel',
        borderwidth=5,
        bordercolor='green',
        background='red',
        relief='solid',
    )
    # replace.TLabelFrame
    root.style.configure(
        'replace.TLabelframe',
        borderwidth=5,
        bordercolor='gray',
        relief='groove',
        highlightthickness=10,
    )
    # root.style.configure('My.Red', background='red')

    def _quit():
        root.quit()
        root.destroy()
        print('APP FECHADO')
        return 0

    root.protocol('WM_DELETE_WINDOW', _quit)

    notebook = ttk.Notebook(root)
    # notebook.grid()
    notebook.grid_rowconfigure(1, weight=1)
    notebook.grid_columnconfigure(1, weight=1)

    load_pdf = gui.Gui_pdf_text_remover(notebook)

    load_pdf.set_size(
        width=root.winfo_screenmmwidth(), height=root.winfo_screenmmheight()
    )

    notebook.grid(sticky='nsew')

    notebook.add(load_pdf.ui, text='File choose')

    notebook.grid_columnconfigure(0, weight=10)
    notebook.grid_columnconfigure(1, weight=10)
    notebook.grid_rowconfigure(0, weight=10)

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    logo = tk.PhotoImage(file=gui.__IMG_LOGO__)

    root.iconphoto(False, logo)

    root.title('PDF Censor')

    root.mainloop()

    root.quit()


if __name__ == '__main__':
    main()
