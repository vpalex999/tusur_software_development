import logging
import abc
from abc import ABCMeta
from sources.repository.baserepository import BaseRepo

log_node_repo = logging.getLogger("migrate.noderepo")


class NodeRepo(BaseRepo, metaclass=ABCMeta):
    """ Xранилище номеров АТС """
    def __init__(self, config):
        super().__init__()
        self.config = config

    @abc.abstractmethod
    def execute(self):
        """ Обработчик для создания и добавления в хранилище
        номеров из исходный данных АТС

        Пример
        -------
        dn = dict()
        for row in self.parce_rows:
            dn['dn'] = row['Номер']
            dn['type_dn'] = self.config.SIP
            dn['password'] = 'test_iskratel'
            dn['list_dn_options'] = row['Услуги']
        self.add(NodeSubscriber.from_dict(dn))
        """
        pass
