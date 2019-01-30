# -*- coding: utf-8 -*-
"""
Модуль для работы с шаблонами Service Set
"""
import re
import copy
import logging

from sources.utilites.file import read_json
from sources.services.license_type import LicenseType


log_service_set = logging.getLogger("migrate.service_set")


class ServiceSet(object):
    def __init__(self, subscriber_set, template_set, barring='0', number_dn=''):
        self._subscriber_set = subscriber_set
        self._template_set = template_set
        self._barring = barring
        self._number_dn = number_dn

    @classmethod
    def from_set(cls, defsbc):
        return cls(defsbc.dvo,
                   defsbc.suppl_set,
                   barring=defsbc.get_CBAC(),
                   number_dn=defsbc.dn).get_set

    @property
    def get_def_set(self):
        return self._template_set.get('Default_Set')

    @property
    def get_defaul_lic(self):
        _set = self._template_set.get('Predefined_Set').get(self.get_def_set)
        return _set.get('License Type')

    def get_category(self, num_set):
        _set = self._template_set.get('Predefined_Set').get(num_set)
        return _set.get('category', '')

    @property
    def get_set(self):
        if len(self._subscriber_set):
            for number_set, service in self._template_set["Predefined_Set"].items():
                if service.get('CBAC') != self._barring:
                    continue
                for suppl_subscriber in self._subscriber_set:
                    if suppl_subscriber in service['set']:
                        continue
                    else:
                        break
                else:
                    return number_set, service.get('License Type', ''), self.get_category(number_set)
            else:
                return self.get_custom_set()

        elif self._barring != '0':
            return self.get_default_set_CBAC()

        else:
            return self.get_default_set()

    def get_custom_set(self, cbac=''):
        log_service_set\
                    .warning(f"DN {self._number_dn}: Not found "
                             f"Sepplementary Service Set {cbac} suitable for services"
                             f" combination:\n\t{self._subscriber_set} so,"
                             f"will be assigned the Custom Service set.")
        return "-1", "", ""

    def get_default_set(self):
        """ Возвращает дефолтный SupplSet если нет услуги CBAC и нет ДВО"""
        log_service_set.info(f"DN {self._number_dn}: Subscriber has not"
                             f" any services so, will be assigned the"
                             f" default Suppl Service Set:"
                             f"{self._template_set['Default_Set']}")
        return (self.get_def_set,
                self.get_defaul_lic,
                self.get_category(self.get_def_set))

    def get_default_set_CBAC(self):
        """ Возвращаем дефолтный SupplSet_CBAC если есть услуга CBAC и нет ДВО """
        for num_def_set in self._template_set["Default_Set_CBAC"]:
            for number_set, service in self._template_set["Predefined_Set"].items():
                if num_def_set == number_set:
                    if self._barring == service.get('CBAC'):
                        return (number_set,
                                service.get('License Type', ''),
                                self.get_category(number_set))
        return self.get_custom_set(cbac="for CBAC")


