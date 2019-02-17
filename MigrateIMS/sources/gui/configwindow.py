""" Формирование главного графического окна """

from tkinter import *
from sources.gui.makeform import *
from sources.config.config import *
import logging


def config_from_gui(gui_config={}):
    win = Toplevel(width=40,
                   height=10,
                   relief=SUNKEN)


    win.title('Config MigrateIMS')

    Button(win, text='OK', command=win.destroy).pack(side=BOTTOM)

    node = optionMenu(win, NODE, label='Тип АТС', ext_var=gui_config.get("node", ''))
    type_dn = optionMenu(win, ALL_TYPE_DN, label='Тип Номера', ext_var=gui_config.get("type_dn", ''))

    dest_dir = formOpenDir(win, label='Папка выгрузки', ext_var=gui_config.get("dest_dir", ''))
    sourse_file_db = formOpenFile(win,    label='База Данных АТС', ext_var=gui_config.get("sourse_file_db", ''))
    mapping_category = formOpenFile(win, label='Шаблон Категорий АОН', ext_var=gui_config.get("mapping_category", ''))
    mapping_service = formOpenFile(win,  label='Шаблон Услуг        ', ext_var=gui_config.get("mapping_service", ''))
    mapping_ims = formOpenFile(win,   label='Шаблон IMS          ', ext_var=gui_config.get("mapping_ims", ''))

    win.grab_set()
    win.focus_set()
    win.wait_window()
    return {
        "node": node.get(),
        "type_dn": type_dn.get(),
        "dest_dir": dest_dir.get(),
        "sourse_file_db": sourse_file_db.get(),
        "mapping_category": mapping_category.get(),
        "mapping_service": mapping_service.get(),
        "mapping_ims": mapping_ims.get()
    }


def config_window(gui_config):
    """ Модадьное окно настройки конфигурации """
    gui_config.update(config_from_gui(gui_config))
    logging.debug("Get Config: " + str(gui_config))
