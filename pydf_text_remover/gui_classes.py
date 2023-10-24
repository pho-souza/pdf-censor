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
from pydf_text_remover.utils import (
    path_normalizer,
    is_dir,
)

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
        self.ui_commands()

    def set_initial_vars(self):
        self.__inputs = 0
        self.__max_inputs = 5
        self.pdf_inputs = []

    def set_replace_menus(self):
        if not hasattr(self,"ui_find_strucuture"):
            self.ui_find_strucuture = {}
            # Inputs
            self.label_find = {}
            self.string_find = {}
            self.label_replace = {}
            self.string_replace = {}
            self.remove_find_strucuture = {}

    def set_replaces(self):
        self.set_replace_menus()

        for key in self.keys:
            if not key in self.ui_find_strucuture.keys():
                self.ui_find_strucuture[key] = Frame(self.row_3)

                # Input
                self.label_find[key] = Label(
                    self.ui_find_strucuture[key],
                    text='Find:'
                )
                self.string_find[key] = Entry(
                    self.ui_find_strucuture[key]
                )
                # Replace
                self.label_replace[key] = Label(
                    self.ui_find_strucuture[key],
                    text='Replace:'
                )
                self.string_replace[key] = Entry(
                    self.ui_find_strucuture[key]
                )
                # Remove_BTN
                self.remove_find_strucuture[key] = Button(
                    self.ui_find_strucuture[key],
                    text='X',
                    command=lambda: self.input_updater(value=-1)
                )
        self.menu_update()

    def menu_update(self):
        row = 1
        for items in self.ui_find_strucuture.keys():
            self.ui_find_strucuture[items].grid_remove()

            self.label_find[items].grid_remove()
            self.string_find[items].grid_remove()
            self.label_replace[items].grid_remove()
            self.string_replace[items].grid_remove()
            self.remove_find_strucuture[items].grid_remove()

        for items in self.keys:
            self.ui_find_strucuture[items].grid(column=1, row=row)
            # Adiciona as labels
            self.label_find[items].grid(column=1, row=1)
            self.string_find[items].grid(column=2, row=1)
            self.label_replace[items].grid(column=1, row=2)
            self.string_replace[items].grid(column=2, row=2)
            self.remove_find_strucuture[items].grid(column=3, row=1, rowspan=2)

            row += 1

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

    def pdf_list(self):
        pass

    def basic_ui_draw(self):
        self.ui.grid(sticky='nwse')
        self.row_1.grid(column=1, row=1, sticky='nwse')
        self.row_2.grid(column=1, row=2, sticky='nwse')
        self.row_3.grid(column=1, row=3, sticky='nwse')
        self.pdf_list.grid(column=1, row=1, columnspan=2, sticky='nwse')

        self.btn_file_selector.grid(column=1, row=2, sticky='nwse')
        self.btn_pdf_export.grid(column=2, row=2, sticky='nwse')
        self.ui.grid_columnconfigure(1, weight=7)

        # Rows configuration
        self.row_1.grid_columnconfigure(1, weight=5)
        self.row_1.grid_columnconfigure(2, weight=5)

        self.row_1.grid_rowconfigure(1, weight=7)

        self.row_2.grid_columnconfigure(1, weight=6)
        self.row_2.grid_columnconfigure(2, weight=3)
        self.row_2.grid_columnconfigure(3, weight=3)

        # Parameter tab
        self.parameters_tab.grid(column = 0,  row = 0, sticky = 'nwse')

    def ui_commands(self):
        self.btn_pdf_export['command'] = self.return_keys
        self.pdf_list.drop_target_register(DND_FILES)
        self.pdf_list.dnd_bind("<<Drop>>",  self.add_file_drag_drop)

        self.pdf_list['columns'] = ['Files', 'Number of pages', 'Ver depois']

        self.pdf_list['show'] = 'headings'

        for col in self.pdf_list['columns']:
            if col == 'Files':
                self.pdf_list.column(col, minwidth=int(300))
            self.pdf_list.heading(col, text=col)

    def add_file_drag_drop(self, event):
        list_files = event.data
        if bool(re.search("^\\{", list_files)):
            list_files = re.sub('[ ]+\{', "", list_files)
            list_files = re.sub('\{', "", list_files)
            list_files = re.sub('\\\\', "/", list_files)
            list_files = re.sub('\}', ";", list_files)
            list_files = re.sub('^[ ]+', "", list_files)
            lista = list_files.split(";")
        else:
            lista = list_files.split()
        # print(lista)

        values = []
        for i in lista:
            if not i == '':
                pdf_inserted = re.sub("^[ ]+", "", i)
                value_pdf = (pdf_inserted, '', '')
                values.append(value_pdf)
        for i in values:
            self.pdf_list.insert('', 'end', values = i)
        self.validate_files()

    def validate_files(self):
        self.files = list()
        for line in self.pdf_list.get_children():
            print(line)
            pdf_file = self.pdf_list.item(line)['values'][0]
            print(pdf_file)
            self.files.append(pdf_file)
        # self.files = list(self.pdf_list.get_children(0, END))
        for file in self.files:
            self.files.remove(file)
            file = path_normalizer(file)
            self.files.append(file)

        for file in self.files:
            file = path_normalizer(file)
            extension = re.sub(".*[.](.*)", "\\1", str.upper(file))
            print(extension)
            if extension != "PDF" or is_dir(file):
                print(file)
                self.files.remove(file)
        self.files = set(self.files)
        self.files = list(self.files)

        self.remove_all_files()

        for i in self.files:
            # value_pdf = self.get_pdf_info(i)
            values = self.get_pdf_info(i)
            self.pdf_list.insert('', 'end',  values=values)
        self.set_status(f'There are {len(self.files)} PDFs files. ')

    def get_pdf_info(self, pdf_path = '', event=None):
        status = "Getting data from: " + pdf_path
        self.set_status(status)

        pdf = path_normalizer(pdf_path)

        pdf_path = os.path.abspath(pdf)

        pdf_path = path_normalizer(pdf_path)

        input_file = ['-i', pdf_path]

        argument_count_annots = input_file + ['--count-annotations']
        argument_count_pages = input_file + ['--total-pages']

        number_of_annots = '1'
        number_of_pages = '1'

        return (pdf_path, number_of_pages, number_of_annots)

    def return_keys(self, event=None):
        self.input_updater(1)
        # print(self.keys)

    def set_size(self, width = 500,  height = 500):
        self.width = width
        self.height = height

    def input_defined(self):
        """Atualiza dinamicamente lista de inputs"""
        # if len(self.pdf_list) < 1:
        #     self.__inputs = 0

    def input_updater(self, value=0):
        if self.__inputs + value <= 0:
            self.__inputs = 0
        elif self.__inputs + value > self.__max_inputs:
            self.__inputs = self.__max_inputs
        self.__inputs += value
        self.set_replaces()

    def remove_all_files(self):
        for line in self.pdf_list.get_children():
            self.pdf_list.delete(line)

    @property
    def keys(self):
        item_name = 'item_'
        return_items = []
        if self.__inputs < 1:
            return_items = []
        else:
            for i in range(1, self.__inputs):
                key_name = item_name + str(i)
                return_items.append(key_name)
        return return_items
