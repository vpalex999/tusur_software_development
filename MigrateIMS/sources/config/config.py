
from sources.config.base_config import BaseConfig
from sources.domain.category import Category
from sources.domain.service import Service


class Config(BaseConfig):
    """ Класс хранит конфигурационные данные для работы конвертера """


    def services_handler(self, list_dn_options):
        return self.service(list_dn_options)

    def category_handler(self, list_dn_options):
        return self.category(list_dn_options)