

class Config(object):
    """ Класс хранит конфигурационные данные для работы конвертера """

    all_type_dn = ['sip', 'pstn', 'other']

    def __init__(self, source_db=None, type_dn='sip', cli=None):
        """
        Аргументы инициализации класса

        Аргументы
        ---------
        source_db=None -- исходная база данных номеров. Может содержать
           текстовые данные в формате списка или объект. Если не указывается,
           то присваивается пустой список [].

        type_dn='sip' -- указывается тип обрабатываемых номеров (sip, pstn, other).

        cli=None -- принимаются аргументы  при запуске из командной строки в формате словаря.

        """
        self.source_db = [] if source_db is None else source_db
        self.type_dn = type_dn
        self.cli = cli
        #self.run_config = kwargs.get('run_config')

    @classmethod
    def from_cli(cls, cli):
        """
        Альтернативный конструктор класса который принимает только словарь аргументов cli
        """
        cnfg = cls(cli=cli).parce_cli()
        return cnfg

    def check_type_dn(self):
        """ Проверка хранения допустимого типа в атрибуте type_dn """
        if self.type_dn not in self.all_type_dn:
            raise Exception('The type_dn should be in: ', self.all_type_dn)

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
        self.check_type_dn()

    def parce_cli(self):
        self.parce_type_dn_cli()
        return self