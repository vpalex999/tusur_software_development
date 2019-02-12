# -*- coding: utf-8 -*-
"""
Базовый Класс содержит базовые свойства номера
"""

import logging
import copy
from abc import ABCMeta
from abc import abstractmethod
from sources.base_repr import BaseRepr
from sources.error import DuplicateError


log_base_dn = logging.getLogger("migrate.base_dn")


class BaseDn(BaseRepr, metaclass=ABCMeta):

    def __init__(self, set_node):
        self._set_node = copy.deepcopy(set_node)
        self._active_services = []
        self._type_dn = None
        self._set_node['password'] = ''
        self._set_node['DN'] = None

    @abstractmethod
    def set_type_dn(self):
        """
        Определяет тип Номера - SIP, PSTN.
        Определяется в наследуемых классах.
        """
        pass

    @property
    def dn(self):
        """ Возвращает номер по ключу 'DN' """
        return self._set_node['DN']

    @dn.setter
    def dn(self, val):
        """ Присваивание номера по ключу 'DN' """
        self._set_node['DN'] = val

    @property
    def display_name(self):
        return self._set_node.get('Отображение имени', '')

    @display_name.setter
    def display_name(self, val):
        self._set_node['Отображение имени'] = val

    @property
    def password(self):
        """ Возвращает пароль по ключу 'password' """
        return self._set_node['password']

    @password.setter
    def password(self, val):
        """ Присваивает пароль по ключу 'password' """
        self._set_node['password'] = val

    @property
    def all_options(self):
        """
        Возвращает все свойства номера: Услуги, категорию, ограничений и т.д.
        по которым будет выполняться маппинг
        """
        return self._set_node.get('all_options', [])

    @all_options.setter
    def all_options(self, val):
        """
        Сохранение всех свойств номера: Услуги, категорию, ограничений и т.д.
        по которым будет выполняться маппинг
        """
        if self._set_node.get('all_options') is None:
            self._set_node['all_options'] = [str(item) for item in val if item]
        else:
            [self._set_node['all_options'].append(str(item)) for item in val if item]

    @property
    def suspend(self):
        return self._set_node.get('suspend', []) or []

    @property
    def active_services(self):
        return self._active_services

    @active_services.setter
    def active_services(self, val):
        try:
            _val = list(iter(val))
        except TypeError:
            _val = [val]
        [self._active_services.append(act) for act in _val]

    @property
    def concurent_sessions(self):
        """
        Обработка количества одновременных сессий у мигрированного номера
        Возвращаем:
         * None если у номера нет такого свойства или 0
         * 1,2,30 - если совпадает с [1,2,30]
         * 30 - если значение больше 2
        """
        num_sessions = self._set_node.get('concurent_sessions')
        if num_sessions is None or int(num_sessions) == 0:
            return None
        elif int(num_sessions) in [1, 2, 30]:
                return num_sessions
        elif int(num_sessions) > 2:
            return '30'

    @concurent_sessions.setter
    def concurent_sessions(self, val):
        """
        Выставляем номеру количетсво одновременных сессий
        из обрабатываемого номера
        """
        self._set_node['concurent_sessions'] = str(int(val))

    @abstractmethod
    def get_msan_interface(self):
        """
        Австрактный метод определяется в наследуемых классах
        В зависимости от типа номера - возвращает кортеж с данными о
        принадлежности в интерфейсу: (ID, Port).
        Если атрибут self._type_dn != 'pstn', то возвращаем пустой кортеж: ('', '')
        Пример:
            if self._type_dn != 'pstn':
                return ('', '',)
        """
        pass

    def check_duplicate_intf(self):
        """
        Проверка на дублирование детектированного интерфейса с описанными в
        конфиге set_node.json
        """
        from collections import defaultdict
        c_intf = defaultdict(int)
        c_name = defaultdict(int)
        for msan in self._set_node['msan']:
            c_intf[msan['id']] += 1
            c_name[msan['name']] += 1

        for id_intf, count_id in c_intf.items():
            if count_id > 1:
                raise DuplicateError(f"Detected duplicating interface "
                                     f"id: '{id_intf}' from 'msan' "
                                     f"section in 'set_node.json'")
        for id_name, count_name in c_name.items():
            if count_name > 1:
                raise DuplicateError(f"Detected duplicating  interface name: "
                                     f"'{id_name}' from 'msan' "
                                     f"section in 'set_node.json'")

    def __eq__(self, other):
        return self.dn == other.dn
