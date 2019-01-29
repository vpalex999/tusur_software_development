# -*- coding: utf-8 -*-
""" Модуль обработки категорий АОН по заданным правилам 

Объект класса инициируется шаблоном с правилами преобразования типа dict.

Для получения категории из атрибутов номера - вызывается объект с акгументом - список атрибутов номера:

cat = category(list_of_attribute).

Если ни один из атрибутов номера не попадает под правила, то выдается категория
определённая по умолчанию.

Пример шаблона с правилами категорий:

{
  "Providers": [
      {"RT": {"AON": "1", "RULE": {"SR4": "56"}}},
      {"MTC": {"AON": "2", "RULE": {"SR3": "62"}}},
      {"VIMPEL": {"AON": "3", "RULE": {"SR5": "65"}}},
      {"EKVANT": {"AON": "4", "RULE": {"SR12": "63"}}},
      {"TRANST": {"AON": "6", "RULE": {"SR6": "58"}}},
      {"SINTERRA": {"AON": "7", "RULE": {"SR0": "59"}}},
      {"ARCTEL": {"AON": "8", "RULE": {"SR11 SR0": "64"}}},
      {"MTT": {"AON": "9", "RULE": {"SR1": "60"}}},
      {"CHOOSE_CALL": {"AON": "0", "RULE": {"SR4 SR7": "61"}}}
  ],
  "Default": [{"AON": "1", "id": "56"}]
}

"""

import collections


class Category(object):
    """
    Класс для вычисления категории АОН.
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

    def __init__(self, mapping_category):
        """ 
        Аргументы:
        - mapping_category (dict) -- шаблон с правилами перевода категорий.
        """
        if not isinstance(mapping_category, collections.Mapping):
          raise Exception("Class {}: the 'mapping_category' is not dictionary".format(self.__class__.__name__))
        self.mapping_category = mapping_category
        self.list_mapping = mapping_category['PROVIDERS']
        self.default = mapping_category['DEFAULT'][0]

    def get_default_category(self):
      """ Получить дефолтную категорию """
      try:
        return self.default['id']
      except KeyError as e:
        raise KeyError("Class {}: The Default category is not defined. {}".format(self.__class__.__name__, e))

    def __call__(self, subscriber_options):
        """
        Функция производит поиск id категории по ключу в
        правилах *self.mapping_category* в списке свойств номера *subscriber_options*.

        Аргументы:
        ----------
        subscriber_options (list) -- принимает список свойств в которых содержатся
          атрибуты номера, определяющие категорию.


        Ключ может быть составным, для этого слова в ключе разделяются пробелами:
        - {"SR4": "56"} -- несоставной ключ.
        - {"CPC HOTEL": "62"} -- составной ключ.

        Если ключ -- составной, то поиск будет успешным, если в *subscriber_options*
        будут присутствовать оба отрибута составного ключа, например:
        ['tsrd', 'SR4', 'RVT', 'CPC', 'HOTEL'] или ['tsrd', 'SR4', 'RVT', 'CPC HOTEL']

        Возврат:
        --------
        str -- номер категории в формате VIMS или категорию, определённую по умолчанию
        """

        category = None

        if not len(self.list_mapping):
          category = self.get_default_category()
          print("Class {}: The list of Providers is empty, so will get default category id:{}".format(self.__class__.__name__, category))
        elif subscriber_options is None or len(subscriber_options) == 0:
          category = self.get_default_category()
          print("Class {}: The subscriber options is empty, so will get default category id:{}".format(self.__class__.__name__, category))
        else:
          for rule in self.sort_list_rules():
              node_category, ims_category = rule
              _node_category = set(node_category.split(' '))
              if _node_category.issubset(set(subscriber_options)):
                return ims_category
              elif node_category in subscriber_options:
                return ims_category
          else:
            category = self.get_default_category()
  
        return category

    def sort_list_rules(self):
      """ Сортировка списка правил с весом ключа на убывание
      
      На выходе список котежей [(key, value)]
      Например: [("SR4", "56"), ]
      """
      list_rule = []
      for r in self.list_mapping:
        for k in r.values():
          list_rule.append(list(k['RULE'].items())[0])

      return sorted(list_rule, key=lambda x: len(x[0]), reverse=True)
  