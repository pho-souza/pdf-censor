# import tkinter as tk
# import tkinter.ttk as ttk
import json
import os
import re
import string
import tkinter.filedialog
from random import choices as random_choices
from threading import *
from tkinter import (
    END,
    BooleanVar,
    DoubleVar,
    IntVar,
    Listbox,
    PhotoImage,
    StringVar,
    Text,
    messagebox,
)
from tkinter.ttk import (
    Button,
    Checkbutton,
    Combobox,
    Entry,
    Frame,
    Label,
    Notebook,
    Progressbar,
    Scrollbar,
    Spinbox,
    Style,
    Treeview,
)

from tkinterdnd2 import DND_FILES

from pydf_text_remover.remover import text_remover


def threading():
    # Call work function
    t1 = Thread(target=text_remover)
    t1.start()


class gui_interface:
    def __init__(self, master=None) -> None:
        self.__master = master
        self.ui = Frame(self.__master)


class gui_pdf_text_remover(gui_interface):
    def __init__(self, master=None) -> None:
        self.__master = master
        self.ui = Frame(self.__master)
        self.assets_import()
        self.set_initial_vars()
        self.basic_ui()
        self.basic_ui_draw()

    def set_initial_vars(self):
        self.vars = {}
        self.vars['pdf_inputs'] = []
        self.vars['string_find'] = []
        self.vars['string_replace'] = ['']
        # self.custom_boxes = {}
        # self.custom_boxes[0] = {'string_find': StringVar()}

    def assets_import(self):
        pass

    def set_status(self, text=''):
        pass

    def basic_ui(self):
        """The basic user interface"""
        self.row_1 = Frame(self.ui)
        self.row_2 = Frame(self.ui)
        self.row_3 = Frame(self.ui)
        # List of PDFs
        self.pdf_list = Treeview(self.row_1)
        # Buttons of row_1
        self.btn_file_selector = Button(self.row_1, text='Select files')
        self.btn_pdf_export = Button(self.row_1, text='Export PDF highlights')
        # Column of buttons
        self.column_btns = Frame(self.row_1)

        # Parameters tab
        self.parameters_tab = Frame(self.row_2)
        self.parameters_label = Label(
            self.parameters_tab, text='Add parameters'
        )
        self.parameters_template_label = Label(
            self.parameters_tab, text='Select a template'
        )

    def basic_ui_draw(self):
        self.ui.grid(sticky='nwse')
        self.row_1.grid(column=1, row=1, sticky='nwse')
        self.row_2.grid(column=1, row=2, sticky='nwse')
        self.row_3.grid(column=1, row=3, sticky='nwse')
        self.pdf_list.grid(column=1, row=1, columnspan=2, sticky='nwse')

        self.btn_file_selector.grid(column=1, row=2, sticky='nwse')
        self.btn_pdf_export.grid(column=2, row=2, sticky='nwse')
        # self.ui.grid_columnconfigure(1, weight=7)
