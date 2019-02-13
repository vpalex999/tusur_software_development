import logging


class MigrateError(Exception):
    def __init__(self, msg=""):
        self.msg = msg
        logging.error(f"{self.__class__.__name__}: {msg}")
