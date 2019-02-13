# -*- coding: utf-8 -*-
""" Модуль представления сконвертированных номеров в формате для импорта на WEB PORTAL IMS """


class ViewWP(object):
    """
    Класс создаёт итерируемый объект обработанных номеров для последующей записи в файл

    Аргументы
    ---------

    """

    def __init__(self, list_subscribers):
        """
        Аргументы:
        - list_subscribers(dict)  - получает список номеров в формате словаря для импорта на WEB PORTAL IMS.
        """
        self.list_subscribers = list_subscribers

    def header_1(self):
        """ Формирование первого заголовка """
        if self.list_subscribers:
            header = []
            for key, field in self.list_subscribers[0].items():
                header.append(f"{key}|")
                header.extend(["|"for i in range(1, len(field.keys()))])

            return ''.join(header) + '\n'

    def header_2(self):
        """ Формирование второго заголовка """
        if self.list_subscribers:
            header = []
            for key, field in self.list_subscribers[0].items():
                header.extend(list(field.keys()))
            
            return '|'.join(header) + '|\n'

    def make_number(self, number):
        """ Формирование строки номера """
        return f"{'|'.join(['|'.join(list(number[key].values())) for key in number])}|\n"

    def __call__(self):
        """ Формирование конечного представления данных для импорта на WEB PORTAL IMS"""
        result = []
        if self.header_1():
            result.append(self.header_1())
            if self.header_2():
                result.append(self.header_2())
                result.extend(map(self.make_number, self.list_subscribers))
        
        return result
