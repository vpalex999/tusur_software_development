# -*- coding: utf-8 -*-
"""
Класс для работы с типами абонентских лицензий
"""

import logging

from sources.error import MigrateElementError
from sources.utilites.file import read_json

log_lic_type = logging.getLogger("migrate.lic_type")


class LicenseType(object):

    _set_lic = read_json('templates/template_license_type.json')

    _default_set_key = ['basicLicense',
                        'standardLicense',
                        'advancedLicense'
                        ]

    @staticmethod
    def get_id(name_lic):
        _default_lic_id = {
            'basicLicense': '21',
            'standardLicense': '20',
            'advancedLicense': '22'
        }
        try:
            return _default_lic_id[name_lic]
        except Exception as e:
            raise MigrateElementError(f"Wrong name subscriber Licence: {e}")

    def __init__(self, template_lic=None, number_dn=''):
        if template_lic is None:
            self._template_lic = self._set_lic
        else:
            self._template_lic = template_lic
        self._number_dn = number_dn

    @classmethod
    def get(cls, number_set_dvo, number_dn):
        _lic = cls(number_dn=number_dn)
        return _lic.get_lic(number_set_dvo)

    @property
    def check(self):
        if not sorted(self._default_set_key) ==\
                        sorted(list(self._template_lic.keys())):
            raise MigrateElementError(f"Error in the name licence: "
                                      f"{self._template_lic}")
        if "" in [''.join(i) for i in self._template_lic.values()]:
            raise MigrateElementError(f"Empty data in licences type: "
                                      f"{self._template_lic}")
        return True

    def get_lic(self, subsciber_set):
        if self.check:
            if not isinstance(subsciber_set, list):
                raise MigrateElementError(f"Received set dvo from subscriber"
                                          f" is wrong: {subsciber_set}")
            if len(subsciber_set) == 0:
                return self.name_basic

            for name_lic, lic_set in self._template_lic.items():
                for suppl_subscriber in subsciber_set:
                    if suppl_subscriber not in lic_set:
                        break
                else:
                    return name_lic
            else:
                log_lic_type.warning(f"DN {self._number_dn}: has a set of "
                                     f"services {subsciber_set} which are not "
                                     f"included in any of the sets of template"
                                     f" License Type \nso, will be assigned "
                                     f"default License Type:{self.name_basic}")
                return self.name_basic

    @property
    def name_basic(self):
        return 'basicLicense'

    @property
    def name_standart(self):
        return 'standardLicense'

    @property
    def name_advanced(self):
        return 'advancedLicense'
