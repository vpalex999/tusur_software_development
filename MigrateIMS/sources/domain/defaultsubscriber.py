
from sources.shared.domain_model import DomainModel
from sources.domain.base_repr import BaseRepr


class DefaultSubscriber(BaseRepr):

    def __init__(self, dn,
                 type_dn=None,
                 password="",
                 category=None,
                 license=None,
                 services=None,
                 service_set='-1',
                 custom_service_set=None,
                 active_services=None,
                 interface=None,
                 access=None):
        self.dn = dn                    # Номер телефона (строка)
        self.type_dn = type_dn          # Тип номера (SIP, PSTN, None)
        self.password = password        # Пароль регистрации, аутентификации, незашифрованный (строка) 
        self.category = category        # Категория АОН (строка)
        self.license = license          # тип лицензии на услуги (строка)
        self.services = services        # Авторизованные Услуги номера
        self.service_set = service_set  # Номер Servise Set (строка)
        self.custom_service_set = custom_service_set  # Набор услуг в Кастомном варианте - None или объект кастомных услуг
        self.active_services = active_services        # Активные услуги номера. None или [] с активными услугами
        self.interface = interface      # Номер аналогово интерфейса
        self.access = access            # Порт доступа

    @classmethod
    def from_dict(cls, adict):
        def_subs = DefaultSubscriber(
            dn=adict['dn'],
            type_dn=adict.get('type_dn'),
            password=adict.get('password', ''),
            category=adict.get('category'),
            services=adict.get('services'),
            service_set=adict.get('service_set', '-1'),
            license=adict.get('license', ''),
            custom_service_set=adict.get('custom_service_set'),
            active_services=adict.get('active_services'),
            interface=adict.get('interface'),
            access=adict.get('access'),
        )

        return def_subs

    def __eq__(self, other):
        return self.dn == other.dn


DomainModel.register(DefaultSubscriber)
