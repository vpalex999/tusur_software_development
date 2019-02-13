import logging


class BaseRepo(object):
    """ Базовое хранилище номеров для импорта на vIMS """

    def __init__(self, subscribers=None):
        self._subscribers = []
        if subscribers:
            self._subscribers.extend(subscribers)

    def _check(self, element, key, value):

        return getattr(element, key) == (value)

    def list(self, filters=None):
        """
        Возвращает список номеров, хранящихся в репозиротории.
        Можно использовать фильтр по атрибутам номера

        Пример:
        -------
        filters={'type_dn': 'SIP'}
        """
        if not filters:
            result = self._subscribers
        else:
            result = []
            result.extend(self._subscribers)

            for key, value in filters.items():
                logging.debug('{}: filters values: {}:{}'.format(self.__class__.__name__, key, value))
                result = [e for e in result if self._check(e, key, value)]

        return [s for s in result]

    def add(self, subscriber):
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)
            logging.info(f"{self.__class__.__name__}: Successfully added subscriber: {subscriber.dn}")
            return True
        else:
            logging.info('Duplicate data in repo: {}'.format(subscriber))
            return False

    def __len__(self):
        return len(self._subscribers)
        