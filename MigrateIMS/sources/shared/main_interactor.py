

class MainInteractor(object):

    def __init__(self, defsubsrepo):
        self.defsubsrepo = defsubsrepo

    def list_subscribers(self):
        return self.defsubsrepo.list()

    def execute(self):
        return self.list_subscribers()
