from sources.domain.defaultsubscriber import DefaultSubscriber as DSubs
from sources.domain.custom_service_set import CustomServiceSet


class MainInteractor(object):

    def __init__(self, defsubsrepo, nodesubsrepo, config):
        self.defsubsrepo = defsubsrepo
        self.nodesubsrepo = nodesubsrepo
        self.config = config

    def list_subscribers(self):
        """ Возвратить список всех номеров из репозитория """
        return self.defsubsrepo.list()

    def get_category(self, list_dn_options):
        """ Вычислить категорию АОН номера по шаблону конвертирования """
        return self.config.category(list_dn_options)

    def get_services(self, list_dn_options):
        """ Вычислить авторизованные услуги номера по шаблону конвертирования """
        return self.config.service(list_dn_options)

    def get_service_set(self, list_dn_options):
        """ Вычислить номер шаблона услуг на стороне VIMS по списку авторизованных услуг """
        return -1 # залгушка, требует доработки

    def get_license_ims(self):
        """ Получить тип илензии из глобального конфига VIMS """
        return getattr(self.config.ims, "LICENSE")
    
    def get_license(self):
        """ Вычисляет конечный тип лицензии на услуги для номера """
        return self.get_license_ims()  # заглушка

    def get_custom_service_set(self, list_services, **kwargs):
        """ Получить объект, хранящий Castom service set """
        return CustomServiceSet().make(list_services, **kwargs)

    def make_subscribers(self):
        """ Применение правил к созданию Базового номера """
        for node_dn in self.nodesubsrepo.list():
            def_subs_dn = dict()
            print("##### Start of subscriber configuration {} #####".format(node_dn.dn))
            def_subs_dn['dn'] = node_dn.dn
            def_subs_dn['license'] = self.get_license()
            def_subs_dn['category'] = self.get_category(node_dn.list_dn_options)
            def_subs_dn['services'] = self.get_services(node_dn.list_dn_options)
            def_subs_dn['service_set'] = self.get_service_set(node_dn.list_dn_options)
            def_subs_dn['custom_service_set'] = self.get_custom_service_set(def_subs_dn['services'],
                                                                            category=def_subs_dn['category'])
            
            print("##### Stop of subscriber configuration {} #####".format(node_dn.dn))

            self.defsubsrepo.add(DSubs.from_dict(def_subs_dn))

    def execute(self):
        return self.list_subscribers()
