

class Config(object):
    def __init__(self, kwargs):
        self.run_config = None
        self.type_sip = 'sip' if kwargs.get('--sip') is True else None
        self.type_pstn = 'pstn' if kwargs.get('--pstn') is True else None
        self.type_all = 'all' if kwargs.get('--all') is True else None
        self.source_file_db = None

    def check_type_dn(self):
        """
        Проверка ввода типа обрабатываемых номеров (sip, pstn, all).
        Указан может быть только один тип или ни одного.
        Конвертер за один проход должен обрабатывать только один тип номеров.
        """
        tpl_type_dn = [self.type_sip, self.type_pstn, self.type_all]
        if tpl_type_dn.count(None) < 2:
            raise Exception('Only one type of type_dn should be is set: ', tpl_type_dn)

    @property
    def type_dn(self):
        return self.type_sip or self.type_pstn or self.type_all

    def execute(self):
        """
        Инициализация конфигурационных данных,
        проверка на допустимость и т.д.
        """
        self.check_type_dn()
