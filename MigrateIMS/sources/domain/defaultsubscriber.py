
from sources.shared.domain_model import DomainModel


class DefaultSubscriber(object):

    def __init__(self, dn, category):
        self.dn = dn                    # Номер телефона (строка)
        self.category = category        # Категория АОН (строка)
        self.services = None            # Авторизованные Услуги номера
        self.service_set = None         # Номер Servise Set (строка)
        self.custom_service_set = None  # Нобор услуг в Кастомном варианте
        self.active_services = None     # Активные услуги номера
        self.suspend = None             # Статус отключения

    @classmethod
    def from_dict(cls, adict):
        def_subs = DefaultSubscriber(
            dn=adict['dn'],
            category=adict['category']
        )

        return def_subs


DomainModel.register(DefaultSubscriber)
