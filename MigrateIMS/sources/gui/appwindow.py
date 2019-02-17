""" Формирование главного графического окна """
import sys
import logging
import _thread
from tkinter import *
from sources.gui.guimaker import GuiMaker
from sources.gui.configwindow import config_window


class AppWindow(GuiMaker):
    """ Главное окно приложения """
    def __init__(self, funct_run_migrate, root=None, ):
        logging.info("***** Start GUI Application *****")
        self.funct_run_migrate = funct_run_migrate
        self.gui_config = {}
        self.tool_bar = [
                         ('Run', (lambda: self.makethreads()), {'side': LEFT}),
                         ('Config', (lambda: config_window(self.gui_config)), {'side': LEFT}),
                         ('Quit', sys.exit, {'side': RIGHT})
                        ]
        root.title('MigrateIMS')
        GuiMaker.__init__(self, root)

    def start(self):
        self.toolBar = self.tool_bar

    def makethreads(self):
        logging.debug('makethreads for run converting MigrateIMS')
        _thread.start_new_thread(self.funct_run_migrate, (self.gui_config,))
