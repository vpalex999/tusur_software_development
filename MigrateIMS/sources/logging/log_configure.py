"""" Модуль настройки логирования """
import os
import json
import logging.config


def setup_logging():
    """ Setup logging configuration """

    logging.config.dictConfig(_config)


_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "file_formatter": {
            "format": "%(asctime)s %(levelname)s | %(module)s - %(lineno)d | %(message)s"
        },
        "console_formatter": {
            "format": "%(asctime)s %(levelname)s | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "console_formatter",
            "stream": "ext://sys.stdout"
        },
        "file_debug": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "file_formatter",
            "filename": "migrate_debug.log",
            "maxBytes": 10485760,
            "backupCount": 5,
            "encoding": "utf8"
        },
        "file_info": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "file_formatter",
            "filename": "migrate_info.log",
            "maxBytes": 10485760,
            "backupCount": 5,
            "encoding": "utf8"
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["file_debug", "file_info", "console"]
    }
}


# ###################### Настройка логирования ############################## #
# filemode = 'w' - перезапись лога
#logger_main = logging.getLogger(__name__)
#logger_main.setLevel(logging.DEBUG)

#handler_main = logging.FileHandler("migrate.log", mode='w', encoding='utf-8')
#handler_main.setLevel(logging.DEBUG)
#formatter_main = logging.Formatter("%(asctime)s %(levelname)s | %(module)s - %(lineno)d | %(message)s")
#handler_main.setFormatter(formatter_main)
#logger_main.addHandler(handler_main)

#console_handler = logging.StreamHandler()
#console_handler.setLevel(logging.DEBUG)
#console_formatter = logging.Formatter("%(asctime)s %(levelname)s | %(message)s")
#console_handler.setFormatter(console_formatter)
#logger_main.addHandler(console_handler)

# ########################################################################### #
