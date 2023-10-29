# import tkinter as tk
# import tkinter.ttk as ttk
import locale
import os
import re
import threading
import tkinter.filedialog as filedialog
import traceback
from copy import deepcopy
from threading import Thread
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
    LabelFrame,
    Notebook,
    Progressbar,
    Scrollbar,
    Spinbox,
    Treeview,
)

import fitz
from tkinterdnd2 import DND_FILES

from pydf_text_remover.remover import text_remover
from pydf_text_remover.utils import is_dir, path_normalizer

from . import (
    __DIR__,
    __IMG_ADD__,
    __IMG_DELETE__,
    __IMG_FILE__,
    __IMG_LOGO__,
    __IMG_SAVE__,
    __IMG_TRASH__,
)

locale.setlocale(locale.LC_ALL, '')


class gui_interface:
    def __init__(self, master=None) -> None:
        self.__master = master
        self.ui = Frame(self.__master)


class Gui_pdf_text_remover(gui_interface):
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
        self.__inputs_open = ['item_1']
        self.status_text = StringVar()
        self.status_text.set('PDF Censor open')

    def set_replace_menus(self):
        if not hasattr(self, 'replaces'):
            self.replaces = {}
            # self.replaces = {}
            # # Inputs
            # self.label_find = {}
            # self.string_find = {}
            # self.label_replace = {}
            # self.string_replace = {}
            # self.btn_remove_find_strucuture = {}
            # self.btn_add_find_structure = {}
            # # Vars
            # self.vars_find = {}
            # self.vars_replace = {}

    def remove_replace_menu(self, key='', event=None):
        """
        Remove key from list
        """
        if key in self.replaces.keys() and key != 'item_1':
            del self.replaces[key]
            self.menu_update()
        self.menu_update()

    def add_replace_menu(self, key='', event=None):
        """
        Add key to the list
        """
        if key not in self.replaces.keys():
            self.replaces[key] = {}
            self.replaces[key]['frame_master'] = LabelFrame(
                self.row_3, text='Replace', style='replace.TLabelframe'
            )
            # Vars
            self.replaces[key]['vars_find'] = StringVar()
            self.replaces[key]['vars_replace'] = StringVar()
            # Input
            self.replaces[key]['label_find'] = Label(
                self.replaces[key]['frame_master'], text='Find:'
            )
            self.replaces[key]['string_find'] = Entry(
                self.replaces[key]['frame_master'],
                textvariable=self.replaces[key]['vars_find'],
            )
            # Replace
            self.replaces[key]['label_replace'] = Label(
                self.replaces[key]['frame_master'], text='Replace:'
            )
            self.replaces[key]['string_replace'] = Entry(
                self.replaces[key]['frame_master'],
                textvariable=self.replaces[key]['vars_replace'],
            )
            # TBN add new_structure
            self.replaces[key]['btn_add_frame'] = Button(
                self.replaces[key]['frame_master'],
                image=self.icon_add,
                # text='+',
                command=lambda: self.input_updater(value=1),
            )
            # Remove_BTN
            self.replaces[key]['btn_rm_frame'] = Button(
                self.replaces[key]['frame_master'],
                image=self.icon_delete,
                # text='-',
                command=lambda: [
                    self.input_updater(value=-1),
                    self.remove_items(item=key),
                ],
            )

    def set_replaces(self):
        self.set_replace_menus()
        for key in self.keys:
            if not key in self.replaces.keys():
                self.add_replace_menu(key=key)
        replaces_keys = list(self.replaces.keys())
        for key in replaces_keys:
            if not key in self.keys:
                self.remove_replace_menu(key=key)
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
        for key in self.replaces.keys():
            self.replaces[key]['frame_master'].grid_remove()
            self.replaces[key]['label_find'].grid_remove()
            self.replaces[key]['string_find'].grid_remove()
            self.replaces[key]['label_replace'].grid_remove()
            self.replaces[key]['string_replace'].grid_remove()
            self.replaces[key]['btn_add_frame'].grid_remove()
            self.replaces[key]['btn_rm_frame'].grid_remove()
        print(f'Chaves são: {self.keys}')
        for key in self.keys:
            self.replaces[key]['frame_master'].grid(
                column=1, row=row, columnspan=3, sticky='nwse'
            )
            # self.replaces[key]['frame_master'].grid_columnconfigure(
            #     1, weight=1
            # )
            self.replaces[key]['frame_master'].grid_columnconfigure(
                2, weight=5
            )
            # self.replaces[key]['frame_master'].grid_columnconfigure(
            #     3, weight=1
            # )
            # Adiciona as labels
            self.replaces[key]['label_find'].grid(
                column=1, row=1, sticky='nse'
            )
            self.replaces[key]['string_find'].grid(
                column=2, row=1, sticky='nwse'
            )
            self.replaces[key]['label_replace'].grid(
                column=1, row=2, sticky='nse'
            )
            self.replaces[key]['string_replace'].grid(
                column=2, row=2, sticky='nwse'
            )
            if key == 'item_1':
                self.replaces[key]['btn_add_frame'].grid(
                    column=3, row=1, rowspan=2, sticky='nse'
                )
            if key != 'item_1':
                self.replaces[key]['btn_rm_frame'].grid(
                    column=3, row=1, rowspan=2, sticky='nse'
                )
            row += 1

    def assets_import(self):
        self.icon_delete = PhotoImage(file=__IMG_DELETE__)
        self.icon_trash = PhotoImage(file=__IMG_TRASH__)
        self.icon_add = PhotoImage(file=__IMG_ADD__)
        self.icon_save = PhotoImage(file=__IMG_SAVE__)
        self.icon_file = PhotoImage(file=__IMG_FILE__)

    def set_values(self, event=None):
        self.strings_to_find = []
        self.strings_to_replace = []
        for key in self.keys:
            find = self.replaces[key]['vars_find'].get()
            replace = self.replaces[key]['vars_replace'].get()
            self.strings_to_find.append(find)
            self.strings_to_replace.append(replace)

    def set_status(self, text=''):
        self.status_text.set(text)

    def basic_ui(self):
        """The basic user interface"""
        self.row_1 = Frame(self.ui)
        self.row_2 = Frame(self.ui)
        self.row_3 = Frame(self.ui)
        self.row_4 = Frame(self.ui)
        self.row_5 = Frame(self.ui)
        # List of PDFs
        self.pdf_list = Treeview(self.row_1)
        self.column_btns = Frame(self.row_1)

        self.btn_remove_item = Button(self.column_btns, image=self.icon_delete)
        self.btn_remove_all_files = Button(
            self.column_btns, image=self.icon_trash
        )
        # Buttons of row_1
        self.btn_file_selector = Button(self.row_1, text='Select files')
        self.btn_pdf_export = Button(
            self.row_1, text='Select exportation folder'
        )
        # Column of buttons

        # Parameters tab
        self.parameters_tab = Frame(self.row_2)
        self.parameters_label = Label(
            self.parameters_tab, text='Add parameters'
        )
        self.parameters_template_label = Label(
            self.parameters_tab, text='Select a template'
        )

        # Add Status bar
        self.status_bar = Label(self.row_5, textvariable=self.status_text)

    def basic_ui_draw(self):
        self.ui.grid(sticky='nwse')
        self.row_1.grid(column=1, row=1, sticky='nwse')
        self.row_2.grid(column=1, row=2, sticky='nwse')
        self.row_3.grid(column=1, row=3, sticky='nwse')
        self.row_4.grid(column=1, row=4, sticky='nswe')
        self.row_5.grid(column=1, row=5, sticky='swe')
        self.pdf_list.grid(column=1, row=1, columnspan=2, sticky='nwse')

        self.btn_file_selector.grid(column=1, row=2, sticky='nwse')
        self.btn_pdf_export.grid(column=2, row=2, sticky='nwse')
        self.ui.grid_columnconfigure(1, weight=7)

        # self.ui.grid_rowconfigure(1, weight=3)
        self.ui.grid_rowconfigure(4, weight=3)

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

        self.row_3.grid_columnconfigure(1, weight=5)
        self.row_3.grid_columnconfigure(2, weight=5)

        # Parameter tab
        self.parameters_tab.grid(column=0, row=0, sticky='nwse')
        self.status_bar.grid(sticky='wse')

    def ui_commands(self):
        self.btn_pdf_export['command'] = self.select_folder
        self.pdf_list.drop_target_register(DND_FILES)
        self.pdf_list.dnd_bind('<<Drop>>', self.add_file_drag_drop)
        self.btn_file_selector['command'] = self.add_file
        self.btn_remove_all_files['command'] = self.remove_all_files
        self.btn_remove_item['command'] = self.remove_file

        self.pdf_list['columns'] = ['Files', 'Pages', 'Size (KB)']

        self.pdf_list['show'] = 'headings'

        for col in self.pdf_list['columns']:
            if col == 'Files':
                self.pdf_list.column(col, minwidth=int(400))
            else:
                self.pdf_list.column(col, anchor='e', minwidth=100)
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

        if len(values) > 0:
            status_message = f'{len(values)} new files added'
            self.set_status(status_message)
        self.validate_files()

    def check_if_pdf(self):
        # print(
        #     f'ANTES === files: {self.pdf_inputs} - len: {len(self.pdf_inputs)}'
        # )
        elimintate = []
        for file in self.pdf_inputs:
            # self.pdf_inputs.remove(file)
            # file = path_normalizer(file)
            extension = re.sub('.*[.]([A-Z]{3}$)', '\\1', str.upper(file))
            # print(f'file: {file} - ext: {extension} - id_dir: {is_dir(file)}')
            if extension == 'PDF' and not is_dir(file):
                pass
            else:
                elimintate.append(file)

        for e in elimintate:
            self.pdf_inputs.remove(e)

        self.pdf_inputs = set(self.pdf_inputs)
        self.pdf_inputs = list(self.pdf_inputs)

        # print(
        #     f'DEPOIS === files: {self.pdf_inputs} - len: {len(self.pdf_inputs)}'
        # )

        print(f'PDF_INPUTS: {self.pdf_inputs}')
        # self.remove_all_files()

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

        file_size = int(os.path.getsize(pdf_path) / (1024))
        file_size = f'{file_size:n}'

        pdf = fitz.open(pdf_path)

        number_of_pages = len(pdf)

        pdf.close()

        # number_of_pages = '1'

        return (pdf_path, number_of_pages, file_size)

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
        item = 'item_'
        if self.__inputs + value < 1:
            self.__inputs = 1
            self.__inputs_open = [item + '1']
        elif self.__inputs + value >= self.__max_inputs:
            self.__inputs = self.__max_inputs
        else:
            self.__inputs = self.__inputs + value
            item = item + str(self.__inputs)

        # self.__inputs_open = list(range(1, self.__inputs+1))
        print(f'input_updater depois: {self.__inputs} - item: {item}')
        self.set_replaces()

    def select_folder(self, event=None):
        if self.pdf_inputs:
            self.export_folder = filedialog.askdirectory(
                title='Select folder to save PDFs.'
            )
            print(f'Export folder: {self.export_folder}')
            if is_dir(self.export_folder):
                self.export_pdfs()
            else:
                status_message = f'Please select a valid folder!'
                messagebox.showerror(title='Error!', message=status_message)
                self.set_status(status_message)
        else:
            status_message = f'Please select a PDF file!'
            messagebox.showwarning(
                title='NO PDF SELECTED!', message=status_message
            )

    def export_pdfs(self, event=None):
        self.set_values()
        for pdf in self.pdf_inputs:
            status_message = f'Exporting "{pdf}" to "{self.export_folder}"'
            self.set_status(status_message)
            arguments = {
                'pdf_input': pdf,
                'string_find': self.strings_to_find,
                'string_replace': self.strings_to_replace,
                'folder': self.export_folder,
            }
            # t1 = Thread(target=text_remover, kwargs=arguments)
            # t1 = MyThread(t1)

            # t1.start()

            try:
                text_remover(
                    pdf_input=pdf,
                    string_find=self.strings_to_find,
                    string_replace=self.strings_to_replace,
                    folder=self.export_folder,
                )
                # t1.join()
                status_message = (
                    f'"{pdf}" exportation to "{self.export_folder}" complete!'
                )
                self.set_status(status_message)
                print(f'\n\nFile: "{pdf}" exported!')
            except Exception as e:
                title_error = 'Error in export!'
                message_error = (
                    f'Error in "{pdf}" export:\n{traceback.format_exc()}'
                )
                messagebox.showerror(title=title_error, message=message_error)
                self.set_status(message_error)
        status_message = f'Files exported.'
        self.set_status(status_message)
        messagebox.showinfo(title='Process completed', message=status_message)

    def remove_file(self, event=None):
        if self.pdf_list.selection():
            selected_items = self.pdf_list.selection()
            for item in selected_items:
                name = self.pdf_list.item(item)['values'][0]
                self.pdf_list.delete(item)
                self.pdf_inputs.remove(name)

    def remove_all_files(self):
        for line in self.pdf_list.get_children():
            name = self.pdf_list.item(line)['values'][0]
            self.pdf_list.delete(line)
            self.pdf_inputs.remove(name)

    def add_items(self, item, event=None):
        self.__inputs_open.append(item)
        self.set_replaces()

    def remove_items(self, item, event=None):
        if item in self.keys:
            self.__inputs_open.remove(item)
        self.set_replaces()

    def get_keys(self):
        # unique_keys = []
        item_base = 'item_'
        key = 1
        while len(self.__inputs_open) < self.__inputs:
            item_key = item_base + str(key)
            if item_key not in self.__inputs_open:
                self.add_items(item_key)
            key += 1

    @property
    def keys(self):
        self.get_keys()
        self.__inputs_open.sort()
        return self.__inputs_open


# Custom Exception Class
class MyException(Exception):
    pass


# Custom Thread Class
class MyThread(threading.Thread):

    # Function that raises the custom exception
    def someFunction(self):
        name = threading.current_thread().name
        raise MyException('An error in thread ' + name)

    def run(self):

        # Variable that stores the exception, if raised by someFunction
        self.exc = None
        try:
            self.someFunction()
        except BaseException as e:
            self.exc = e

    def join(self):
        threading.Thread.join(self)
        # Since join() returns in caller thread
        # we re-raise the caught exception
        # if any was caught
        if self.exc:
            raise self.exc
