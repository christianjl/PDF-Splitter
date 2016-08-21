#! python3

import tkinter
from tkinter import ttk
import os
import PyPDF2
import re


def output_message(message):
    """Opens new window with message"""

    input_window = tkinter.Toplevel(root)
    input_window.title('Message')

    secondframe = ttk.Frame(input_window, padding="15 15 30 30")
    secondframe.grid(column=0, row=0, sticky=('N', 'W', 'E', 'S'))
    secondframe.columnconfigure(0, weight=1)
    secondframe.rowconfigure(0, weight=1)

    error_label = ttk.Label(secondframe, text=message)
    error_label.grid(column=0, row=0)


def create_page_range(user_input):
    """SCreates A List Of Included Pages From User Input"""

    user_input = user_input.replace(',', ';')
    user_input = user_input.split(';')

    page_ranges = []

    for entry in user_input:
        page_ranges.append(entry.replace(' ', ''))

    regex = re.compile(r'(\d*)-?(\d*)')

    complete_pages = []

    for entry in page_ranges:
        page_numbers = regex.search(entry)

        try:
            if page_numbers.group(2) == '':     # If True: single page given
                complete_pages.append(int(page_numbers.group(1)))
            else:
                # Create a range of the two page numbers given
                for i in range(int(page_numbers.group(1)), int(page_numbers.group(2)) + 1):
                    complete_pages.append(i)

        except ValueError:
            output_message('Value Error')
            return None

    for page in range(len(complete_pages)):
        try:
            if complete_pages[page] > complete_pages[page + 1]:
                output_message('Page Range Not Sequential.')
                return None
        except IndexError:
            continue

        if not isinstance(complete_pages[page], int):
            output_message('Non-numerical in Page Range.')
            return None

    return complete_pages


def split_custom(file_location):
    """Create New PDF From User Selected Pages"""

    list_of_pages = create_page_range(page_index_entry.get())

    if list_of_pages is None:
        return

    pdf_file_in = open(file_location, 'rb')
    pdf_reader_in = PyPDF2.PdfFileReader(pdf_file_in)

    pdf_writer = PyPDF2.PdfFileWriter()

    for page in list_of_pages:

        try:
            page_object = pdf_reader_in.getPage(page-1)  # (page-1): Account for index starting at 0
            pdf_writer.addPage(page_object)
        except IndexError:
            output_message('Index Error. Requested Pages Not In Document Range.')
            return

    file_path_list = file_location.split('\\')
    file_path = '\\'.join(file_path_list[:-1]) + '\\'

    os.chdir(file_path)

    if file_out_name_entry.get() == '':
        file_out_name = file_path_list[-1][:-4]
        file_out_name += ' (Edited).pdf'
    else:
        file_out_name = file_out_name_entry.get() + '.pdf'

    if os.path.isfile(file_out_name):
        edit_nr = 1
        base_name = file_out_name[:-4]

        while os.path.isfile(file_out_name):
            file_out_name = '{0} ({1}).pdf'.format(base_name, str(edit_nr))
            edit_nr += 1

    pdf_file_out = open(file_out_name, 'wb')
    pdf_writer.write(pdf_file_out)

    pdf_file_out.close()
    pdf_file_in.close()

    output_message('Success!\n New file saved with original.')

    return


def split_single(file_location):
    """Split PDF pages into single documents"""

    file_path_list = file_location.split('\\')
    file_path = '\\'.join(file_path_list[:-1]) + '\\'
    folder_name = file_path_list[-1][:-4] + ' Split Files'

    os.chdir(file_path)

    if os.path.exists(folder_name):
        edit_nr = 1
        folder_base_name = folder_name

        while os.path.exists(folder_name):
            folder_name = '{0} ({1})'.format(folder_base_name, str(edit_nr))
            edit_nr += 1

    os.makedirs(file_path + folder_name)

    os.chdir(file_path + folder_name)

    pdf_file_in = open(file_location, 'rb')
    pdf_reader_in = PyPDF2.PdfFileReader(pdf_file_in)

    for page_num in range(pdf_reader_in.numPages):
        pdf_writer = PyPDF2.PdfFileWriter()
        page_object = pdf_reader_in.getPage(page_num)
        pdf_writer.addPage(page_object)

        pdf_file_out = open('Page ' + str(page_num) + '.pdf', 'wb')
        pdf_writer.write(pdf_file_out)
        pdf_file_out.close()

    pdf_file_in.close()
    return


def validate_new_file_name(name):
    invalid_symbols = ['/', '\\', ':', '*', '\"', '<', '>']

    for symbol in invalid_symbols:
        if symbol in name:
            return False

    return True


def split_command():
    """Function Executed When Split Button Is Pressed"""
    file_location = file_location_entry.get()
    if file_location[-4:] != '.pdf':
        file_location += '.pdf'

    if not os.path.isfile(file_location):
        output_message('File Does Not Exist.')
        return

    if not validate_new_file_name(file_out_name_entry.get()):
        output_message('Invalid Output File Name.')
        return

    if split_method_selection.get() not in [1, 2]:
        return
    elif split_method_selection.get() == 1:
        split_single(file_location)
    else:
        split_custom(file_location)

    return


#  - - - - - GUI - - - -  -

root = tkinter.Tk()
root.title('PDF Splitter')

mainframe = ttk.Frame(root, padding="15 15 30 30")
mainframe.grid(column=0, row=0, sticky=('N', 'W', 'E', 'S'))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

split_method_selection = tkinter.IntVar()


# Widgets
file_input_label = ttk.Label(mainframe, text='File location: ')
file_location_entry = ttk.Entry(mainframe, width=55)
file_location_entry.insert(0, 'C:\\Users\\User\\example.pdf')

split_button = ttk.Button(mainframe, text='Split', command=split_command)

split_options_label = ttk.Label(mainframe, text='Options')
option1 = ttk.Radiobutton(mainframe, text='Split Into Individual Files', variable=split_method_selection, value=1)
option2 = ttk.Radiobutton(mainframe, text='New File From Pages: (e.g.:  1-2; 4-7,9 )',
                          variable=split_method_selection, value=2)

page_index_entry = ttk.Entry(mainframe, width=16)

file_out_name_label = ttk.Label(mainframe, text='New File Name:  (Optional)')
file_out_name_entry = ttk.Entry(mainframe, width=16)


# Pack widgets to grid
file_input_label.grid(column=0, row=0, padx=14)
file_location_entry.grid(column=1, row=0)
split_options_label.grid(column=0, row=1)
option1.grid(column=1, row=2, sticky='W')
option2.grid(column=1, row=3, sticky='W')
page_index_entry.grid(column=1, row=3, sticky='E', pady=2)

file_out_name_label.grid(column=1, row=4, sticky='W', pady=10)
file_out_name_entry.grid(column=1, row=4, sticky='E', pady=10)

split_button.grid(column=1, row=5, pady=10)


root.mainloop()
