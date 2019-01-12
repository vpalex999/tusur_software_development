

class Config(object):
    """ Класс хранит конфигурационные данные для работы конвертера """

    all_type_dn = ['sip', 'pstn', 'other']
    nodes = ['MT20', 'AXE-10']

    def __init__(self, node=None, sf_db=None, sd_db=None, type_dn='sip', cli=None):
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

        cli(dict) -- принимаются аргументы  при запуске из командной строки в формате словаря.

        """
        self.node = node
        self.source_db = None
        self.source_file_db = sf_db
        self.source_dir_db = sd_db
        self.type_dn = type_dn
        self.cli = cli

    @classmethod
    def from_cli(cls, cli):
        """
        Альтернативный конструктор класса который принимает словарь
        специализированных аргументов cli.
        """
        cnfg = cls(cli=cli).parce_cli()
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

    def parce_type_dn_cli(self):
        """
        Проверка ввода типа обрабатываемых номеров (sip, pstn, all) из
        словаря аргументов консольного ввода cli.
        Конвертер за один проход обрабатывает только один тип номеров.
        """
        if self.cli is not None:

            if len(self.cli.keys()) == 0: raise Exception('The cli args is empty')

            list_type = []
            if self.cli.get('--sip') is True: list_type.append('sip')
            if self.cli.get('--pstn') is True: list_type.append('pstn')
            if self.cli.get('--all') is True: list_type.append('other')

            if len(list_type) > 1:
                raise Exception('Only one type of type_dn should be is set from cli: ', list_type)
            elif len(list_type) == 0:
                raise Exception('Not type_dn selected from cli')
            else:
                self.type_dn = list_type[0]

    def execute(self):
        """
        Инициализация конфигурационных данных,
        проверка на допустимость и т.д.
        """
        self.check_node()
        self.check_type_dn()
        return self

    def parce_cli(self):
        """ Парсинг аргументов из командной строки """
        self.parce_type_dn_cli()
        return self

