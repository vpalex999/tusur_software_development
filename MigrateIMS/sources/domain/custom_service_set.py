
import json
from sources.domain.base_repr import BaseRepr
from sources.domain.license_type import LicenseType
from sources.domain.errors import MigrateError


class CustomServiceSet(BaseRepr):
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
        self._lic_type = LicenseType()

    def __getattr__(self, val):
        return getattr(self._lic_type, val)

    def make(self, list_services, category=None, license_type=None):
        """ Принимает список авторизованных услуг и выставляет соответствующим атрибутам значение 1 """
        self.__dict__.update(CustomServiceSet.def_custom_set)

        if category:
            self.subsctg = category

        if license_type is None:
            self.licenseType = self.get_id_lic_by_set(list_services)
        elif self.is_cover_lic(license_type, list_services):
                self.licenseType = self.get_id_by_name(license_type)
        else:
            raise MigrateError(f"The got licenseType '{license_type}' is not "
                               f"cover subscriber services: {list_services}")

        if list_services:
            for serv in list_services:
                if serv in self._auth_dvo:
                    setattr(self, self._auth_dvo[serv], "1")

        return self

    def __call__(self):
        return {key: self.__dict__[key] for key in self.__dict__ if not key.startswith('_')}
