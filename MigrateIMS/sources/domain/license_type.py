# -*- coding: utf-8 -*-
"""
Класс для работы с типами абонентских лицензий
"""

import json
import logging

from sources.domain.errors import MigrateError


class LicenseType(object):

    _set_lic = json.load(open('templates/template_license_type.json'))

    default_lic_id = {
        'basicLicense': '21',
        'standardLicense': '20',
        'advancedLicense': '22'
    }

    weight_lic = {
        "21": 1,
        "20": 2,
        "22": 3
    }

    @staticmethod
    def get_id_by_name(name_lic):
        """ Возвращает id лицензии по её названию """
        try:
            return LicenseType.default_lic_id[name_lic]
        except KeyError as e:
            raise MigrateError(f"Wrong name LicenceType: {e}")

    def __init__(self, template_lic=None):
        if template_lic is None:
            self._template_lic = self._set_lic
        else:
            self._template_lic = template_lic

    @property
    def check(self):
        """ Проверка шаблона лицензий """
        if sorted(list(self.default_lic_id)) != sorted(list(self._template_lic.keys())):
            raise MigrateError(f"Error in the name licence: "
                               f"{self._template_lic}")
        if "" in [''.join(i) for i in self._template_lic.values()]:
            raise MigrateError(f"Empty data in licences type: "
                               f"{self._template_lic}")
        return True

    def get_lic(self, subsciber_set):
        """
        Вычислить тип лицензии на основании списка услуг номера

        Аргументы
        ----------
        subsciber_set(list) - список услуг в формате ["CFU", "CW"]

        Выход
        ------
        - имя лицензии
        """
        if self.check:
            if not isinstance(subsciber_set, list):
                raise MigrateError(f"Received set dvo from subscriber"
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
                raise MigrateError(f"DN: has a set of "
                                   f"services {subsciber_set} which are not "
                                   f"included in any of the sets of template"
                                   f" License Type")

    def get_id_lic_by_set(self, subsciber_set):
        """ получить id вычисленной лицензии на основании набора услуг"""
        return self.get_id_by_name(self.get_lic(subsciber_set))

    def is_cover_lic(self, lic_type, subsciber_set):
        """ Покрытие лицензией набора услуг """

        w_subs_lic = self.weight_lic[self.get_id_lic_by_set(subsciber_set)]
        w_test_lis = self.weight_lic[self.get_id_by_name(lic_type)]

        return w_test_lis >= w_subs_lic

    @property
    def name_basic(self):
        return 'basicLicense'

    @property
    def name_standart(self):
        return 'standardLicense'

    @property
    def name_advanced(self):
        return 'advancedLicense'
