import json

from sources.config.config import Config
from sources.shared.main_interactor import MainInteractor
from sources.repository.imsrepository import ImsSubsRepo
from sources.repository.mockrepository import MockRepo
from sources.domain.wp import WpDN
from sources.domain.view_wp import ViewWP


category_j = json.load(open('templates/template_category_set_mt20.json'))
service_j = json.load(open('templates/template_set_mt20.json'))
ims_j = json.load(open('templates/template_ims.json'))


config = Config(node='AXE-10',
                mapping_category=category_j,
                mapping_service=service_j,
                mapping_ims=ims_j
                ).execute()

node_repo = MockRepo(config).execute()
main_repo = ImsSubsRepo()

main_handler = MainInteractor(main_repo, node_repo, config)
main_handler.execute()

wp_list = [WpDN(dn, config)() for dn in main_repo.list(filters={'type_dn': "SIP"})]
wiev = ViewWP(wp_list)

open('web_portal.txt', 'w').writelines(wiev())

