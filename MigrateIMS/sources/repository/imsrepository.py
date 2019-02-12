import logging
from sources.repository.baserepository import BaseRepo


log_def_subs_repo = logging.getLogger("migrate.defsubsrepo")


class ImsSubsRepo(BaseRepo):
    """ Хранилище преобразованных базовых номеров, для импорта на vIMS """
    pass
