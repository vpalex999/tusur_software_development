import logging
from sources.repository.noderepository import NodeRepo
from sources.domain.nodesubscriber import NodeSubscriber

log_def_subs_repo = logging.getLogger("migrate.defsubsrepo")


class MockRepo(NodeRepo):
    """ Xранилище номеров Макета АТС для типа SIP """
    def __init__(self, config):
        super().__init__(config)

        self.parce_rows = [
                {
                 'Номер': "6873639",
                 'Услуги': ['CFU', "CW", 'AON1']
                }
        ]

    def execute(self):
        dn = dict()
        for row in self.parce_rows:
            dn['dn'] = row['Номер']
            dn['type_dn'] = self.config.SIP
            dn['password'] = ''
            dn['list_dn_options'] = row['Услуги']
        self.add(NodeSubscriber.from_dict(dn))

        return self
