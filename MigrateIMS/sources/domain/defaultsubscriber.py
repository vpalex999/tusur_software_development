
from sources.shared.domain_model import DomainModel


class DefaultSubscriber(object):

    def __init__(self, dn, category,
                 services=None,
                 service_set='-1',
                 custom_service_set=None,
                 active_services=None):
        self.dn = dn                    # Номер телефона (строка)
        self.category = category        # Категория АОН (строка)
        self.services = services        # Авторизованные Услуги номера
        self.service_set = service_set  # Номер Servise Set (строка)
        self.custom_service_set = custom_service_set  # Нобор услуг в Кастомном варианте - None или объект кастовных услуг
        self.active_services = active_services        # Активные услуги номера. None или [] с активными услугами

    @classmethod
    def from_dict(cls, adict):
        def_subs = DefaultSubscriber(
            dn=adict['dn'],
            category=adict['category'],
            services=adict.get('services'),
            service_set=adict.get('service_set', '-1'),
            custom_service_set=adict.get('custom_service_set'),
            active_services=adict.get('active_services')
        )

        return def_subs


DomainModel.register(DefaultSubscriber)
