# -*- coding: utf-8 -*-
""" Модуль обработки конфигурации IMS """

import collections
from sources.domain.base_repr import BaseRepr


class IMS(BaseRepr):
    """
    Класс хранит шаблон конфигурации IMS.
    """

    def __init__(self, mapping_ims):
        """
        Аргументы:
        - mapping_ims (dict) -- шаблон(словарь) конфигурации IMS.
        """
        if not isinstance(mapping_ims, collections.Mapping):
          raise Exception("Class {}: the 'mapping_ims' is not dictionary".format(self.__class__.__name__))
        for key in mapping_ims:
            self.__dict__.update(mapping_ims[key])

    def __getattribute__(self, attr):
        return object.__getattribute__(self, attr)
