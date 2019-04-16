""" Формирование главного графического окна """
import os
from tkinter import *
from tkinter import Toplevel
from tkinter.messagebox import showerror
from sources.gui.makeform import optionMenu, formOpenDir, formOpenFile
from sources.config.config import *
import logging


class ConfigWindow(Toplevel):

    def __init__(self, gui_config={}):
        Toplevel.__init__(self, width=40, height=10, relief=SUNKEN)
        self.title('Config MigrateIMS')

        self.button_ok = Button(self, text='OK', command=self.close_config_window)
        self.button_ok.pack(side=BOTTOM)

        self.node = optionMenu(self, NODE, label='Тип АТС',
                               ext_var=gui_config.get("node", ''))
        self.type_dn = optionMenu(
            self, ALL_TYPE_DN, label='Тип Номера', ext_var=gui_config.get("type_dn", ''))
        self.dest_dir = formOpenDir(
            self, label='Папка выгрузки', ext_var=gui_config.get("dest_dir", ''))
        self.sourse_file_db = formOpenFile(
            self,   label='База Данных АТС', ext_var=gui_config.get("sourse_file_db", ''))
        self.mapping_category = formOpenFile(
            self, label='Шаблон Категорий АОН', ext_var=gui_config.get("mapping_category", ''))
        self.mapping_service = formOpenFile(
            self,  label='Шаблон Услуг        ', ext_var=gui_config.get("mapping_service", ''))
        self.mapping_ims = formOpenFile(
            self,      label='Шаблон IMS          ', ext_var=gui_config.get("mapping_ims", ''))

    def check_fields(self):
        """ проверка полей ввода"""
        if not self.check_range_fields("Папка выгрузки", self.dest_dir.get()):
            return
        if not os.path.isdir(self.dest_dir.get()):
            showerror("Config: Папка выгрузки", "Указана несуществующая директория:\n{}".format(self.dest_dir.get()))
            return
        if not self.check_range_fields("База Данных АТС", self.sourse_file_db.get()):
            return
        if not self.check_is_file("База Данных АТС", self.sourse_file_db.get()):
            return
        if not self.check_range_fields("Шаблон Категорий АОН", self.mapping_category.get()):
            return
        if not self.check_is_file("Шаблон Категорий АОН", self.mapping_category.get()):
            return
        if not self.check_range_fields("Шаблон Услуг", self.mapping_service.get()):
            return
        if not self.check_is_file("Шаблон Услуг", self.mapping_service.get()):
            return
        if not self.check_range_fields("Шаблон IMS", self.mapping_ims.get()):
            return
        if not self.check_is_file("Шаблон IMS", self.mapping_ims.get()):
            return
        return True

    def close_config_window(self):
        """ Закрыть окно конфигурирования с проверкой полей ввода """
        if self.check_fields():
            self.destroy()

    def check_range_fields(self, field_name, field_text):
        """ Проверка на границы длинны поля """
        if len(field_text) < 1 or len(field_text) > 250:
            showerror("Config: {}".format(field_name), "длинна поля должна быть в диапазоне от 1 до 250: {}".format(len(field_text)))
            return False
        return True

    def check_is_file(self, field_name, field_text):
        """ Проверка на суествование файла """
        if not os.path.isfile(field_text):
            showerror("Config: {}".format(field_name), "Указан несуществующий файл:\n{}".format(field_text))
            return False
        return True

    def __call__(self):
        self.grab_set()
        self.focus_set()
        self.wait_window()

        return {
            "node": self.node.get(),
            "type_dn": self.type_dn.get(),
            "dest_dir": self.dest_dir.get(),
            "sourse_file_db": self.sourse_file_db.get(),
            "mapping_category": self.mapping_category.get(),
            "mapping_service": self.mapping_service.get(),
            "mapping_ims": self.mapping_ims.get()
        }


def config_window(gui_config):
    """ Модальное окно настройки конфигурации """
    gui_config.update(ConfigWindow(gui_config)())
    logging.debug("Get Config: " + str(gui_config))
