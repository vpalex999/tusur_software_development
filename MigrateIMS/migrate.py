# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
from sources.logging.log_configure import setup_logging

from sources.config import *
from sources.config.config import Config
from sources.shared.main_interactor import MainInteractor
from sources.repository.baserepository import BaseRepo
from sources.repository.imsrepository import ImsSubsRepo
from sources.repository.mockrepository import MockRepo
from sources.domain.wp import WpDN
from sources.domain.view_wp import ViewWP
from sources.domain.errors import MigrateError
from sources.gui.appwindow import AppWindow
from tkinter import *


setup_logging()


def run_migrate(gui_config):

    logging.info("****************** Start converting MigrateIMS **************************\n")

    config = Config.from_dict(gui_config).execute()

    if gui_config["node"] == 'DEMO':
        node_repo = MockRepo(config).execute()
    else:
        node_repo = BaseRepo()
    main_repo = ImsSubsRepo()

    MainInteractor(main_repo, node_repo, config).execute()

    wp_list = [WpDN(dn, config)() for dn in main_repo.list(filters={'type_dn': "SIP"})]
    wiev = ViewWP(wp_list)

    try:
        file_name_wp = os.path.join(config.dest_dir, 'web_portal.txt')
        open(os.path.join(config.dest_dir, file_name_wp), 'w').writelines(wiev())
        logging.info("Successful writing file: {}".format(file_name_wp))
    except Exception as e:
        logging.error('Failed to write file', exc_info=True)
        raise MigrateError(e)

    logging.info("****************** End converting MigrateIMS **************************\n")


def main_win():
    root = Tk()
    win = AppWindow(run_migrate, root)
    root.mainloop()


if __name__ == '__main__':
    main_win()
