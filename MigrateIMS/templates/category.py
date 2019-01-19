# -*- coding: utf-8 -*-
"""
Класс для обработки аргументов командной строки
"""

import logging
from sources.error import CategoryError

log_category = logging.getLogger("migrate.category")


class Category(object):
    """
    Класс для вычисления категории АОН.

    Аргументы:
    - subscriber_set (list) -- принимает список свойств в которых содержатся
      атрибуты номера, определяющие категорию.
    - template_set (dict) -- шаблон с правилами перевода категорий.
    - number_dn (str) -- Необязательный аргумент. Принимает номер в строковом
      формате для которого осуществяется обработка котегорий.

    Функция self.category - производит поиск id категории по ключу в
    правилах *template_set* в списке свойств номера *subscriber_set*.
    Ключ может быть составным, для этого слова в ключе разделяются пробелами:
    - {"SR4": "56"} -- несоставной ключ.
    - {"CPC HOTEL": "62"} -- составной ключ.
    Если ключ -- составной, то поиск будет успешным, если в *subscriber_set*
    будут присутствовать оба отрибута составного ключа, например:
    ['tsrd', 'SR4', 'RVT', 'CPC', 'HOTEL']
    """
    _ims_category = [
        {'id': '56', 'aon': '1'},
        {'id': '62', 'aon': '2'},
        {'id': '65', 'aon': '3'},
        {'id': '63', 'aon': '4'},
        {'id': '57', 'aon': '5'},
        {'id': '58', 'aon': '6'},
        {'id': '59', 'aon': '7'},
        {'id': '64', 'aon': '8'},
        {'id': '60', 'aon': '9'},
        {'id': '61', 'aon': '0'}
    ]

    def __init__(self, subscriber_set, template_set, number_dn='', **kwargs):
        self._subscriber_set = subscriber_set
        self._template_set = template_set
        self._number_dn = number_dn
        self._mapping_category = (kwargs.get('mapping_category', []) or [])

    @property
    def get_default_id(self):
        """ Получить id дефолтной категории """
        return self._template_set.get('Default')[0].get('id')

    @property
    def get_default_AON(self):
        """ Получить АОН дефолтной категории """
        return self._template_set.get('Default')[0].get('AON')

    def find_category_by_id(self, source_category_id):
        """ Поиск категории АОН по его id_SI3000 """

        for category in self._ims_category:
            if category['id'] == source_category_id:
                return category['aon']

        raise CategoryError(f"DN {self._number_dn} has undefaned id category "
                            f"from allowed values: {self._ims_category}")

    def find_id_category_by_aon(self, source_category_aon):
        """ Поиск категории id_SI3000 по его АОН """

        for category in self._ims_category:
            if category['aon'] == source_category_aon:
                return category['id']

        raise CategoryError(f"DN {self._number_dn} has undefaned id category "
                            f"from allowed values: {self._ims_category}")

    def get_mapping_category(self, source_category_id):
        """
        Получить новую категорию АОН из маппинг файла категорий
        Если есть совпадение по ключу, то возвращаем значение - новую категорию,
        Если не находим, то возвращаем - исходную.
        """

        _source_aon = self.find_category_by_id(source_category_id)

        for mapping in self._mapping_category:
            if _source_aon == mapping:
                log_category.info(f"DN {self._number_dn}: "
                                  f"detected are changing Subscriber Category "
                                  f"from {_source_aon} "
                                  f"to {self._mapping_category[mapping]}")
                return self.find_id_category_by_aon(self._mapping_category[mapping])
                break
        return source_category_id

    @property
    def category(self):
        logging.info(f"Start convert category")
        _default = self._template_set.get('Default')[0]
        if len(self._subscriber_set):
            for _category in self._template_set["Providers"]:
                for providers, category in _category.items():
                    orig_category, new_category = list(category['RULE'].items())[0]
                    if orig_category in self._subscriber_set:
                        return self.get_mapping_category(new_category)
                    _orig_category = set(orig_category.split(' '))
                    _s_set = set(self._subscriber_set)
                    if (_orig_category & _s_set) == _orig_category:
                        return self.get_mapping_category(new_category)
            else:
                log_category.\
                    warning(f"DN {self._number_dn}: Not found Subscriber "
                            f"Category from Subscriber Data combination:\n"
                            f"{self._subscriber_set}\nso, will be assigned"
                            f" the default category value: "
                            f"{self.get_default_AON}"
                            f" by id: {self.get_default_id}")
                return self.get_mapping_category(self.get_default_id)
        else:
            log_category.\
                    warning(f"DN {self._number_dn}: Not found Subscriber "
                            f"Category because data is empty:"
                            f"{self._subscriber_set} so, will be assigned "
                            f"the default value set: "
                            f"{_default.get('AON')} "
                            f" by id: "
                            f"{self.get_default_id}")
            return self.get_mapping_category(self.get_default_id)
