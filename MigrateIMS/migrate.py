# -*- coding: utf-8 -*-

import os
import json
import logging
from sources.logging.log_configure import setup_logging

from sources.config.config import Config
from sources.shared.main_interactor import MainInteractor
from sources.repository.imsrepository import ImsSubsRepo
from sources.repository.mockrepository import MockRepo
from sources.domain.wp import WpDN
from sources.domain.view_wp import ViewWP


setup_logging()

logging.info("****************** Start MigrateIMS **************************\n")

category_j = json.load(open('data/node_test/config/category_set_fake_atc.json'))
service_j = json.load(open('data/node_test/config/service_set_fake_atc.json'))
ims_j = json.load(open('data/node_test/config/config_fake_ims.json'))
source_db = "data/node_test/data/ATC_MAKET.xlsx"


config = Config(node='AXE-10',
                sf_db=source_db,
                mapping_category=category_j,
                mapping_service=service_j,
                mapping_ims=ims_j,
                dest_dir='data/node_test'
                ).execute()

node_repo = MockRepo(config).execute()
main_repo = ImsSubsRepo()

main_handler = MainInteractor(main_repo, node_repo, config)
main_handler.execute()

wp_list = [WpDN(dn, config)() for dn in main_repo.list(filters={'type_dn': "SIP"})]
wiev = ViewWP(wp_list)

open(os.path.join(config.dest_dir, 'web_portal.txt'), 'w').writelines(wiev())
