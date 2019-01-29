
import collections


class DocOpt(object):
    """ Класс хранит аргументы командной строки принятые в формате dict """

    def __init__(self, docopt):
        """
        Аргументы инициализации класса

        Аргументы
        ---------
        docopt(dict) -- принимаются аргументы  при запуске из командной строки в формате словаря.
        """
        
        if not isinstance(docopt, collections.Mapping):
            raise Exception("Class {}: the cli is not dictionary".format(self.__class__.__name__))
        self.docopt = docopt
    

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
        self.category = Category(self.set_category)

    def make_service(self):
        """ Создать объект Service для обработки авторизованных услуг """
        self.service = Service(self.set_service)

    def get_node(self):
        pass

    def get_sourse_file_db(self):
        pass

    def get_source_dir_db(self):
        pass

    def get_type_dn(self):
        """ Вычислить тип конвертируемых номеров из словаря командной строки """
        list_type = []

        if self.docopt.get('--sip') is True:
            list_type.append('sip')
        if self.docopt.get('--pstn') is True:
            list_type.append('pstn')
        if self.docopt.get('--all') is True:
            list_type.append('other')

        if len(list_type) > 1:
            raise Exception('Only one type of type_dn should be is set from cli: ', list_type)
        elif len(list_type) == 0:
            raise Exception('Not type_dn selected from cli')
        else:
            return list_type[0]

    def get_mapping_category(self):
        pass

    def get_mapping_service(self):
        pass

    def get_mapping_ims(self):
        pass