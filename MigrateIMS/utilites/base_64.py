# -*- coding: utf-8 -*-
"""
класс кодировки пароля в Base64
"""

import base64
#from sources.base_repr import BaseRepr


class B64(object):
    """
    Клас выполняет кодировку входных данных в формате base64

    name: - входные данные в формате str

    выходные данные - строка в кодировке base64

    Пример:

    b = B64('iskratel)

    c_encode = b()

    c_encode == 'aXNrcmF0ZWw='

    """
    def __init__(self, name):
        self._name = name
        self._test = 'aXNrcmF0ZWw='

    def decode(self):
        decode = base64.b64decode(self._name.encode('utf-8'))
        return str(decode, encoding='utf-8')

    def __call__(self):
        encoded = base64.b64encode(self._name.encode('utf-8'))
        return str(encoded, encoding='utf-8')
