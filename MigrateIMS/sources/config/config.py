
import json
import logging
from sources.config.base_config import *
from sources.domain.errors import MigrateError


class Config(BaseConfig):
    """ Класс хранит конфигурационные данные для работы конвертера """

    @classmethod
    def from_dict(cls, adict):
        logging.debug("Make Config from dictionary: {}".format(str(adict)))
        try:
            config = cls(
                        node=adict.get("node", ''),
                        type_dn=adict.get("type_dn", ''),
                        sf_db=adict.get("sourse_file_db", ''),
                        sd_db=adict.get('source_dir_db', ''),
                        mapping_category=json.load(open(adict.get("mapping_category", ''))),
                        mapping_service=json.load(open(adict.get("mapping_service", ''))),
                        mapping_ims=json.load(open(adict.get("mapping_ims", ''))),
                        dest_dir=adict.get('dest_dir', '')
            )
        except Exception as e:
            logging.error('Failed to make Config from dict: {}'.format(str(adict)), exc_info=True)
            raise MigrateError(e)
        return config

    def services_handler(self, list_dn_options):
        return self.service(list_dn_options)

    def category_handler(self, list_dn_options):
        return self.category(list_dn_options)
