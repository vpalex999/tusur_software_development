
from sources.shared.domain_model import DomainModel
from sources.domain.base_repr import BaseRepr
from sources.config.config import *


class NodeSubscriber(BaseRepr):

    def __init__(self, dn,
                 type_dn=OTHER,
                 password="",
                 interface=None,
                 access=None,
                 list_dn_options=[]):
        self.dn = dn                    # Номер телефона (строка)
        self.type_dn = type_dn          # Тип номера (SIP, PSTN, None)
        self.password = password        # Пароль регистрации, аутентификации, незашифрованный (строка)
        self.interface = interface      # Номер аналогово интерфейса
        self.access = access            # Порт доступа
        self.list_dn_options = list_dn_options  # список исходных атрибутов номера

    @classmethod
    def from_dict(cls, adict):
        def_subs = NodeSubscriber(
            dn=adict['dn'],
            type_dn=adict.get('type_dn', OTHER),
            password=adict.get('password', ''),
            interface=adict.get('interface'),
            access=adict.get('access'),
            list_dn_options=adict.get('list_dn_options', [])
        )

        return def_subs

    def __eq__(self, other):
        return self.dn == other.dn


DomainModel.register(NodeSubscriber)
