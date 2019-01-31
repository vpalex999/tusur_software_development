
import json


class CustomServiceSet(object):
    """ Класс формирует кастомный набор услуг абонента """

    def_custom_set = json.load(open('templates/template_custom_service_set.json'))

    def __init__(self):
        self.__dict__.update(CustomServiceSet.def_custom_set)
    
    def __call__(self):
        return {key:self.__dict__[key] for key in self.__dict__}
