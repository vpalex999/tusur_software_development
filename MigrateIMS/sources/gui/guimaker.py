""" Формирование главного графического окна """

import sys
from tkinter import *
from sources.logging.logging_gui import ConsoleUi


class GuiMaker(Frame):
    menuBar = []        # значения по умолчанию
    toolBar = []        # изменять при создании подклассов

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)  # растягиваемый фрейм
        self.start()        # в подклассе: установить меню/панель инстр.
        self.makeToolBar()  # здесь: создать панель инструментов
        self.makeWidgets()  # в подклассе: добавить середину

    def makeToolBar(self):
        """
        создает панель с кнопками внизу, если необходимо
        expand=no, fill=x, чтобы ширина оставалась постоянной
        """
        if self.toolBar:
            toolbar = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
            toolbar.pack(side=BOTTOM, fill=X)

            for (name, action, where) in self.toolBar:
                Button(toolbar, text=name, command=action).pack(where)

    def makeWidgets(self):
        """
        'средняя' часть создается последней
        """
        name = LabelFrame(self,
                          width=79,
                          height=10,
                          relief=SUNKEN,
                          bg='white',
                          text='Log')
        ConsoleUi(name)
        name.pack(expand=YES, fill=BOTH, side=TOP)

    def start(self):
        """ переопределите в подклассе: связать меню/панель инструментов с self """
        pass
