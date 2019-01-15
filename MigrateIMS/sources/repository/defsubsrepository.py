

class DefSubsRepo(object):
    """ Хранилище базовых номеров, для импорта на vIMS """

    def __init__(self, subscribers=None):
        self._subscribers = []
        if subscribers:
            self._subscribers.extend(subscribers)

    def _check(self, element, key, value):

        if key in ['dn']:
            return getattr(element, key) == (value)

    def list(self, filters=None):
        if not filters:
            result = self._subscribers
        else:
            result = []
            result.extend(self._subscribers)
            
            for key, value in filters.items():
                print('values: {}:{}'.format(key, value))
                result = [e for e in result if self._check(e, key, value)]

        return [s for s in result]

    def add(self, subscriber):
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)
            return True
        else:
            print('Duplicate data in repo: {}'.format(subscriber))
            return False

    def __len__(self):
        return len(self._subscribers)
        