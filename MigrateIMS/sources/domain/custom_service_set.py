
import json


class CustomServiceSet(object):
    """ Класс формирует кастомный набор услуг абонента """

    _auth_dvo = {
                  "CFU": 'cfuAuth',
                  "CFB": 'cfbAuth',
                  "CFNR": 'cfnrAuth',
                  "CCBS & CCNR": 'ccbsAuth',
                  "HOTI": 'hotiAuth',
                  "HOTD": 'hotdAuth',
                  "DND": 'dndAuth',
                  "CFNRC": 'cfnrcAuth',
                  "CD": 'cdAuth',
                  "ECT": 'ctAuth',
                  "AR": 'arAuth',
                  "LNR": 'abdsCategory',
                  "OIP": 'clipAuth',
                  "OIR": 'clirAuth',
                  "TIP": 'colpAuth',
                  "TIR": 'colrAuth',
                  "MCID": 'mcidAuth',
                  "CW": 'cwAuth',
                  "HOLD": 'holdAuth',
                  "3PTY": 's3ptyAuth',
                  "CONF": 'confAuth',
                  "PDCONF": 'pdcnfAuth',
                  "CBSC": 'cbscAuth',
                  "PEOC": 'peocAuth',
                  "FCR": 'fcrAuth',
                  "ACR": 'acrAuth',
                  "ACS": 'acsAuth',
    }

    def_custom_set = json.load(open('templates/template_custom_service_set.json'))

    def __init__(self):
        self.__dict__.update(CustomServiceSet.def_custom_set)

    def make(self, list_services, category=None):
        """ Принимает список авторизованных услуг и выставляет соответствующим атрибутам значение 1 """
        
        if category:
            self.subsctg = category

        if list_services:
            for serv in list_services:
                if serv in self._auth_dvo:
                    setattr(self, self._auth_dvo[serv], "1")

        return self
    
    def __call__(self):
        return {key:self.__dict__[key] for key in self.__dict__}
