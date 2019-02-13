# -*- coding: utf-8 -*-
""" Модуль обработки Авторизованных услуг по заданным правилам """

import collections
import logging
from sources.domain.errors import MigrateError


class Service(object):
    """
    Класс хранит шаблон правил переноса авторизованных услуг.

    Атрибуты
    ---------
    self.mapping_service - хранит шаблон(словарь) с правилами перноса услуг.
    self.list_mapping  - хранит извлечённый список правил из шаблон(словарь) с правилами перноса услуг.
    """

    def __init__(self, mapping_service):
        """
        Аргументы:
        - mapping_service (dict) -- шаблон(словарь) с правилами перноса услуг.
        """
        if not isinstance(mapping_service, collections.Mapping):
            msg = "Class {}: the 'mapping_service' is not dictionary".format(self.__class__.__name__)
            raise MigrateError(msg)
    
        self.mapping_service = mapping_service
        self.list_mapping = self.mapping_service['SI']

    def __call__(self, subscriber_options):
        """
        Функция производит поиск авторизованных услуг из принятого списка свойств
        номера *subscriber_options* в правилах *self.mapping_service*.

        Аргументы:
        ----------
        subscriber_options (list) -- принимает список свойств в которых содержатся
          атрибуты номера, определяющие категорию.


        Ключ может быть составным, для этого слова в ключе разделяются пробелами:
        - {"RVT": "CFU"} -- несоставной ключ.
        - {"RVA ACS": "ACS"} -- составной ключ.

        Если ключ -- составной, то поиск будет успешным, если в *subscriber_options*
        будут присутствовать оба отрибута составного ключа, например:
        ['tsrd', 'SR4', 'RVT', 'RVA', 'ACS'] или ['tsrd', 'SR4', 'RVT', 'RVA ACS']

        Возврат:
        --------
        list -- список авторизованных услуг в формате VIMS или пустой список.
        """

        service = []

        if not len(self.list_mapping):
            logging.warning("Class {}: The list of SI is empty, so will get empty service list".format(self.__class__.__name__))
        elif subscriber_options is None or len(subscriber_options) == 0:
            logging.warning("Class {}: The subscriber options is empty, so will get empty service list".format(self.__class__.__name__))
        else:
            for rule in self.sort_list_rules():
                node_service, ims_service = rule
                _node_service = set(node_service.split(' '))
                if _node_service.issubset(set(subscriber_options)):
                    service.extend(ims_service)
                elif node_service in subscriber_options:
                    service.extend(ims_service)
        if not service:
            logging.warning("Class: {} In The subscriber options has not options for mapping rules: {}".format(self.__class__.__name__, subscriber_options))

        return service

    def sort_list_rules(self):
        """ Сортировка списка правил с весом ключа на убывание

        На выходе список котежей [(key, value)]
        Например: [("SR4", "56"), ]
        """
        list_rule = [list(i) for i in self.list_mapping.items()]
        return sorted(list_rule, key=lambda x: len(x[0]), reverse=True)
  