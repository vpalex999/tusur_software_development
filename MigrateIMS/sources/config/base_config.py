
import abc
from abc import ABCMeta
from sources.domain.category import Category
from sources.domain.service import Service
from sources.domain.ims import IMS


class BaseConfig(metaclass=ABCMeta):
    """ Класс хранит конфигурационные данные для работы конвертера """

    PSTN = 'PSTN'
    ISDN = 'ISDN'
    SIP = 'SIP'
    OTHER = 'OTHER'

    all_type_dn = [SIP, PSTN, ISDN, OTHER]

    nodes = ['MT20', 'AXE-10']

    def __init__(self,
                 node=None,
                 type_dn='SIP',
                 sf_db=None,
                 sd_db=None,
                 mapping_category=None,
                 mapping_service=None,
                 mapping_ims=None
                 ):
        """
        Аргументы инициализации класса

        Аргументы
        ---------
        node -- содержит название типа АТС для которой выполняется миграция.
           Все разрешённые типы, для которых возможна обработка данных
           находятся в классовом атрибуте 'nodes'.

        source_db(list or object) -- исходная база данных номеров. Может содержать
           текстовые данные в формате списка или объект.

        sf_db(str) -- имя файла с исходной базой данных. По умолчанию None.

        sd_db(str) -- имя директории с исходной базой данных. По умолчанию None.

        type_dn(str) -- указывается тип обрабатываемых номеров (sip, pstn, other).
           Все разрешённые типы, для которых возможна обработка данных
           находятся в классовом атрибуте 'all_type_dn'.
        """
        self.node = node
        self.type_dn = type_dn
        self.source_db = None
        self.source_file_db = sf_db
        self.source_dir_db = sd_db
        self.mapping_category = mapping_category  # шаблон маппинга категорий
        self.mapping_service = mapping_service  # шаблон маппинга услуг
        self.mapping_ims = mapping_ims  # шаблон настроек IMS

        self.category = None    # хранит объект для вычисления категорий
        self.service = None     # хранит объект для вычисления авторизованных услуг
        self.ims = None         # хранит объект для конфигурации IMS

    @classmethod
    def from_cli(cls, cli):
        """
        Альтернативный конструктор класса который принимает словарь
        специализированных аргументов cli.
        """
        cnfg = cls(node=cli.get_node(),
                   sf_db=cli.get_sourse_file_db(),
                   sd_db=cli.get_source_dir_db(),
                   type_dn=cli.get_type_dn(),
                   mapping_category=cli.get_mapping_category(),
                   mapping_service=cli.get_get_mapping_service(),
                   mapping_ims=cli.get_mapping_ims()
                   )
        return cnfg

    def check_node(self):
        """ Проверка названия обрабатываемого типа АТС из списка разрешённых типов """
        if self.node not in self.nodes:
            raise Exception("Unknown type of node '{}', Please select from this list'{}'".format(self.node, self.nodes))

    def check_type_dn(self):
        """ Проверка хранения допустимого типа в атрибуте type_dn """
        if self.type_dn not in self.all_type_dn:
            raise Exception('The type_dn should be in: ', self.all_type_dn)

    def check_source_db(self):
        """ Проверка наличия исходной БД """
        if (self.source_file_db is None and self.source_dir_db is None):
            raise Exception("Source DataBase is not selected")

    def make_category(self):
        """ Создать объект Category для обработки категорий """
        self.category = Category(self.mapping_category)

    def make_service(self):
        """ Создать объект Service для обработки авторизованных услуг """
        self.service = Service(self.mapping_service)
    
    def make_ims(self):
        """ Создать объект IMS для получения конфигурационных данных IMS """
        self.ims = IMS(self.mapping_ims)

    def execute(self):
        """
        Инициализация конфигурационных данных,
        проверка на допустимость и т.д.
        """
        self.check_node()
        self.check_type_dn()
        self.make_category()
        self.make_service()
        self.make_ims()
        return self

    @abc.abstractmethod
    def services_handler(self):
        pass

    @abc.abstractmethod
    def category_handler(self):
        pass