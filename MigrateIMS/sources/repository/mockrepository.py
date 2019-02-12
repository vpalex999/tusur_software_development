# -*- coding: utf-8 -*-
import os
import xlrd
import logging
from sources.repository.noderepository import NodeRepo
from sources.domain.nodesubscriber import NodeSubscriber
from sources.domain.errors import MigrateError


log_def_subs_repo = logging.getLogger("migrate.defsubsrepo")


class MockRepo(NodeRepo):
    """ Xранилище номеров Макета АТС для типа SIP """
    def __init__(self, config):
        super().__init__(config)
        try:
            if os.path.isfile(config.source_file_db):
                self.book = xlrd.open_workbook(config.source_file_db)
            else:
                self.book = None
        except TypeError as e:
            raise MigrateError(e)

    @property
    def check_book(self):
        """ Проверка на непустые входные данные """
        return bool(self.book)

    @property
    def sheet(self):
        """ Выбор 0 закладки книги """
        return self.book.sheet_by_index(0)

    @property
    def header(self):
        """ Читаем заголовки в 0 строке """
        return self.sheet.row_values(0)

    def zip_number(self, number):
        _n = dict(zip(self.header, number))
        return _n

    def get_numbers(self):
        _index = range(1, self.sheet.nrows)
        _numbers_gen = [self.sheet.row_values(i) for i in _index]
        return list(map(self.zip_number, _numbers_gen))

    def execute(self):
        
        if self.check_book:
    
            dn = dict()

            for row in self.get_numbers():
                dn['dn'] = str(int(row['Номер']))
                dn['type_dn'] = self.config.SIP
                dn['password'] = row['Пароль']
                dn['list_dn_options'] = [row['Категория'].strip()]
                dn['list_dn_options'].extend([suppl.strip() for suppl in row['Услуги'].split(',')])

                self.add(NodeSubscriber.from_dict(dn))

        return self
