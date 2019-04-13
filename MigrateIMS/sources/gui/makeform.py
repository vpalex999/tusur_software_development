"""
создает фрейм-ряд с меткой и полем ввода и дополнительной кнопкой, вызывающей
диалог выбора файла
"""

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory


def formOpenFile(parent, label, width=25, browse=True, ext_var=''):
    """
    создает фрейм-ряд с меткой и полем ввода и дополнительной кнопкой,
    вызывающей диалог выбора файла
    """
    var = StringVar()
    var.set(ext_var)
    row = Frame(parent)
    lab = Label(row, text=label, relief=FLAT, width=width)
    ent = Entry(row, relief=SUNKEN, textvariable=var)
    row.pack(fill=X)
    lab.pack(side=LEFT)
    ent.pack(side=LEFT, expand=YES, fill=X)
    if browse:
        btn = Button(row, text='browse...')
        btn.pack(side=RIGHT)
        btn.config(command=lambda: var.set(askopenfilename() or var.get()))
    return var


def formOpenDir(parent, label, width=25, browse=True, ext_var=''):
    """
    создает фрейм-ряд с меткой и полем ввода и дополнительной кнопкой,
    вызывающей диалог выбора Директории
    """
    var = StringVar()
    var.set(ext_var)
    row = Frame(parent)
    lab = Label(row, text=label, relief=FLAT, width=width)
    ent = Entry(row, relief=RIDGE, textvariable=var)
    row.pack(fill=X)
    lab.pack(side=LEFT)
    ent.pack(side=LEFT, expand=YES, fill=X)
    if browse:
        btn = Button(row, text='browse...')
        btn.pack(side=RIGHT)
        btn.config(command=lambda: var.set(askdirectory() or var.get()))
    return var


def optionMenu(parent, list_options, label='', ext_var="", side=TOP, width=15):
    row = Frame(parent)
    var = StringVar()
    var.set(ext_var)
    lab = Label(row, text=label, relief=FLAT, width=width)
    opt = OptionMenu(row, var, *list_options)
    row.pack(side=side, anchor=NW)
    lab.pack(side=LEFT)
    opt.pack(side=LEFT)
    return var
