from sources.domain.defaultsubscriber import DefaultSubscriber as DSubs


class MainInteractor(object):

    def __init__(self, defsubsrepo, nodesubsrepo):
        self.defsubsrepo = defsubsrepo
        self.nodesubsrepo = nodesubsrepo

    def list_subscribers(self):
        """ Возвратить список всех номеров из репозитория """
        return self.defsubsrepo.list()

    def make_subscribers(self):
        """ Применение правил к созданию Базового номера """
        for node_dn in self.nodesubsrepo.list():
            def_subs_dn = dict()
            def_subs_dn['dn'] = node_dn.dn

            self.defsubsrepo.add(DSubs.from_dict(def_subs_dn))

    def execute(self):
        return self.list_subscribers()