class CustomServiceSet(object):
    """ Класс формирует кастомный набор услуг абонента"""

    _def_custom_set = read_json('templates/template_custom_service_set.json')

    _set_inband_type = {
        'ISDN Public': 1,
        'Analog Public': 2,
        'ISDN PBX': 3,
        'Analog PBX': 4,
        'PC Applications': 5
    }

    _set_display_ring_type = {
        'Analog Public': 1,
        'Analog PBX': 2,
        'Not Used': 3
    }

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

    def __init__(self, subscriber):
        self._subscriber = subscriber
        self._custom_set = copy.deepcopy(self._def_custom_set)

    @property
    def get_custom_set(self):
        self.custom_set()
        self.auth_set()
        return self._custom_set

    @property
    def get_str_custom_set(self):
        return re.sub('\'', '\"', str(self.get_custom_set))

    def custom_set(self):
        self.subsctg = int(self._subscriber.category)
        self.licenseType = self._subscriber.license
        self.inbandIndType = self._subscriber.inband
        self.displayRingType = self._subscriber.disp_ring_type
        self.set_CBAC()

    def auth_set(self):
        if self._subscriber.dvo is None or\
                len(self._subscriber.dvo) == 0:
            return

        for _dvo in self._subscriber.dvo:

            try:
                exec(f"self.{self._auth_dvo[_dvo]} = 1")
            except KeyError:
                log_service_set.warning(f"DN {self._subscriber.dn} has "
                                        f"unrecognized supplementary service "
                                        f"for Auth: {_dvo}")

    def set_CBAC(self):
        self._custom_set['cbacBarrclass'] = self._subscriber.get_CBAC()

    @property
    def cbacBarrclass(self):
        return self._custom_set.get('cbacBarrclass')

    @property
    def cfuAuth(self):
        return self._custom_set.get('cfuAuth')

    @cfuAuth.setter
    def cfuAuth(self, val):
        self._custom_set['cfuAuth'] = val

    @property
    def cfbAuth(self):
        return self._custom_set.get('cfbAuth')

    @cfbAuth.setter
    def cfbAuth(self, val):
        self._custom_set['cfbAuth'] = val

    @property
    def cfnrAuth(self):
        return self._custom_set.get('cfnrAuth')

    @cfnrAuth.setter
    def cfnrAuth(self, val):
        self._custom_set['cfnrAuth'] = val

    @property
    def ccbsAuth(self):
        return self._custom_set.get('ccbsAuth')

    @ccbsAuth.setter
    def ccbsAuth(self, val):
        self._custom_set['ccbsAuth'] = val

    @property
    def hotiAuth(self):
        return self._custom_set.get('hotiAuth')

    @hotiAuth.setter
    def hotiAuth(self, val):
        self._custom_set['hotiAuth'] = val

    @property
    def hotdAuth(self):
        return self._custom_set.get('hotdAuth')

    @hotdAuth.setter
    def hotdAuth(self, val):
        self._custom_set['hotdAuth'] = val

    @property
    def dndAuth(self):
        return self._custom_set.get('dndAuth')

    @dndAuth.setter
    def dndAuth(self, val):
        self._custom_set['dndAuth'] = val

    @property
    def cfnrcAuth(self):
        return self._custom_set.get('cfnrcAuth')

    @cfnrcAuth.setter
    def cfnrcAuth(self, val):
        self._custom_set['cfnrcAuth'] = val

    @property
    def cdAuth(self):
        return self._custom_set.get('cdAuth')

    @cdAuth.setter
    def cdAuth(self, val):
        self._custom_set['cdAuth'] = val

    @property
    def ctAuth(self):
        return self._custom_set.get('ctAuth')

    @ctAuth.setter
    def ctAuth(self, val):
        self._custom_set['ctAuth'] = val

    @property
    def arAuth(self):
        return self._custom_set.get('arAuth')

    @arAuth.setter
    def arAuth(self, val):
        self._custom_set['arAuth'] = val

    @property
    def abdsCategory(self):
        return self._custom_set.get('abdsCategory')

    @abdsCategory.setter
    def abdsCategory(self, val):
        self._custom_set['abdsCategory'] = val

    @property
    def clipAuth(self):
        return self._custom_set.get('clipAuth')

    @clipAuth.setter
    def clipAuth(self, val):
        self._custom_set['clipAuth'] = val

    @property
    def clirAuth(self):
        return self._custom_set.get('clirAuth')

    @clirAuth.setter
    def clirAuth(self, val):
        self._custom_set['clirAuth'] = val

    @property
    def colpAuth(self):
        return self._custom_set.get('colpAuth')

    @colpAuth.setter
    def colpAuth(self, val):
        self._custom_set['colpAuth'] = val

    @property
    def colrAuth(self):
        return self._custom_set.get('colrAuth')

    @colrAuth.setter
    def colrAuth(self, val):
        self._custom_set['colrAuth'] = val

    @property
    def mcidAuth(self):
        return self._custom_set.get('mcidAuth')

    @mcidAuth.setter
    def mcidAuth(self, val):
        self._custom_set['mcidAuth'] = val

    @property
    def cwAuth(self):
        return self._custom_set.get('cwAuth')

    @cwAuth.setter
    def cwAuth(self, val):
        self._custom_set['cwAuth'] = val

    @property
    def holdAuth(self):
        return self._custom_set.get('holdAuth')

    @holdAuth.setter
    def holdAuth(self, val):
        self._custom_set['holdAuth'] = val

    @property
    def s3ptyAuth(self):
        return self._custom_set.get('s3ptyAuth')

    @s3ptyAuth.setter
    def s3ptyAuth(self, val):
        self._custom_set['s3ptyAuth'] = val

    @property
    def confAuth(self):
        return self._custom_set.get('confAuth')

    @confAuth.setter
    def confAuth(self, val):
        self._custom_set['confAuth'] = val

    @property
    def pdcnfAuth(self):
        return self._custom_set.get('pdcnfAuth')

    @pdcnfAuth.setter
    def pdcnfAuth(self, val):
        self._custom_set['pdcnfAuth'] = val

    @property
    def cbscAuth(self):
        return self._custom_set.get('cbscAuth')

    @cbscAuth.setter
    def cbscAuth(self, val):
        self._custom_set['cbscAuth'] = val

    @property
    def peocAuth(self):
        return self._custom_set.get('peocAuth')

    @peocAuth.setter
    def peocAuth(self, val):
        self._custom_set['peocAuth'] = val

    @property
    def fcrAuth(self):
        return self._custom_set.get('fcrAuth')

    @fcrAuth.setter
    def fcrAuth(self, val):
        self._custom_set['fcrAuth'] = val

    @property
    def acrAuth(self):
        return self._custom_set.get('acrAuth')

    @acrAuth.setter
    def acrAuth(self, val):
        self._custom_set['acrAuth'] = val

    @property
    def acsAuth(self):
        return self._custom_set.get('acsAuth')

    @acsAuth.setter
    def acsAuth(self, val):
        self._custom_set['acsAuth'] = val
###########################################################

    @property
    def subsctg(self):
        return self._custom_set.get('subsctg')

    @subsctg.setter
    def subsctg(self, val):
        self._custom_set['subsctg'] = val

    @property
    def licenseType(self):
        return self._custom_set.get('licenseType')

    @licenseType.setter
    def licenseType(self, val):
        self._custom_set['licenseType'] = int(LicenseType.get_id(val))

    @property
    def inbandIndType(self):
        return self._custom_set.get('inbandIndType')

    @inbandIndType.setter
    def inbandIndType(self, val):
        self._custom_set['inbandIndType'] = self._set_inband_type.get(val, '3')

    @property
    def displayRingType(self):
        return self._custom_set.get('displayRingType')

    @displayRingType.setter
    def displayRingType(self, val):
        self._custom_set['displayRingType'] = self._set_display_ring_type.get(val, '2')
