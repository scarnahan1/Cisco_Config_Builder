# Author - Shane Carnahan
# Email  - Shane.Carnahan1@gmail.com
# Date - 8/29/2018
# Project - TXT2EXCEL
# Module Version - 1.0


import glob, csv, xlwt, os, tkinter
from tkinter import *
from tkinter import messagebox
import tkinter.filedialog as filedialog
from pathlib import Path
from threading import Thread
from MyLogger import my_logger
import webbrowser
import time

'''
This utility will search the folder given as input for .txt files and will add them to tabs in an excel file.
The tabs will be named with the file name found. 
'''

wb = xlwt.Workbook()


def help_docs():
    webbrowser.open_new(r"https://github.com/scarnahan1/Cisco_Config_Builder")
    return


def about():
    messagebox.showinfo(title="About", message="""
    File compare utility created by Shane Carnahan (Shane.carnahan1@gmail.com).
    """)
    return


def close():
    exit = messagebox.askyesno(title="Quit", message="Are You Sure You Want To Be a Quitter?")
    if exit > 0:
        main_window.destroy()
        sys.exit(0)
    return


def path(location_entry, default_path):
    # Clear the original location in the path box
    location_entry.delete(0, 'end')
    path = filedialog.askdirectory(initialdir=default_path)
    # Write out new path to the entry box
    location_entry.insert(END, path)
    return path


def gui_thread(site_name_entry, input_location_entry, output_location_entry, logger2, logger3):
    """ This calls a new thread for the work to begin and allows the GUI to respond again"""
    logger2.debug("Called GUI Function...")
    myThread = Thread(target=lambda: main_thread(site_name_entry, input_location_entry, output_location_entry, logger2, logger3))
    myThread.start()


def main_thread(site_name_entry, input_location_entry, output_location_entry, logger2, logger3):
    start_time = time.time()
    pattern = "/*.txt"
    in_location = input_location_entry.get()
    out_location = output_location_entry.get() + '/'
    g_location = in_location + pattern
    for filename in glob.glob(g_location):
        (f_path, f_name) = os.path.split(filename)
        (f_short_name, f_extension) = os.path.splitext(f_name)
        ws = wb.add_sheet(f_short_name)
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                ws.write(i, 0, line)
    outfile_append = "_Configs.xls"
    outfile = out_location + site_name_entry.get() + outfile_append
    logger3.debug('Saving file {}...'. format(outfile))
    wb.save(outfile)
    logger3.info('--- {} seconds ---'.format(time.time() - start_time))
    logger3.info('Run Completed...')


def main(log_location):
    # Set up our logging here
    log_file_name = log_location + 'TXT2Excel.log'
    # Set loggers for specific areas of the module
    logger1 = my_logger('TXT2Excel.main', log_file_name)
    logger2 = my_logger('TXT2Excel.gui_thread', log_file_name)
    logger3 = my_logger('TXT2Excel.main_thread', log_file_name)
    logger4 = my_logger('TXT2Excel.multiple_replace', log_file_name)
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
    main_window.title('TXT2Excel')

    site_name_text = Label(main_window, text="Site Name/Code")
    site_name_text.grid(row=1, column=0, sticky=W)
    site_name_entry = Entry(main_window)
    site_name_entry.grid(row=1, column=1, sticky=W)
    site_name_entry.insert(END, 'BOP')

    input_location_text = Label(main_window, text="Select the input path")
    input_location_text.grid(row=3, column=0, sticky=W)
    input_location_entry = Entry(main_window, width=30)
    input_location_entry.grid(row=3, column=1, sticky=W)
    input_location_entry.insert(END, default_path)
    open_file = Button(main_window, command=lambda: path(input_location_entry, default_path), padx=1, text="Select input Path")
    open_file.grid(row=3, column=2, sticky=W)

    output_location_text = Label(main_window, text="Select the output path")
    output_location_text.grid(row=4, column=0, sticky=W)
    output_location_entry = Entry(main_window, width=30)
    output_location_entry.grid(row=4, column=1, sticky=W)
    output_location_entry.insert(END, default_path)
    open_file = Button(main_window, command=lambda: path(output_location_entry, default_path), padx=1, text="Select Output Path")
    open_file.grid(row=4, column=2, sticky=W)

    # Let's Go!
    attempt = Button(text="OK", command=lambda: gui_thread(site_name_entry, input_location_entry, output_location_entry, logger2, logger3))
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
