# -*- coding: utf-8 -*-
"""
Класс для отображения отрибутов класса в _repr_
"""


class BaseRepr(object):

    def __repr__(self):
        attrs = ', \n'.join([f"{atr}={getattr(self, atr)}"
                            for atr in self.__dict__])
        return f"{self.__class__.__name__}:\n{attrs}\n"
