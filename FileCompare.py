#!/usr/bin/env python3

# Author - Shane Carnahan
# Email - Shane.Carnahan1@gmail.com
# Date - 8/28/18
# Project - Cisco_Config_Builder
# Version - 1.0

import difflib
import tkinter
import tkinter.filedialog as filedialog
from tkinter import messagebox
from tkinter import *
import os
from pathlib import Path
from threading import Thread
import time
from MyLogger import my_logger
import webbrowser

'''
This program simply compares two text files and logs the differences to a file.
'''


""" File Menu functions"""


def new():
    print("You've done something new!!")
    return


def edit():
    print('You edited something!!!')


def close():
    exit = messagebox.askyesno(title="Quit", message="Are You Sure You Want To Quite?")
    if exit > 0:
        main_window.destroy()
        sys.exit(0)
    return


""" Help Menu functions"""


def help_docs():
    # messagebox.showinfo(title="github", message="github link", command=webbrowser.open_new(r"https://github.com/scarnahan1"))
    webbrowser.open_new(r"https://github.com/scarnahan1/Cisco_Config_Builder")
    return


def about():
    messagebox.showinfo(title="About", message="""
    File compare utility created by Shane Carnahan (Shane.carnahan1@gmail.com).
    """)
    return


def file_entry(file_entry):
    """ This gets our seed file if we need one"""
    file = filedialog.askopenfilename()
    # print(seedfile)
    file_entry.insert(END, file)
    return file


def outpath(output_location_entry):
    # Clear the original location in the path box
    output_location_entry.delete(0, 'end')
    outpath = filedialog.askdirectory()
    # Write out new path to the entry box
    output_location_entry.insert(END, outpath)
    return outpath


def gui_thread(file1_entry, file2_entry, site_name_entry, output_location_entry, logger2, logger3):
    """ This calls a new thread for the work to begin and allows the GUI to respond again"""
    logger2.debug("Called GUI Function...")
    myThread = Thread(
        target=lambda: main_thread(file1_entry, file2_entry, site_name_entry, output_location_entry, logger3))
    myThread.start()


def main_thread(file1_entry, file2_entry, site_name_entry, output_location_entry, logger3):
    logger3.debug('Called Main_Thread...')
    start_time = time.time()
    file1 = file1_entry.get()
    file2 = file2_entry.get()
    output_location = output_location_entry.get()
    site_name = site_name_entry.get()
    output_file_location = output_location + '/' + site_name + '/'
    if not os.path.exists(output_location + '/' + site_name):
        try:
            os.makedirs(output_location + '/' + site_name)
        except Exception as err:
            logger3.exception('Something happened when creating the Site Folder: ').format(err)
            pass
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        diff = difflib.ndiff(f1.readlines(), f2.readlines())
        # Create and open the output log file
        diff_file = open(output_file_location + site_name + '_difflog.txt', 'w+')
        for line in diff:
            # - at start of line is unique to sequence 1
            if line.startswith('-'):
                sys.stdout.write('Missing in File1 {}'.format(line))
                diff_file.write('Missing in File1 {}'.format(line))

            # + at start of line is unique to sequence 2
            elif line.startswith('+'):
                sys.stdout.write('Missing in File2 {}'.format(line))
                diff_file.write('Missing in File2 {}'.format(line))
        diff_file.write('Analysis completed...')
        diff_file.close()
    logger3.info('--- {} seconds ---'.format(time.time() - start_time))


def main(log_location):
    # Set up our logging here
    log_file_name = log_location + 'FileCompare.log'
    # Set loggers for specific areas of the module
    logger1 = my_logger('FileCompare.main', log_file_name)
    logger2 = my_logger('FileCompare.gui_thread', log_file_name)
    logger3 = my_logger('FileCompare.main_thread', log_file_name)
    logger4 = my_logger('FileCompare.multiple_replace', log_file_name)

    """
        Get the path to the users Documents folder
        Assumes that this is a Windows 10 machine and the user has a Documents folder.
        """
    default_path = ""
    try:
        userprofile = os.environ.get('USERPROFILE')  # This should work for windows OS
        logger1.debug(userprofile)
        default_path = userprofile + "\\" + "Documents"
        logger1.debug(default_path)
    except:
        userprofile = str(Path.home())  # This should work for MAC and probably Linux
        default_path = userprofile + "/" + "Documents"
        logger1.debug(default_path)

    # GUI Things
    global main_window
    main_window = tkinter.Tk()
    main_window.title('File Compare')

    site_name_text = Label(main_window, text="Site Name/Code")
    site_name_text.grid(row=1, column=0, sticky=W)
    site_name_entry = Entry(main_window)
    site_name_entry.grid(row=1, column=1, sticky=W)
    site_name_entry.insert(END, 'BOP')
    file1_text = Label(main_window, text="select file1")
    file1_text.grid(row=2, column=0, sticky=W)
    file2_text = Label(main_window, text="select file2")
    file2_text.grid(row=3, column=0, sticky=W)

    file1_entry = Entry(main_window, width=30)  # width=30
    file1_entry.grid(row=2, column=1, sticky=W)
    open_file = Button(main_window, command=lambda: file_entry(file1_entry), padx=1, text="Select File1")
    open_file.grid(row=2, column=2, sticky=W)

    file2_entry = Entry(main_window, width=30)  # width=30
    file2_entry.grid(row=3, column=1, sticky=W)
    open_file = Button(main_window, command=lambda: file_entry(file2_entry), padx=1, text="Select File2")
    open_file.grid(row=3, column=2, sticky=W)

    output_location_text = Label(main_window, text="Select the output path")
    output_location_text.grid(row=4, column=0, sticky=W)

    output_location_entry = Entry(main_window, width=30)  # width=40 was used originally
    output_location_entry.grid(row=4, column=1, sticky=W)
    output_location_entry.insert(END, default_path)
    open_file = Button(main_window, command=lambda: outpath(output_location_entry), padx=1, text="Select Output Path")
    open_file.grid(row=4, column=2, sticky=W)

    # Let's Go!
    attempt = Button(text="OK",
                     command=lambda: gui_thread(file1_entry, file2_entry, site_name_entry, output_location_entry,
                                                logger2, logger3))
    attempt.grid(row=10, column=0, sticky=W)
    exit = Button(text="Close", command=close)
    exit.grid(row=10, column=1, sticky=W)

    """ Playing with Menu ideas. This may get ripped out in the end but wanted to give it a try for now. """
    # Menu Construction
    menubar = Menu(main_window)
    filemenu = Menu(menubar, tearoff=0)
    # filemenu.add_command(label="New", command=new)  # New would be a function similar to a button
    # filemenu.add_command(label="Open")
    # filemenu.add_command(label="Save As..")
    filemenu.add_command(label="Close", command=close)
    menubar.add_cascade(label="File", menu=filemenu)
    main_window.config(menu=menubar)

    # Edit Menu
    # editmenu = Menu(menubar, tearoff=0)
    # editmenu.add_command(label='Edit', command=edit)
    # menubar.add_cascade(label="Edit", menu=editmenu)

    # Help Menu
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help Docs", command=help_docs)
    helpmenu.add_command(label="About", command=about)
    menubar.add_cascade(label="Help", menu=helpmenu)

    # Main Starter required for Windows machines
    main_window.mainloop()


if __name__ == "__main__":
    log_location = './LOGS/'
    main(log_location)
