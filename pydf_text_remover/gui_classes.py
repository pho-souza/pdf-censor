# import tkinter as tk
# import tkinter.ttk as ttk
import os
import re
import tkinter.filedialog as filedialog
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
from pydf_text_remover.utils import is_dir, path_normalizer


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
        self.ui_commands()
        self.basic_ui_draw()
        self.set_replaces()

    def set_initial_vars(self):
        self.__inputs = 1
        self.__max_inputs = 5
        self.pdf_inputs = []

    def set_replace_menus(self):
        if not hasattr(self, 'ui_find_strucuture'):
            self.ui_find_strucuture = {}
            # Inputs
            self.label_find = {}
            self.string_find = {}
            self.label_replace = {}
            self.string_replace = {}
            self.remove_find_strucuture = {}
            self.add_find_strucuture = {}
            # Vars
            self.vars_find = {}
            self.vars_replace = {}

    def set_replaces(self):
        self.set_replace_menus()

        for key in self.keys:
            if not key in self.ui_find_strucuture.keys():
                self.ui_find_strucuture[key] = Frame(self.row_3)
                # Vars
                self.vars_find[key] = StringVar()
                self.vars_replace[key] = StringVar()
                # Input
                self.label_find[key] = Label(
                    self.ui_find_strucuture[key], text='Find:'
                )
                self.string_find[key] = Entry(
                    self.ui_find_strucuture[key],
                    textvariable=self.vars_find[key],
                )
                # Replace
                self.label_replace[key] = Label(
                    self.ui_find_strucuture[key], text='Replace:'
                )
                self.string_replace[key] = Entry(
                    self.ui_find_strucuture[key],
                    textvariable=self.vars_replace[key],
                )
                # TBN add new_structure
                if key == 'item_1':
                    self.add_find_strucuture[key] = Button(
                        self.ui_find_strucuture[key],
                        text='+',
                        command=lambda: self.input_updater(value=1),
                    )
                # Remove_BTN
                if key != 'item_1':
                    self.remove_find_strucuture[key] = Button(
                        self.ui_find_strucuture[key],
                        text='-',
                        command=lambda: self.input_updater(value=-1),
                    )
        self.menu_update()

    def add_file(self):
        file_open = filedialog.askopenfiles(
            defaultextension=['pdf'], filetypes=[('PDF', '.pdf')]
        )
        if isinstance(file_open, list):
            for i in file_open:
                file = i.name
                path = os.path.abspath(file)
                if not is_dir(file):
                    values = (file, '', '')
                    self.pdf_list.insert('', 'end', values=values)
        else:
            file = os.path.abspath(file_open)
            if not is_dir(file):
                values = self.get_pdf_info(file)
                self.pdf_list.insert('', 'end', values=values)
        self.validate_files()

    def menu_update(self):
        row = 1
        for key in self.ui_find_strucuture.keys():
            self.ui_find_strucuture[key].grid_remove()
            self.label_find[key].grid_remove()
            self.string_find[key].grid_remove()
            self.label_replace[key].grid_remove()
            self.string_replace[key].grid_remove()
            if key == 'item_1':
                self.add_find_strucuture[key].grid_remove()
            if key != 'item_1':
                self.remove_find_strucuture[key].grid_remove()
        print(f'Chaves são: {self.keys}')
        for key in self.keys:
            self.ui_find_strucuture[key].grid(column=1, row=row)
            # Adiciona as labels
            self.label_find[key].grid(column=1, row=1)
            self.string_find[key].grid(column=2, row=1, sticky='nwse')
            self.label_replace[key].grid(column=1, row=2)
            self.string_replace[key].grid(column=2, row=2, sticky='nwse')
            if key == 'item_1':
                self.add_find_strucuture[key].grid(
                    column=3, row=1, rowspan=2, sticky='nwse'
                )
            if key != 'item_1':
                self.remove_find_strucuture[key].grid(
                    column=3, row=1, rowspan=2, sticky='nwse'
                )
            row += 1

    def assets_import(self):
        self.icon_delete = PhotoImage(
            file=os.path.abspath('pydf_text_remover/gui_assets/delete.png')
        )
        self.icon_trash = PhotoImage(
            file=os.path.abspath('pydf_text_remover/gui_assets/trash.png')
        )

    def set_values(self, event=None):
        self.strings_to_find = []
        self.strings_to_replace = []
        for key in self.keys:
            find = self.vars_find[key].get()
            replace = self.vars_replace[key].get()
            self.strings_to_find.append(find)
            self.strings_to_replace.append(replace)

    def set_status(self, text=''):
        pass

    def basic_ui(self):
        """The basic user interface"""
        self.row_1 = Frame(self.ui)
        self.row_2 = Frame(self.ui)
        self.row_3 = Frame(self.ui)
        # List of PDFs
        self.pdf_list = Treeview(self.row_1)
        self.column_btns = Frame(self.row_1)

        self.btn_remove_item = Button(self.column_btns, image=self.icon_delete)
        self.btn_remove_all_files = Button(
            self.column_btns, image=self.icon_trash
        )
        # Buttons of row_1
        self.btn_file_selector = Button(self.row_1, text='Select files')
        self.btn_pdf_export = Button(self.row_1, text='Export PDF highlights')
        # Column of buttons

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
        self.ui.grid_columnconfigure(1, weight=7)
        # self.ui.grid_rowconfigure(2, weight=3)

        self.column_btns.grid(column=3, row=1, rowspan=2)
        self.btn_remove_item.grid()
        self.btn_remove_all_files.grid()

        # Rows configuration
        self.row_1.grid_columnconfigure(1, weight=5)
        self.row_1.grid_columnconfigure(2, weight=5)

        self.row_1.grid_rowconfigure(1, weight=7)

        self.row_2.grid_columnconfigure(1, weight=6)
        self.row_2.grid_columnconfigure(2, weight=3)
        self.row_2.grid_columnconfigure(3, weight=3)

        # Parameter tab
        self.parameters_tab.grid(column=0, row=0, sticky='nwse')

    def ui_commands(self):
        self.btn_pdf_export['command'] = self.select_folder
        self.pdf_list.drop_target_register(DND_FILES)
        self.pdf_list.dnd_bind('<<Drop>>', self.add_file_drag_drop)
        self.btn_file_selector['command'] = self.add_file
        self.btn_remove_all_files['command'] = self.remove_all_files
        self.btn_remove_item['command'] = self.remove_file

        self.pdf_list['columns'] = ['Files', 'Number of pages', 'Ver depois']

        self.pdf_list['show'] = 'headings'

        for col in self.pdf_list['columns']:
            if col == 'Files':
                self.pdf_list.column(col, minwidth=int(300))
            self.pdf_list.heading(col, text=col)

    def add_file_drag_drop(self, event):
        list_files = event.data
        space_names = []
        if bool(re.search('\\{', list_files)):
            space_names = re.findall('\{.*?\}', list_files)
            list_files = re.sub('\{.*?\}', '', list_files)

        list_files = re.sub('[ ]+', ';', list_files)
        list_files = list_files.split(';')

        lista = list_files
        if space_names:
            for space in space_names:
                space = re.sub(pattern='\}[ ]+\{', repl=';', string=space)
                space = re.sub(pattern='(^\{|\}$)', repl='', string=space)
                lista.append(space)

        print(f'\n\n\nLISTA: {lista}\n\n\n')

        values = []
        for i in lista:
            if not i == '' and os.path.exists(i):
                pdf_inserted = re.sub('^[ ]+', '', i)
                value_pdf = (pdf_inserted, '', '')
                values.append(value_pdf)
        for i in values:
            self.pdf_inputs.append(i)
            self.pdf_list.insert('', 'end', values=i)
        self.validate_files()

    def check_if_pdf(self):
        print(
            f'ANTES === files: {self.pdf_inputs} - len: {len(self.pdf_inputs)}'
        )
        elimintate = []
        for file in self.pdf_inputs:
            # self.pdf_inputs.remove(file)
            # file = path_normalizer(file)
            extension = re.sub('.*[.]([A-Z]{3}$)', '\\1', str.upper(file))
            print(f'file: {file} - ext: {extension} - id_dir: {is_dir(file)}')
            if extension == 'PDF' and not is_dir(file):
                pass
            else:
                elimintate.append(file)

        for e in elimintate:
            self.pdf_inputs.remove(e)

        self.pdf_inputs = set(self.pdf_inputs)
        self.pdf_inputs = list(self.pdf_inputs)

        print(
            f'DEPOIS === files: {self.pdf_inputs} - len: {len(self.pdf_inputs)}'
        )

        print(f'PDF_INPUTS: {self.pdf_inputs}')
        self.remove_all_files()

    def validate_files(self):
        self.pdf_inputs = list()
        for line in self.pdf_list.get_children():
            pdf_file = self.pdf_list.item(line)['values'][0]
            self.pdf_inputs.append(pdf_file)
            self.pdf_list.delete(line)

        self.check_if_pdf()

        for i in self.pdf_inputs:
            values = self.get_pdf_info(i)
            self.pdf_list.insert('', 'end', values=values)

        self.set_status(f'There are {len(self.pdf_inputs)} PDFs files. ')

    def get_pdf_info(self, pdf_path='', event=None):
        status = 'Getting data from: ' + pdf_path
        self.set_status(status)

        pdf = path_normalizer(pdf_path)

        pdf_path = os.path.abspath(pdf)

        pdf_path = path_normalizer(pdf_path)

        input_file = ['-i', pdf_path]

        number_of_annots = '1'
        number_of_pages = '1'

        return (pdf_path, number_of_pages, number_of_annots)

    def return_keys(self, event=None):
        self.input_updater(1)
        print(f'__inputs: {self.__inputs} - keys: {self.keys}')
        # print(self.keys)

    def set_size(self, width=500, height=500):
        self.width = width
        self.height = height

    def input_defined(self):
        """Atualiza dinamicamente lista de inputs"""

    def input_updater(self, value=0):
        print(f'input_updater antes: {self.__inputs}')
        if self.__inputs + value < 1:
            self.__inputs = 0
        elif self.__inputs + value >= self.__max_inputs:
            self.__inputs = self.__max_inputs
        else:
            self.__inputs = self.__inputs + value
        print(f'input_updater depois: {self.__inputs}')
        self.set_replaces()

    def select_folder(self, event=None):
        if self.pdf_inputs:
            self.export_folder = filedialog.askdirectory(
                title='Select folder to save PDFs.'
            )
            print(f'Export folder: {self.export_folder}')
            self.export_pdfs()

    def export_pdfs(self, event=None):
        self.set_values()
        for pdf in self.pdf_inputs:
            # t1 = Thread(
            #     target=text_remover,
            #     kwargs={
            #         'pdf_input': pdf,
            #         'string_find': self.strings_to_find,
            #         'string_replace': self.strings_to_replace,
            #         'folder': self.export_folder,
            #     }
            # )
            text_remover(
                pdf_input=pdf,
                string_find=self.strings_to_find,
                string_replace=self.strings_to_replace,
                folder=self.export_folder,
            )
            # t1.start()
            print(f'\n\nFile: "{pdf}" exported!')

    def remove_file(self, event=None):
        if self.pdf_list.selection():
            selected_items = self.pdf_list.selection()
            for item in selected_items:
                # print(item)
                self.pdf_list.delete(item)

    def remove_all_files(self):
        for line in self.pdf_list.get_children():
            self.pdf_list.delete(line)

    def get_keys(self):
        item_name = 'item_'
        return_items = []
        if self.__inputs < 1:
            return_items = []
        else:
            for i in range(1, self.__inputs + 1):
                print(i)
                key_name = item_name + str(i)
                return_items.append(key_name)
        return return_items

    @property
    def keys(self):
        return self.get_keys()
