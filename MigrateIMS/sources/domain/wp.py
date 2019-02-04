# -*- coding: utf-8 -*-
"""
    Модуль миграции на Web Portal
"""
import re
import logging
import copy

from sources.utilites.base_64 import B64
from sources.error import MigrateElementError
from sources.utilites.file import read_json

log_wp = logging.getLogger("migrate.web_portal")


class WpDn(object):
    """
    Конечная обработка данных номера для формирования
    импорта на Web Portal
    """

    _ims = read_json('templates/template_ims.json')

    def __init__(self, number, config_ims):
        self._number = number
        self._config_ims = dict(config_ims.get('IMS'))
        self._template_ims = copy.deepcopy(self._ims)

    #@classmethod
    #def migrate_mt20(cls, data, config):
    #    return cls(data, config.config_ims).greate_import_wp(mt20=True)

    #@classmethod
    #def migrate_sip(cls, data, config):
    #    return cls(data, config.config_ims).greate_import_wp(sip=True)

    @classmethod
    def migrate(cls, data, config):
        return cls(data, config.config_ims).greate_import_wp(node=config.node)

    @staticmethod
    def del_key(dict_in, list_of_delete):
        """ Удаление ключа в словаре по имени ключа"""
        list_key = dict_in.keys()
        for k in list(list_key):
            if k in list_of_delete:
                del dict_in[k]
            elif isinstance(dict_in[k], dict):
                WpDn.del_key(dict_in[k], list_of_delete)

    @staticmethod
    def del_key_by_val(dict_in):
        """ Удаление ключа в словаре по значению ключа - 'delete' """
        list_of_delete = ['delete']
        list_key = dict_in.keys()
        for k in list(list_key):
            if dict_in[k] in list_of_delete:
                del dict_in[k]
            elif isinstance(dict_in[k], dict):
                WpDn.del_key_by_val(dict_in[k])

    @property
    def ndc(self):
        return self._config_ims.get('NDC')

    @property
    def domain(self):
        return self._config_ims.get('IMS domain')

    @property
    def name(self):
        return self._template_ims.get("IMS User Subscription").get("Name *")

    @name.setter
    def name(self, val):
        self._template_ims["IMS User Subscription"]["Name *"] = val

    @property
    def capabilities_set(self):
        return self._template_ims.get("IMS User Subscription")\
                                 .get("Capabilities Set")

    @capabilities_set.setter
    def capabilities_set(self, val):
        self._template_ims["IMS User Subscription"]["Capabilities Set"] = val

    @property
    def preferred_set(self):
        return self._template_ims\
            .get("IMS User Subscription").get("Preferred S-CSCF Set")

    @preferred_set.setter
    def preferred_set(self, val):
        self._template_ims["IMS User Subscription"]["Preferred S-CSCF Set"] = val

    @property
    def identity(self):
        return self._template_ims\
            .get('IMS Private User Identity').get('Identity')

    @identity.setter
    def identity(self, val):
        self._template_ims['IMS Private User Identity']['Identity'] = val

    @property
    def secret_key_k(self):
        return self._template_ims\
            .get('IMS Private User Identity').get('Secret Key K *')

    @secret_key_k.setter
    def secret_key_k(self, val):
        self._template_ims['IMS Private User Identity']['Secret Key K *'] = val

    @property
    def authorization_schemes(self):
        return self._template_ims\
            .get('IMS Private User Identity').get('Authorization Schemes')

    @authorization_schemes.setter
    def authorization_schemes(self, val):
        self._template_ims['IMS Private User Identity']['Authorization Schemes'] = val

    @property
    def def_authorization_schemes(self):
        return self._template_ims\
            .get('IMS Private User Identity').get('Default Auth. Scheme')

    @def_authorization_schemes.setter
    def def_authorization_schemes(self, val):
        self._template_ims['IMS Private User Identity']['Default Auth. Scheme'] = val

    @property
    def identity_public(self):
        return self._template_ims.get('IMS Public User Identity')\
            .get('Identity *')

    @identity_public.setter
    def identity_public(self, val):
        self._template_ims['IMS Public User Identity']['Identity *'] = val

    @property
    def type_public(self):
        return self._template_ims.get('IMS Public User Identity').get('Type')

    @type_public.setter
    def type_public(self, val):
        self._template_ims['IMS Public User Identity']['Type'] = val

    @property
    def barring(self):
        return self._template_ims.get('IMS Public User Identity')\
            .get('Barring')

    @barring.setter
    def barring(self, val):
        self._template_ims['IMS Public User Identity']['Barring'] = val

    @property
    def service_profile(self):
        return self._template_ims.get('IMS Public User Identity')\
            .get('Service Profile')

    @service_profile.setter
    def service_profile(self, val):
        self._template_ims['IMS Public User Identity']['Service Profile'] = val

    @property
    def implicit_set(self):
        return self._template_ims.get('IMS Public User Identity')\
            .get('Implicit Set Identity')

    @implicit_set.setter
    def implicit_set(self, val):
        self._template_ims['IMS Public User Identity']['Implicit Set Identity'] = val

    @property
    def charging_info(self):
        return self._template_ims.get('IMS Public User Identity')\
            .get('Charging Info')

    @charging_info.setter
    def charging_info(self, val):
        self._template_ims['IMS Public User Identity']['Charging Info'] = val

    @property
    def wildcard_psi(self):
        return self._template_ims.get('IMS Public User Identity')\
            .get('Wildcard PSI')

    @wildcard_psi.setter
    def wildcard_psi(self, val):
        self._template_ims['IMS Public User Identity']['Wildcard PSI'] = val

    @property
    def display_name(self):
        return self._template_ims.get('IMS Public User Identity')\
            .get('Display Name')

    @display_name.setter
    def display_name(self, val):
        self._template_ims['IMS Public User Identity']['Display Name'] = val

    @property
    def psi_activation(self):
        return self._template_ims.get('IMS Public User Identity')\
            .get('PSI Activation')

    @psi_activation.setter
    def psi_activation(self, val):
        self._template_ims['IMS Public User Identity']['PSI Activation'] = val

    @property
    def can_register(self):
        return self._template_ims.get('IMS Public User Identity')\
            .get('Can Register')

    @can_register.setter
    def can_register(self, val):
        self._template_ims['IMS Public User Identity']['Can Register'] = val

    @property
    def allowed_roaming(self):
        return self._template_ims.get('IMS Public User Identity')\
            .get('Allowed Roaming')

    @allowed_roaming.setter
    def allowed_roaming(self, val):
        self._template_ims['IMS Public User Identity']['Allowed Roaming'] = val

    @property
    def type_agcf(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('Type *')

    @type_agcf.setter
    def type_agcf(self, val):
        self._template_ims['Access Gateway Control Function']['Type *'] = val

    @property
    def node_agcf(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('Node *')

    @node_agcf.setter
    def node_agcf(self, val):
        self._template_ims['Access Gateway Control Function']['Node *'] = val

    @property
    def pub_id_alias_agcf(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('Public Id Alias *')

    @pub_id_alias_agcf.setter
    def pub_id_alias_agcf(self, val):
        self._template_ims['Access Gateway Control Function']['Public Id Alias *'] = val

    @property
    def uri_type_agcf(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('URI Type *')

    @uri_type_agcf.setter
    def uri_type_agcf(self, val):
        self._template_ims['Access Gateway Control Function']['URI Type *'] = val

    @property
    def interface(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('Interface *')

    @interface.setter
    def interface(self, val):
        self._template_ims['Access Gateway Control Function']['Interface *'] = val

    @property
    def access(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('Access *')

    @access.setter
    def access(self, val):
        self._template_ims['Access Gateway Control Function']['Access *'] = val

    @property
    def access_variant(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('Access Variant *')

    @access_variant.setter
    def access_variant(self, val):
        self._template_ims['Access Gateway Control Function']['Access Variant *'] = val

    @property
    def rtp_profile(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('RTP Profile *')

    @rtp_profile.setter
    def rtp_profile(self, val):
        self._template_ims['Access Gateway Control Function']['RTP Profile *'] = val

    @property
    def password(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('Password *')

    @password.setter
    def password(self, val):
        self._template_ims['Access Gateway Control Function']['Password *'] = val

    @property
    def private_id_alias(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('Private Id Alias')

    @private_id_alias.setter
    def private_id_alias(self, val):
        self._template_ims['Access Gateway Control Function']['Private Id Alias'] = val

    @property
    def embed_teluri(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('Embed telURI into SIP URI')

    @embed_teluri.setter
    def embed_teluri(self, val):
        self._template_ims['Access Gateway Control Function']['Embed telURI into SIP URI'] = val

    @property
    def dtmf(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('DTMF Authorization')

    @dtmf.setter
    def dtmf(self, val):
        self._template_ims['Access Gateway Control Function']['DTMF Authorization'] = val

    @property
    def out_of_service(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('Out of Service Indication')

    @out_of_service.setter
    def out_of_service(self, val):
        self._template_ims['Access Gateway Control Function']['Out of Service Indication'] = val

    @property
    def active_subscriber(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('Active Subscriber')

    @active_subscriber.setter
    def active_subscriber(self, val):
        self._template_ims['Access Gateway Control Function']['Active Subscriber'] = val

    @property
    def initiate_reg_startup(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('Initiate registration at system startup')

    @initiate_reg_startup.setter
    def initiate_reg_startup(self, val):
        self._template_ims['Access Gateway Control Function']['Initiate registration at system startup'] = val

    @property
    def display_ring_type(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('Display/Ring Type')

    @display_ring_type.setter
    def display_ring_type(self, val):
        self._template_ims['Access Gateway Control Function']['Display/Ring Type'] = val

    @property
    def inband(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('In-band Indication Type')

    @inband.setter
    def inband(self, val):
        self._template_ims['Access Gateway Control Function']['In-band Indication Type'] = val

    @property
    def tariff_origin_code(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('Tariff Origin Code')

    @tariff_origin_code.setter
    def tariff_origin_code(self, val):
        self._template_ims['Access Gateway Control Function']['Tariff Origin Code'] = val

    @property
    def standalone_mode(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('Standalone Mode Calls')

    @standalone_mode.setter
    def standalone_mode(self, val):
        self._template_ims['Access Gateway Control Function']['Standalone Mode Calls'] = val

    @property
    def hotline_agcf(self):
        return self._template_ims.get('Access Gateway Control Function')\
            .get('Hotline Enable')

    @hotline_agcf.setter
    def hotline_agcf(self, val):
        self._template_ims['Access Gateway Control Function']['Hotline Enable'] = val

    @property
    def public_id_alias(self):
        return self._template_ims.get('IMS Public Identities from implicit registration set')\
            .get('Public Id Alias')

    @public_id_alias.setter
    def public_id_alias(self, val):
        self._template_ims['IMS Public Identities from implicit registration set']['Public Id Alias'] = val

    @property
    def uri_type(self):
        return self._template_ims.get('IMS Public Identities from implicit registration set')\
            .get('URI Type')

    @uri_type.setter
    def uri_type(self, val):
        self._template_ims['IMS Public Identities from implicit registration set']['URI Type'] = val

    @property
    def hotline_enable(self):
        return self._template_ims.get('IMS Public Identities from implicit registration set')\
            .get('Hotline Enable')

    @hotline_enable.setter
    def hotline_enable(self, val):
        self._template_ims['IMS Public Identities from implicit registration set']['Hotline Enable'] = val

    @property
    def msn(self):
        return self._template_ims.get('IMS Public Identities from implicit registration set')\
            .get('Set as MSN Number')

    @msn.setter
    def msn(self, val):
        self._template_ims['IMS Public Identities from implicit registration set']['Set as MSN Number'] = val

# Telephony Application Server #

    @property
    def tas_node(self):
        return self._template_ims.get('Telephony Application Server')\
            .get('TAS Node')

    @tas_node.setter
    def tas_node(self, val):
        self._template_ims['Telephony Application Server']['TAS Node'] = val

    @property
    def tas_alias(self):
        return self._template_ims.get('Telephony Application Server')\
            .get('TAS Public Id Alias')

    @tas_alias.setter
    def tas_alias(self, val):
        self._template_ims['Telephony Application Server']['TAS Public Id Alias'] = val

    @property
    def supl_serv_set(self):
        return self._template_ims.get('Telephony Application Server')\
            .get('Supplementary Service Set')

    @supl_serv_set.setter
    def supl_serv_set(self, val):
        self._template_ims['Telephony Application Server']['Supplementary Service Set'] = val

    @property
    def concurent_session(self):
        return self._template_ims.get('Telephony Application Server')\
            .get('Concurrent Sessions')

    @concurent_session.setter
    def concurent_session(self, val):
        self._template_ims['Telephony Application Server']['Concurrent Sessions'] = val

    @property
    def license(self):
        return self._template_ims.get('Telephony Application Server')\
            .get('License Type*')

    @license.setter
    def license(self, val):
        self._template_ims['Telephony Application Server']['License Type*'] = val

    @property
    def subscriber_category(self):
        return self._template_ims.get('Telephony Application Server')\
            .get('Subscriber Category')

    @subscriber_category.setter
    def subscriber_category(self, val):
        self._template_ims['Telephony Application Server']['Subscriber Category'] = val

    @property
    def m_sip_profile_class(self):
        return self._template_ims.get('Telephony Application Server')\
            .get('m.SipProfile.class')

    @m_sip_profile_class.setter
    def m_sip_profile_class(self, val):
        self._template_ims['Telephony Application Server']['m.SipProfile.class'] = val

    @property
    def business_group(self):
        return self._template_ims.get('Telephony Application Server')\
            .get('Business Group')

    @business_group.setter
    def business_group(self, val):
        self._template_ims['Telephony Application Server']['Business Group'] = val

    @property
    def custom_serv_set(self):
        return self._template_ims.get('Telephony Application Server')\
            .get('Custom Service Set')

    @custom_serv_set.setter
    def custom_serv_set(self, val):
        self._template_ims['Telephony Application Server']['Custom Service Set'] = val

# Additional parameters needed  for migration #

    @property
    def ngn_interface(self):
        return self._template_ims.get('Additional parameters needed  for migration')\
            .get('NGN Interface *')

    @ngn_interface.setter
    def ngn_interface(self, val):
        self._template_ims['Additional parameters needed  for migration']['NGN Interface *'] = val

    @property
    def ngn_access(self):
        return self._template_ims.get('Additional parameters needed  for migration')\
            .get('NGN Access *')

    @ngn_access.setter
    def ngn_access(self, val):
        self._template_ims['Additional parameters needed  for migration']['NGN Access *'] = val

    @property
    def ngn_access_var(self):
        return self._template_ims.get('Additional parameters needed  for migration')\
            .get('NGN Access Variant *')

    @ngn_access_var.setter
    def ngn_access_var(self, val):
        self._template_ims['Additional parameters needed  for migration']['NGN Access Variant *'] = val

    @property
    def ngn_rtp_profile(self):
        return self._template_ims.get('Additional parameters needed  for migration')\
            .get('NGN RTP Profile *')

    @ngn_rtp_profile.setter
    def ngn_rtp_profile(self, val):
        self._template_ims['Additional parameters needed  for migration']['NGN RTP Profile *'] = val

    @property
    def time_zone(self):
        return self._template_ims.get('Additional parameters needed  for migration')\
            .get('Time Zone', "") or ""

    @time_zone.setter
    def time_zone(self, val):
        self._template_ims['Additional parameters needed  for migration']['Time Zone'] = val

    @property
    def geo_area(self):
        return self._template_ims.get('Additional parameters needed  for migration')\
            .get('Geographical Area', "") or ""

    @geo_area.setter
    def geo_area(self, val):
        self._template_ims['Additional parameters needed  for migration']['Geographical Area'] = val

# ######################### IMS User Subscription #############################

    def set_number(self):
        """
        Формирует поле Name \*::

           - Value is calculated based on defined DN, NDC and CC data from NGN

        * Обязательный параметр.
        """
        if self._number.dn is None:
            raise MigrateElementError(f"Attribute with name 'DN' "
                                      f"contains is None:{self._number.dn}")
        if not isinstance(self._number.dn, str):
            raise MigrateElementError(f"Inconsistent type 'DN' "
                                      f"should be type is string:"
                                      f"{self._number.dn}")
        if self._number.dn in [""]:
            raise MigrateElementError(f"'Create field Name *'. Attribute with "
                                      f"name 'DN' is Empty:{self._number.dn}")
        else:
            result_name = f"+{self.ndc}{self._number.dn}"
            if len(result_name) == 12 and result_name.startswith('+7'):
                self.name = result_name
            else:
                raise MigrateElementError(f"DN has wrong format: NDC: "
                                          f"'{self.ndc}', DN must be in the "
                                          f"format - 7(10digits of DN): "
                                          f"{self._number.dn}")

    def set_capabilities(self):
        """
        Формирует поле 'Capabilities Set'::

           - Id of HSS Capabilities Set. This set shall be created on HSS
             (via HSS GUI) first.
           - Settings to define rules for selecting S-CSCF where user is
             redirected for registration.

        * Определено на стороне IMS.
        * Должен быть заранее создан на HSS.
        * Если такого поля нет, то по дефолту выставляем: "".
        * Значение должено быть представлено числом в строковом формате.
        * Необязательный параметр.
        """
        capabilities = self._config_ims.get('Capabilities Set')
        if capabilities is None:
            log_wp.info(f"Not found or got 'null' the label 'Capabilities Set'"
                        f" in '--config_wp' data, so taked data from"
                        f" template_IMS")
        else:
            if not isinstance(capabilities, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Capabilities Set' should be type"
                                          f" is string:{self._config_ims}")
            if capabilities not in [""]:
                if not capabilities.isdigit():
                    raise MigrateElementError(f"Inconsistent data, the type "
                                              f"'Capabilities Set' should be"
                                              f" digits:{self._config_ims}")
                self.capabilities_set = capabilities

    def set_preferred(self):
        """
        Формирует поле 'Preferred S-CSCF Set'::

           - Settings to define rules for selecting S-CSCF where user is
             redirected for registration.
           - Id of prefered S-CSCF Set. This set shall be created on HSS
             (via HSS GUI) first.

        * Определено на стороне IMS.
        * Должен быть заранее создан на HSS.
        * Если такого поля нет, то по дефолту выставляем: "".
        * Значение должено быть представлено числом в строковом формате.
        * Необязательный параметр.
        """
        preferred = self._config_ims.get('Preferred S-CSCF Set')
        if preferred is None:
            log_wp.info(f"Not found or got 'null' the label 'Preferred S-CSCF "
                        f"Set' in '--config_wp' data, so taked data from"
                        f" template_IMS")
        else:
            if not isinstance(preferred, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Preferred S-CSCF Set' should be"
                                          f" type is string:"
                                          f"{self._config_ims}")
            if preferred not in [""]:
                if not preferred.isdigit():
                    raise MigrateElementError(f"Inconsistent data, the type "
                                              f"'Preferred S-CSCF Set' should"
                                              f" be digits:{self._config_ims}")
                self.preferred_set = preferred

    def configure_subcription(self):
        """Конфигурируем поля IMS User Subscription
        """
        self.set_number()
        self.set_capabilities()
        self.set_preferred()

# ############################### IMS Private User Identity ###################

    def set_identity(self):
        """
        Формируем поле 'Identity' по формату: *+{NDC}{Name \*}{domain name}*.

        * Пример: +73436873639@dis.rd.mak
        * Вычисляемое поле.
        * Обязательный параметр.
        """
        _ius = self._template_ims.get('IMS User Subscription')
        if self.name is None:
            raise MigrateElementError(f"Not found attribute with name 'Name *'"
                                      f" or contains is None in "
                                      f"'IMS User Subscription':"
                                      f"\n{_ius}")
        if self.name in [""]:
            raise MigrateElementError(f"Inconsistent data, the type 'Name *' "
                                      f"should not is empty string:"
                                      f"\n{_ius}")
        self.identity = f"{self.name}@{self.domain}"

    def set_secret_key_k(self):
        """
        Формируем поле Secret Key K \*::

           - SIP password for authentication of SIP terminal to IMS

        * Определяется на стороне номера.
        * Для PSTN абонентов пароль формируется на этапе формирования
          дополнительных данных. Если не указан, то подставляем пороль
          iskratel.
        * Обязательный параметр.
        """
        secret_key = self._number.password
        if secret_key is None:
            raise MigrateElementError(f"Not found attribute with name "
                                      f"'Secret Key K *' contains is None in"
                                      f" source Number:"
                                      f"{self._number.get_number}")
        if not isinstance(secret_key, str):
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'Secret Key K *' "
                                      f"should be type is string:"
                                      f"{self._number.get_number}")
        if secret_key in [""]:
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'Secret Key K *' "
                                      f"contains is empty string in source"
                                      f" Number:{self._number.get_number}")
            if self.secret_key_k in ["", None] or not isinstance(self.secret_key_k, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Secret Key K *' in IMS config "
                                          f"should be type is string:"
                                          f"{self.secret_key_k}")
        secret_key = B64(secret_key)
        self.secret_key_k = secret_key()

    def set_authorization_schemes(self):
        """
        Формируем поле Authorization Schemes::

            - Supported authorization schemes. This the sum of supported
              authorization schemes.
            - System sets default value (=127) if value not inserted.

        * Определяется на стороне номера.
        * Если такого поля нет, то по дефолту выставляем "".
        * Значение должно быть представлено числом в диапазоне (1 -- 255) в
          строковом формате.
        * Необязательный параметр.
        """
        auth_scheme = self._number.authorization_schemes
        if auth_scheme is not None:
            if not isinstance(auth_scheme, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Authorization Schemes' should be"
                                          f" type is string:"
                                          f"{self._number.get_number}")
            if auth_scheme not in [""]:
                if not auth_scheme.isdigit():
                    raise MigrateElementError(f"Inconsistent data, the type "
                                              f"'Authorization Schemes' should"
                                              f" be consist of digits:"
                                              f"{self._number.get_number}")
                if int(auth_scheme) < 0 or int(auth_scheme) > 255:
                    raise MigrateElementError(f"Inconsistent data, the value "
                                              f"'Authorization Schemes' should"
                                              f" be between 0 & 255:"
                                              f"{self._number.get_number}")
                self.authorization_schemes = auth_scheme

    def set_def_auth_scheme(self):
        """
        Формируем поле 'Default Auth. Scheme'::

           - Selected default authorization scheme from list of available
             authorization schemes.
           - System sets default value (=1) if value not inserted.

        * Определяется на стороне номера.
        * Если у абонента такого поля нет, то по дефолту выставляем "".
        * Варианты: ['1', '2', '4', '8', '16', '32', '64', '128', ""]

        | Allowed values:
        | 1=NASS Bundled
        | 2=Early IMS
        | 4=HTTP DIGEST MD5
        | 8=Digest
        | 16=Digest MD5
        | 32=Digest AKAv2 MD5
        | 64=Digest AKAv1 MD5
        | 128=SIP Digest (3GPP)
        | Default: 1 если поле ""
        * Необязательный параметр.
        """
        choose_var = ['1', '2', '4', '8', '16', '32', '64', '128', ""]
        def_auth = self._number.def_authorization_schemes
        if def_auth is not None:
            if not isinstance(def_auth, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Default Auth. Scheme' should be "
                                          f"type is string:"
                                          f"{self._number.get_number}")
            if def_auth not in choose_var:
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Default Auth. Scheme' should be "
                                          f"choose of ({choose_var})in "
                                          f"{self._number.get_number}")
            self.def_authorization_schemes = def_auth

    def configure_private_user(self):
        """Конфигурируем поля IMS Private User Identity
        """
        # self.set_identity()
        self.set_authorization_schemes()
        self.set_def_auth_scheme()
        self.set_secret_key_k()

# ############################### IMS Public User Identity ####################

    def set_identity_public(self, impu=False):
        """
        Формируем поле Identity \*::

           - Value is calculated based on defined DN, NDC and CC data from NGN.

        * Вычисляемое поле через 'Name \*'.
        * Пример: sip:+73436873639@dis.rd.mak
        * Обязательный параметр.
        """
        _impu = f"sip:{self.name}@{self.domain}"

        if self.name is None:
            raise MigrateElementError(f"Not found attribute with name 'Name *'"
                                      f" or contains is None in 'IMS User "
                                      f"Subscription':{self.name}")
        if self.name in [""]:
            raise MigrateElementError(f"Inconsistent data, the type 'Name *' "
                                      f"should not is empty string:"
                                      f"{self.name}")
        if impu:
            return _impu
        else:
            self.identity_public = _impu

    def set_type_public(self):
        """
        Формируем поле Type::

           - Public Identity Type:
              - Valid values:
                 - Public User Identity
                 - Distinct PSI
                 - Wildcarded PSI
                 - Default: Public User Identity
           - System sets default value (=Public User Identity)
             if value not inserted.

        * Определяется на стороне номера.
        * Может принимать значения
          ['Public User Identity', 'Distinct PSI', 'Wildcarded PSI', ""]
        * Необязательный параметр.
        """
        choose_type = ['Public User Identity',
                       'Distinct PSI', 'Wildcarded PSI', ""]
        public_type = self._number.type_
        if public_type is not None:
            if not isinstance(public_type, str):
                raise MigrateElementError(f"Inconsistent data, the type 'Type'"
                                          f" should be type is string:"
                                          f"{self._number.get_number}")
            if public_type not in choose_type:
                raise MigrateElementError(f"Inconsistent data, the type 'Type'"
                                          f" should be choose of (choose_type)"
                                          f":{self._number.get_number}")
            self.type_public = public_type

    def set_barring(self):
        """
        Формируем поле Barring::

           - Barring of this Identity.
              - Valid values:
                 - no
                 - yes
                 - Default: no
           - System sets default value (=No) if value not inserted.

        * Определено на стороне IMS.
        * Может принимать значения ['no', 'yes', ""].
        * Если нет поля, то выставляем ""(=no).
        * Необязательный параметр.
        """
        choose_barring = ['no', 'yes', ""]
        barring = self._config_ims.get("Barring")
        if barring is None:
            log_wp.info(f"Not found or got 'null' the label 'Barring' in "
                        f"'--config_wp' data, so taked data from "
                        f"template_IMS: {self._config_ims}")
        else:
            if not isinstance(barring, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Barring' should be type is "
                                          f"string:{self._config_ims}")
            if barring not in choose_barring:
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Barring' should be choose of "
                                          f"({choose_barring}):"
                                          f"{self._config_ims}")
            self.barring = barring

    def set_service_profile(self):
        """
        Формируем поле 'Service Profile'. Номер профиля TAS сервера.
        Определено на стороне IMS.
        Должен быть заранее создан на HSS.
        Если такого поля нет, то по дефолту выставляем: "".
        Значение должено быть представлено числом в строковом формате.

        - Обязательный параметр, если абонент пользуется ДВО.
        - Обязательный параметр.
        """
        s_profile = self._config_ims.get('Service Profile')
        if s_profile is None:
            raise MigrateElementError(f"Not found attribute with name "
                                      f"'Service Profile' or contains is None:"
                                      f"\n{self._config_ims}")
        if not isinstance(s_profile, str):
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'Service Profile' should be type "
                                      f"is string:{self._config_ims}")
        if not s_profile.isdigit():
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'Service Profile' should be consist of"
                                      f" digits:{self._config_ims}")
        self.service_profile = s_profile

    def set_implicit_set(self):
        """
        Формируем поле 'Implicit Set Identity'.

        * Вычисляемое поле.
        * Обязательный параметр.
        """
        if self.name is None:
            raise MigrateElementError(f"Not found attribute with name 'Name *'"
                                      f" or contains is None in "
                                      f"'IMS User Subscription':{self.name}")
        self.implicit_set = f"sip:{self.name}@{self.domain}"

    def set_charging_info(self):
        """
        Формируем поле 'Charging Info'
        Определено на стороне IMS.
        Если такого поля нет, то по дефолту выставляем: "".
        Значение должено быть представлено числом в строковом формате.
        Необязательный параметр.
        """
        charg_info = self._config_ims.get('Charging Info')
        if charg_info is not None:
            if not isinstance(charg_info, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Charging Info' should be type "
                                          f"is string:{self._config_ims}")
            if charg_info not in [""]:
                if not charg_info.isdigit():
                    raise MigrateElementError(f"Inconsistent data, the type "
                                              f"'Charging Info' should be "
                                              f"consist of digits:"
                                              f"{self._config_ims}")
                self.charging_info = charg_info

    def set_wildcard_psi(self):
        """
        Формируем поле 'Wildcard PSI'.
        Определено на стороне IMS.
        Если такого поля нет, то по дефолту выставляем: "".
        Значение должено быть представлено числом в строковом формате
        с максимальным значением знаков: 255.
        Необязательный параметр.
        """
        wildcard = self._config_ims.get('Wildcard PSI')
        if wildcard is not None:
            if not isinstance(wildcard, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Wildcard PSI' should be type is "
                                          f"string:{self._config_ims}")
            if wildcard not in [""]:
                if len(wildcard) > 255:
                    raise MigrateElementError(f"Inconsistent data, the type "
                                              f"'Wildcard PSI' should be "
                                              f"less 255:{self._config_ims}")
                self.wildcard_psi = wildcard

    def set_display_name(self):
        """Формируем поле 'Display Name'.

        * Определяется на стороне номера.
        * Если такого поля нет, то по дефолту выставляем: "".
        * Значение должено быть представлено в строковом формате.
          с максимальным значением знаков: 255.
        * Необязательный параметр.
        """
        display = self._number.display_name
        if display is not None:
            if not isinstance(display, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Display Name' should be type is "
                                          f"string:{self._number.get_number}")
            if display not in [""]:
                if len(display) > 255:
                    raise MigrateElementError(f"Inconsistent data, the type "
                                              f"Display Name' should be less "
                                              f"255:{self._number.get_number}")
                self.display_name = display

    def set_psi_activation(self):
        """Формируем поле 'PSI Activation'.
        Определено на стороне IMS.
        Может принимать значения ['no', 'yes', ""]
        Если нет поля, то выставляем ""
        Необязательный параметр.
        """
        choose_psi = ['no', 'yes', ""]
        psi_act = self._config_ims.get('PSI Activation')
        if psi_act is not None:
            if psi_act not in choose_psi:
                raise MigrateElementError(f"Read the incorrect value of "
                                          f"'PSI Activation', it should be set"
                                          f" to {choose_psi}:"
                                          f"{self._config_ims}")
            self.psi_activation = psi_act

    def set_can_register(self):
        """
        Формируем поле 'Can Register'.
        Определено на стороне IMS.
        Может принимать значения ['no', 'yes', ""]
        Если нет поля, то выставляем ""
        Необязательный параметр.
        !!! В процедуре миграции, данный параметр выставляется в 'no'
        """
        can_reg = self._config_ims.get('Can Register')
        if can_reg is not None:
            if can_reg not in ["no"]:
                raise MigrateElementError(f"Read the incorrect value, for "
                                          f"Migration this 'Can Register' "
                                          f"should be set to 'no': "
                                          f"{self._config_ims}")
            self.can_register = can_reg

    def set_allowed_roaming(self):
        """
        Формируем поле 'Allowed Roaming'::

           - Array of visited (allowed) networks, in which public identity
             can register.
           - Parameters of visited network object are explained in Table 8:
             Visited Network model.
           - Values are separated with commas.

        * Определено на стороне IMS.
        * Строка должна содержать строку чисел: "1,2".
        * Если нет поля, то выставляем "1"
        * Необязательный параметр.
        """
        roaming = self._config_ims.get('Allowed Roaming')
        if roaming is not None:
            if roaming in [""]:
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Allowed Roaming' not should be "
                                          f"type is empty string:"
                                          f"{self._config_ims}")
            if not isinstance(roaming, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Allowed Roaming' should be type "
                                          f"is string:{self._config_ims}")
            r = []
            for roam in roaming.split(','):
                if not roam.strip().isdigit():
                    raise MigrateElementError(f"Inconsistent data, the type "
                                              f"'Allowed Roaming' should be "
                                              f"values is digit:"
                                              f"{self._config_ims}")
                r.append(roam.strip())
            self.allowed_roaming = ",".join(r)

    def configure_public_user(self):
        # self.set_identity_public() #
        self.set_type_public()
        self.set_barring()
        self.set_service_profile()
        # self.set_implicit_set() #
        self.set_charging_info()
        self.set_wildcard_psi()
        self.set_display_name()
        self.set_psi_activation()
        self.set_psi_activation()
        self.set_can_register()
        self.set_allowed_roaming()


# ############################### Access Gateway Control Function #############

    def set_type_agcf(self):
        """
        Формируем поле 'Type \*'.
        Определяется на стороне номера.
        Значение в диапазоне: ['Analog Subscriber', 'ISDN Subscriber', '']
        Если не PSTN номер, то дефолтное значение: "" берётся из шаблона IMS.
        Oбязательный параметр для PSTN.
        """
        choose_type_asterisk = ['Analog Subscriber', 'ISDN Subscriber']
        type_ = self._number.type_asterisk
        if type_ is None:
            raise MigrateElementError(f"Not found attribute with name 'Type *'"
                                      f" or contains is None:"
                                      f"\n{self._number.get_number}")
        if type_ not in choose_type_asterisk:
            raise MigrateElementError(f"Inconsistent data, the type 'Type *' "
                                      f"should be choose of "
                                      f"({choose_type_asterisk}):"
                                      f"\n{self._number.get_number}")
        self.type_agcf = type_

    def set_node_agcf(self):
        """
        Формируем поле 'Node \*' - номер AGCF.
        Определено на стороне IMS.
        Значение должено быть представлено числом в строковом формате.
        Если не PSTN номер, то дефолтное значение: "".
        Обязательный параметр для PSTN.
        """
        node_ = self._config_ims.get('Node *')
        if node_ is None:
            raise MigrateElementError(f"Not found attribute with name 'Node *'"
                                      f" or contains is None:"
                                      f"\n{self._config_ims}")
        if not isinstance(node_, str):
            raise MigrateElementError(f"Inconsistent data, the type 'Node *' "
                                      f"should be type is string:"
                                      f"{self._config_ims}")
        if not node_.isdigit():
            raise MigrateElementError(f"Inconsistent data, the type 'Node *' "
                                      f"in AGCF should be consist of digits:"
                                      f"{self._config_ims}")
        self.node_agcf = node_

    def set_pub_id_alias_agcf(self):
        """
        Формируем поле Public Id Alias \*.
        Вычисляемое поле.
        Обязательный параметр.
        """
        pub_id_alias = self.name
        self.pub_id_alias_agcf = re.sub('[+]', '', pub_id_alias)

    def set_uri_type_agcf(self):
        """
        Формируем поле URI 'Type \*'.
        Определено на стороне IMS.
        Может принимать значения ["", 'telUri', 'sipUri']
        Если нет поля, то выставляем: ""(=telUri).
        Oбязательный параметр для PSTN.
        """
        choose_uri_agcf = ["", 'telUri', 'sipUri']
        uri_ = self._config_ims.get('URI Type *')
        if uri_ is None:
            raise MigrateElementError(f"Not found attribute with name "
                                      f"'URI Type *' or contains is None:"
                                      f"\n'{self._config_ims}'")
        if not isinstance(uri_, str):
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'URI Type *' should be type is string:"
                                      f"\n'{self._config_ims}'")
        if uri_ not in choose_uri_agcf:
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'URI Type *' in AGCF should be consist"
                                      f" one of {choose_uri_agcf}:"
                                      f"\n'{self._config_ims}'")
        self.uri_type_agcf = uri_

    def set_interface(self, attr_interface):
        """
        Формируем поле 'Interface \*'.
        Определено на стороне номера.
        Строка должна содержать номер(ID)интерфейса AGCF.
        Обязательный параметр.
        """
        _interface = self._number.iad if self._number.iad else self._number.interface
        if _interface is None:
            raise MigrateElementError(f"Not found attribute with name "
                                      f"'Interface *' or contains is None:"
                                      f"'{_interface}'")
        if not isinstance(_interface, str):
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'Interface *' should be type is "
                                      f"string:'{_interface}'")
        if not _interface.isdigit():
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'Interface *' in AGCF should be "
                                      f"consist of digits:'{_interface}'")

        setattr(self, attr_interface, _interface)

    def set_access(self, attr_access):
        """
        Формируем поле 'Access \*'.
        Определено на стороне номера.
        Строка должна содержать номер(ID) порта в интерфейсе на AGCF .
        Обязательный параметр.
        """
        _access = self._number.access
        if _access is None:
            raise MigrateElementError(f"Not found attribute with name "
                                      f"'Access *' or contains is None:"
                                      f"'{_access}'")
        if not isinstance(_access, str):
            raise MigrateElementError(f"Inconsistent data, the type 'Access *'"
                                      f" should be type is string:"
                                      f"'{_access}'")
        if not _access.isdigit():
            raise MigrateElementError(f"DN {self.name}: Inconsistent data, the type 'Access *'"
                                      f" in AGCF should be consist of digits:"
                                      f"'{_access}'")
        setattr(self, attr_access, _access)

    def set_access_variant(self, attr_access_variant):
        """
        Формируем поле Access 'Variant \*'.

        * Определяется на стороне номера.
        * Строка должна содержать номер(ID) варианта порта доступа в AGCF 
          интерфейсе.
        * Используется только для Аналоговых номеров, Для ISDN оставляем "".
        * Значение должено быть представлено числом в строковом формате.
        * Обязательный параметр для PSTN.
        """
        _access_var = self._number.access_variant
        if _access_var is None:
            raise MigrateElementError(f"Not found attribute with name "
                                      f"'Access Variant *' or contains is "
                                      f"None:'{_access_var}'")
        if not isinstance(_access_var, str):
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'Access Variant *' should be type is "
                                      f"string:'{_access_var}'")
        if self.type_agcf == 'Analog Subscriber':
            if not _access_var.isdigit():
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Access Variant *' in AGCF should "
                                          f"be consist of digits:"
                                          f"'{_access_var}'")
            setattr(self, attr_access_variant, _access_var)

        elif _access_var not in [""]:
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'Access Variant *' in AGCF should be "
                                      f"consist of '':'{_access_var}'")

    def set_rtp_profile(self, attr_rtp_profile):
        """
        Формируем поле RTP 'Profile \*'.

        * Определяется на стороне номера.
        * Строка должна содержать номер(ID) RTP профиля порта доступа в AGCF
          интерфейсе.
        * Используется только для ISDN.
        * Для Аналоговых оставляем: "".
        * Обязательный параметр.
        """
        _rtp_profile = self._number.rtp_profile
        if self.type_agcf == 'ISDN Subscriber':
            if _rtp_profile is None:
                raise MigrateElementError(f"Not found attribute with name "
                                          f"'RTP Profile *' or contains is None:"
                                          f"'{_rtp_profile}'")
            if not isinstance(_rtp_profile, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'RTP Profile *' should be type is "
                                          f"string:'{_rtp_profile}'")
            if _rtp_profile not in [""]:
                if not _rtp_profile.isdigit():
                    raise MigrateElementError(f"Inconsistent data, the type "
                                              f"'RTP Profile *' in AGCF should be "
                                              f"consist of digits:"
                                              f"'{_rtp_profile}'")
                setattr(self, attr_rtp_profile, _rtp_profile)
        else:
            setattr(self, attr_rtp_profile, "")

    def set_password(self):
        """
        Формируем поле 'Password \*'::

           - Password for IMS user authentication during IMS registration.

        * Копируется с поля: Secret Key K \*.
        * Обязательный параметр.
        """
        _password = self.secret_key_k
        if _password is None:
            raise MigrateElementError(f"Not found attribute with name "
                                      f"'Secret Key K *' contains is None in "
                                      f"source Number:'{_password}'")
        if not isinstance(_password, str):
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'Secret Key K *' contains is empty "
                                      f"string in source Number:'{_password}'")
        if _password in "":
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'Secret Key K *' contains is empty "
                                      f"string in source Number:'{_password}'")
        self.password = _password

    def set_private_id_alias(self):
        """
        Формируем поле 'Private Id Alias'
        Определено на стороне IMS.
        Значение должено быть представлено числом в строковом формате.
        Если нет поля, то выставляем "".
        Необязательный параметр.
        """
        _priv_id_alias = self._config_ims.get('Private Id Alias')
        if _priv_id_alias is not None:
            if _priv_id_alias not in [""]:
                if not isinstance(_priv_id_alias, str):
                    raise MigrateElementError(f"Inconsistent data, the type "
                                              f"'Private Id Alias' should be "
                                              f"type is string:"
                                              f"\n{self._config_ims}")
                if not _priv_id_alias.isdigit():
                    raise MigrateElementError(f"Inconsistent data, the type "
                                              f"'Private Id Alias' in AGCF "
                                              f"should be consist of digits:"
                                              f"\n{self._config_ims}")
                self.private_id_alias = _priv_id_alias

    def set_embed_teluri(self):
        """
        Формируем поле 'Embed telURI into SIP URI'
        Определено на стороне IMS.
        Значение в диапазоне ['no', 'yes', ""]
        Если нет поля, то выставляем ""(=yes).
        Необязательный параметр.
        """
        choose_embed = ['no', 'yes', ""]
        _embed = self._config_ims.get('Embed telURI into SIP URI')
        if _embed is not None:
            if not isinstance(_embed, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Embed telURI into SIP URI' should"
                                          f" be type is string:"
                                          f"\n{self._config_ims}")
            if _embed not in choose_embed:
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Type public' should be choose of "
                                          f"({choose_embed}):"
                                          f"\n{self._config_ims}")
            self.embed_teluri = _embed

    def set_dtmf(self):
        """
        Формируем поле 'DTMF Authorization'.
        Определяется на стороне номера.
        Значение в диапазоне ['no', 'yes', ""]
        Если нет поля, то выставляем ""(=no).
        Необязательный параметр.
        """
        choose_dtmf = ['no', 'yes', ""]
        _dtmf = self._number.dtmf
        if _dtmf is not None:
            if _dtmf not in choose_dtmf:
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'DTMF Authorization' should be "
                                          f"choose of ({choose_dtmf}):"
                                          f"'{_dtmf}'")
            self.dtmf = _dtmf

    def set_out_of_service(self):
        """
        Формируем поле 'Out of Service Indication'
        Определяется на стороне номера.
        Значение в диапазоне ['no', 'yes', ""]
        Если нет поля, то выставляем ""(=no).
        Необязательный параметр.
        """
        choose_out = ['no', 'yes', ""]
        _out_of_service = self._number.out_of_service
        if _out_of_service is not None:
            if not isinstance(_out_of_service, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Out of Service Indication' should"
                                          f" be type is string:"
                                          f"'{_out_of_service}'")
            if _out_of_service not in choose_out:
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Out of Service Indication' should"
                                          f" be choose of ({choose_out}):"
                                          f"'{_out_of_service}'")
            self.out_of_service = _out_of_service

    def set_active_subscriber(self):
        """
        Формируем поле 'Active Subscriber'.
        Определено на стороне IMS.
        Определяет вкл/выкл порта доступа.
        Значение в диапазоне ['no', 'yes', ""]
        Если нет поля, то выставляем ""(=no).
        Необязательный параметр.
        """
        choose_active = ['no', 'yes', ""]
        _active = self._config_ims.get('Active Subscriber')
        if _active is not None:
            if not isinstance(_active, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Active Subscriber' should be type"
                                          f" is string:\n{self._config_ims}")
            if _active not in choose_active:
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Active Subscriber' should be "
                                          f"choose of ({choose_active}):"
                                          f"\n{self._config_ims}")
            self.active_subscriber = _active

    def set_initiate_reg_startup(self):
        """
        Формируем поле 'Initiate registration at system startup'.
        Определяется на стороне номера.
        Значение в диапазоне ['no', 'yes', ""]
        Если нет поля, то выставляем ""(=no).
        Необязательный параметр.
        Для PSTN выставляем "yes'
        """
        choose_startup = ['no', 'yes', ""]
        _init_reg_startup = self._number.init_reg_startup
        if _init_reg_startup is not None:
            if not isinstance(_init_reg_startup, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Initiate registration' at system "
                                          f"startup' should be type is string:"
                                          f"'{_init_reg_startup}'")
            if _init_reg_startup not in choose_startup:
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Initiate registration' at system"
                                          f" startup' should be choose of "
                                          f"({choose_startup}):"
                                          f"'{_init_reg_startup}'")
            self.initiate_reg_startup = _init_reg_startup

    def set_display_ring_type(self):
        """
        Формируем поле 'Display/Ring Type'.
        Определяется на стороне номера.
        Значение в диапазоне ['Analog Public', 'Analog PBX', 'Not Used', ""]
        Если нет поля, то выставляем ""(='Analog Public).
        Необязательный параметр.
        Для PSTN выставляем "Analog Public'
        """
        choose_disp_ring = ['Analog Public', 'Analog PBX', 'Not Used', ""]
        _d_ring_t = self._number.disp_ring_type
        if _d_ring_t is not None:
            if not isinstance(_d_ring_t, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Display/Ring Type' at system "
                                          f"startup' should be type is string:"
                                          f"'{_d_ring_t}'")
            if _d_ring_t not in choose_disp_ring:
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Display/Ring Type' at system "
                                          f"startup' should be choose of "
                                          f"({choose_disp_ring}):"
                                          f"'{_d_ring_t}'")
            self.display_ring_type = _d_ring_t

    def set_inband(self):
        """
        Формируем поле 'In-band Indication Type'
        Определяется на стороне номера.
        Значение в диапазоне ['ISDN Public', 'Analog Public', 'ISDN PBX',
        'Analog PBX', 'PC', '']
        Если нет поля, то выставляем: ""(=ISDN Public).
        Необязательный параметр.
        Для аналоговых номеров PSTN выставляем "Analog Public'
        """
        choose_inband = ['ISDN Public', 'Analog Public', 'ISDN PBX',
                         'Analog PBX', 'PC', '']
        _in_band = self._number.inband
        if _in_band is not None:
            if not isinstance(_in_band, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'In-band Indication Type' at "
                                          f"system startup' should be type is "
                                          f"string:'{_in_band}'")
            if _in_band not in choose_inband:
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'In-band Indication Type' at "
                                          f"system startup' should be choose "
                                          f"of ({choose_inband}):"
                                          f"'{_in_band}'")
            self.inband = _in_band

    def set_tariff_origin_code(self):
        """
        Формируем поле 'Tariff Origin Code'.
        Определено на стороне IMS.
        Значение должено быть представлено числом в строковом формате.
        Если нет поля, то выставляем: '1'.
        Необязательный параметр.
        """
        _tariff = self._config_ims.get('Tariff Origin Code')
        if _tariff is None:
            _tariff = "1"
        elif _tariff not in ["1"]:
            if not isinstance(_tariff, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Tariff Origin Code' should be "
                                          f"type is string:"
                                          f"\n{self._config_ims}")
            if not _tariff.isdigit():
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Tariff Origin Code' in AGCF "
                                          f"should be consist of digits:"
                                          f"\n{self._config_ims}")
        self.tariff_origin_code = _tariff

    def set_standalone_mode(self):
        """
        Формируем поле 'Standalone Mode Calls'.
        Определено на стороне IMS.
        Значение в диапазоне ['no', 'yes', '']
        Если нет поля, то выставляем: ""(=no).
        Необязательный параметр.
        """
        choose_mode = ['no', 'yes', '']
        _standalone = self._config_ims.get('Standalone Mode Calls')
        if _standalone is not None:
            if not isinstance(_standalone, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Standalone Mode Calls' should be "
                                          f"type is string:"
                                          f"\n{self._config_ims}")
            if _standalone not in choose_mode:
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Standalone Mode Calls' should be"
                                          f" choose of ({choose_mode}):"
                                          f"\n{self._config_ims}")
            self.standalone_mode = _standalone

    def set_hotline_agcf(self):
        """
        Формируем поле Hotline Enable.
        Определяется на стороне номера.
        Значение в диапазоне ['none', 'hotd', 'hoti']
        Если нет поля, то выставляем: "none".
        Необязательный параметр.
        """
        choose_hotline = ['hotd', 'hoti', 'none']
        _hotline = self._number.hotline
        if _hotline is None:
            self.hotline_agcf = 'none'
        else:
            if not isinstance(_hotline, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Hotline Enable' should be type is"
                                          f" string:'{_hotline}'")
            if _hotline not in choose_hotline:
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Hotline Enable' should be choose"
                                          f" of ({choose_hotline}):"
                                          f"'{_hotline}'")
            self.hotline_agcf = _hotline

    def configure_agcf(self, node=None):
        """
        Конфигурируем Access Gateway Control Function
        """
        if self._number.type_dn == 'pstn':
            self.set_type_agcf()
            self.set_node_agcf()
            # self.set_pub_id_alias_agcf()
            self.set_uri_type_agcf()
            self.set_interface('interface')
            self.set_access('access')
            self.set_access_variant('access_variant')
            self.set_rtp_profile('rtp_profile')
            self.set_password()
            self.set_private_id_alias()
            self.set_embed_teluri()
            self.set_dtmf()
            self.set_out_of_service()
            self.set_active_subscriber()
            self.set_initiate_reg_startup()
            self.set_display_ring_type()
            self.set_inband()
            self.set_tariff_origin_code()
            self.set_standalone_mode()
            self.set_hotline_agcf()

# ############# IMS Public Identities from implicit registration set ##########

    def set_public_id_alias(self):
        """
        Формируем поле Public Id Alias.
        Вычисляемое поле.
        Обязательный параметр для SIP.
        """
        if self._number.type_asterisk in [None, ""]:
            self.public_id_alias = self.name
        else:
            self.public_id_alias = ''

    def set_uri_type(self):
        """
        Формируем поле URI Type
        Определяется на стороне IMS.
        Может принимать значения ["", 'telUri', 'sipUri']
        Если нет поля, то выставляем "".
        Необязательный параметр.
        """
        choose_uri = ["", "telUri", "sipUri"]
        _uri_type = self._config_ims.get('URI Type')
        if _uri_type is not None:
            if _uri_type not in choose_uri:
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'URI type' should be choose of "
                                          f"({choose_uri}):"
                                          f"\n{self._config_ims}")
            self.uri_type = _uri_type

    def set_hotline_enable(self):
        """
        Формируем поле Hotline Enable.
        Определяется на стороне номера так же как для AGCF.
        Может принимать значения ["none", 'hotd', 'hoti']
        Если нет поля, то выставляем "none".
        Необязательный параметр.
        """
        choose_hotline_ = ["none", 'hotd', 'hoti']
        _hot = self._number.hotline
        if _hot is None:
            self.hotline_enable = 'none'
        else:
            if _hot not in choose_hotline_:
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Hotline Enable' should be choose"
                                          f" of ({choose_hotline_}):{_hot}")
            self.hotline_enable = _hot

    def set_msn(self):
        """
        Формируем поле Set as MSN Number.
        Определяется на стороне номера.
        Может принимать значения ["", 'no, 'yes'].
        Если нет поля, то выставляем "".
        Необязательный параметр.
        """
        choose_msn = ["", "no", "yes"]
        _msn = self._number.msn
        if _msn is not None:
            if _msn not in choose_msn:
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Set as MSN Number' should be"
                                          f" choose of ({choose_msn}):{_msn}")
            self.msn = _msn

    def configure_public_iirs(self):
        """
        Конфигурируем IMS Public Identities from implicit registration set
        """
        # self.set_public_id_alias()
        self.set_uri_type()
        self.set_hotline_enable()
        self.set_msn()

# ############################### TAS #########################################

    def set_tas_node(self):
        """
        Формируем поле TAS Node.
        Определяется на стороне IMS.
        Значение должено быть представлено числом в строковом формате.
        Обязательный параметр.
        """
        _tas_node = self._config_ims.get("TAS Node")
        if _tas_node is None:
            raise MigrateElementError(f"Not found attribute with name "
                                      f"'TAS Node' or contains is None:"
                                      f"\n{self._config_ims}")
        if not isinstance(_tas_node, str):
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'TAS Node' should be type is string:"
                                      f"\n{self._config_ims}")
        if not _tas_node.isdigit():
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'TAS Node' should be consist of "
                                      f"digits:\n{self._config_ims}")
        self.tas_node = _tas_node

    def set_tas_alias(self):
        """
        Формируем поле TAS Public Id Alias.

        * Обязательный параметр
        * вычисляемое значение.
        """
        if self.name is None:
            raise MigrateElementError(f"Not found attribute with name 'Name *'"
                                      f" or contains is None in "
                                      f"'IMS User Subscription':'{self.name}'")
        self.tas_alias = f"sip:{self.name}@{self.domain}"

    def set_supl_serv_set(self):
        """
        Формируем поле Supplementary Service Set
        * Определено на стороне Абонента.
        * Значение должено быть представлено числом в строковом формате.
        * Если такого поля нет, то по дефолту выставляем: "902".
        * Oбязательный параметр.
        """
        _suppl_set = self._number.service_set
        if _suppl_set not in ["-1"]:
            if _suppl_set is None:
                raise MigrateElementError(f"Not found attribute with name "
                                          f"'Supplementary Service Set' or"
                                          f" contains is None:'{_suppl_set}'")
            if not isinstance(_suppl_set, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Supplementary Service Set' should"
                                          f" be type is string:'{_suppl_set}'")
            if not _suppl_set.isdigit():
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Supplementary Service Set' "
                                          f"should be consist of digits:'"
                                          f"{_suppl_set}'")
        self.supl_serv_set = _suppl_set

    def set_concurent_session(self):
        """
        Формируем поле Concurrent Sessions.
        Определяется на стороне номера.
        Допустимы значения: ['1', '2', '30']
        Значение должено быть представлено числом в строковом формате.
        """
        choose_concurent = ['1', '2', '30']
        _concurent = self._number.concurent_sessions
        if _concurent is None:
            raise MigrateElementError(f"Not found attribute with name "
                                      f"'Concurrent Sessions' or contains is"
                                      f" None:'{_concurent}'")
        if not isinstance(_concurent, str):
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'Concurrent Sessions' should be type"
                                      f" is string:'{_concurent}'")

        if _concurent not in choose_concurent:
            raise MigrateElementError(f"Inconsistent data in "
                                      f"'Concurrent session' "
                                      f"({choose_concurent}):"
                                      f"'{_concurent}'")
        self.concurent_session = _concurent

    def set_license_type(self):
        """
        Формируем поле License Type\*.
        Определяется на стороне номера.
        Допустимы значения:
        ['basicLicense', 'standardLicense', 'advancedLicense']
        """
        _lic_type = ['basicLicense', 'standardLicense', 'advancedLicense']
        _subs_lic = self._number.license
        if _subs_lic is None:
            raise MigrateElementError(f"Not found attribute with name "
                                      f"'License Type*' or contains is"
                                      f" None:'{_subs_lic}'")
        if not isinstance(_subs_lic, str):
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'License Type*' should be type"
                                      f" is string:'{_subs_lic}'")
        if _subs_lic not in _lic_type:
            raise MigrateElementError(f"Inconsistent data 'License Type*:dn'"
                                      f"in ({_lic_type}):"
                                      f"'{_subs_lic}'")
        self.license = _subs_lic

    def set_subscriber_category(self):
        """
        Формируем поле Subscriber Category.
        * Определяется на стороне номера.
        * Значение должено быть представлено числом в строковом формате.
        * Обязательный параметр
        """
        _subs_category = self._number.category
        if _subs_category is None:
            raise MigrateElementError(f"Not found attribute with name "
                                      f"'Subscriber Category' or contains is"
                                      f" None:'{_subs_category}'")
        if not isinstance(_subs_category, str):
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'Subscriber Category' should be type"
                                      f" is string:'{_subs_category}'")
        if not _subs_category.isdigit():
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'Subscriber Category' should be "
                                      f"consist digits:'{_subs_category}'")
        self.subscriber_category = _subs_category

    def set_m_sip_profile_class(self):
        """
        Формируем поле m.SipProfile.class.
        * Определяется на стороне номера.
        * Значение должено быть представлено числом в строковом формате.
        * Обязательный параметр, по дефолту ставим '1'
        """
        _mSipProfile = self._number.m_sip_profile
        if _mSipProfile is None:
            raise MigrateElementError(f"Not found attribute with name "
                                      f"'m.SipProfile.class' or contains "
                                      f"is None:'{_mSipProfile}'")
        if not isinstance(_mSipProfile, str):
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'m.SipProfile.class' should be type is"
                                      f" string:'{_mSipProfile}'")
        if not _mSipProfile.isdigit():
            raise MigrateElementError(f"Inconsistent data, the type "
                                      f"'m.SipProfile.class' should be consist"
                                      f" of digits:'{_mSipProfile}'")
        self.m_sip_profile_class = _mSipProfile

    def set_business_group(self):
        """
        Формируем поле Business Group.
        * Определяется на стороне номера.
        * Значение должено быть представлено числом в строковом формате.
        * Небязательный параметр, по дефолту ставим ''
        """
        _bus_group = self._number.business_group
        if _bus_group is not None:
            if not isinstance(_bus_group, str):
                raise MigrateElementError(f"Inconsistent data, the type "
                                          f"'Business Group' should be type is"
                                          f" string:'{_bus_group}'")
            if _bus_group not in [""]:
                if not _bus_group.isdigit():
                    raise MigrateElementError(f"Inconsistent data, the type "
                                              f"'Business Group' should be"
                                              f" consist of digits:"
                                              f"'{_bus_group}'")
                self.business_group = _bus_group

    def set_custom_servise_set(self):
        if self.supl_serv_set in "-1":
            self.custom_serv_set = str(self._number.custom_service_set)

    def configure_tas(self):
        """ Конфигурируем TAS 'Telephony Application Server
        """
        self.set_tas_node()
        # self.set_tas_alias()
        self.set_supl_serv_set()
        self.set_concurent_session()
        self.set_license_type()
        self.set_subscriber_category()
        self.set_m_sip_profile_class()
        self.set_business_group()
        self.set_custom_servise_set()

# ################ Additional parameters needed  for migration ###########################

    def set_ngn_interface(self):
        """
        Формируем поле NGN Interface \*.
        * Копирует поле Interface \*.
        """
        self.set_interface('ngn_interface')

    def set_ngn_access(self):
        """
        Формируем поле NGN Access \*.
        * Копирует поле Access \*.
        """
        self.set_access('ngn_access')

    def set_ngn_access_var(self):
        """
        Формируем поле NGN Access Variant \*.
        * Копирует поле Access Variant \*.
        """
        self.set_access_variant('ngn_access_var')

    def set_ngn_rtp_profile(self):
        """
        Формируем поле NGN RTP Profile \*.
        * Копирует поле RTP Profile \*.
        """
        self.set_rtp_profile('ngn_rtp_profile')

    def set_time_zone(self):
        """
        Обрабатываем поле Time Zone.
        Определяется на стороне IMS.
        Значение должено быть представлено числом в строковом формате.
        Необязательный параметр.

        Значение None или '' передаем как ''(пустая строка).
        """
        _time_zone = self._config_ims.get("Time Zone", '') or ''

        if _time_zone == 'delete':
            self.time_zone = _time_zone
            return

        if _time_zone in [""]:
            log_wp.info(f"DN: {self.name} The 'Time Zone' is not defined in config IMS")
            return

        if not isinstance(_time_zone, str):
                raise MigrateElementError(f"DN: {self.name} Inconsistent data, the type "
                                          f"'Time Zone' should be type is"
                                          f" string:'{_time_zone}'")

        if not _time_zone.isdigit():
            raise MigrateElementError(f"DN: {self.name} Inconsistent data, the"
                                      f" type 'Time Zone' should be"
                                      f" consist of digits:"
                                      f"'{_time_zone}'")
        self.time_zone = _time_zone

    def set_geo_area(self):
        """
        Обрабатываем поле Geographical Area.
        Определяется на стороне IMS.
        Значение должено быть представлено числом в строковом формате.
        Необязательный параметр.

        Значение None или '' передаем как ''(пустая строка).
        """
        _geo_area = self._config_ims.get("Geographical Area", '') or ''

        if _geo_area == 'delete':
            self.geo_area = _geo_area
            return

        if _geo_area in [""]:
            log_wp.info(f"DN: {self.name} The 'Geographical Area' is not defined in config IMS")
            return

        if not isinstance(_geo_area, str):
                raise MigrateElementError(f"DN: {self.name} Inconsistent data,"
                                          f" the type 'Geographical Area'"
                                          f" should be type is string:'{_geo_area}'")

        if not _geo_area.isdigit():
            raise MigrateElementError(f"DN: {self.name} Inconsistent data,"
                                      f" the type 'Geographical Area' should"
                                      f" be consist of digits:"
                                      f"'{_geo_area}'")
        self.geo_area = _geo_area

    def configure_ngn(self, node='False'):
        if self._number.type_dn == 'pstn':
            self.set_ngn_interface()
            self.set_ngn_access()
            self.set_ngn_access_var()
            self.set_ngn_rtp_profile()
        self.set_time_zone()
        self.set_geo_area()

# ################ Create Import Data to Web Portal ###########################

    def greate_import_wp(self, node=False):
        self.configure_subcription()
        self.configure_private_user()
        self.configure_public_user()
        self.configure_agcf(node=node)
        self.configure_public_iirs()
        self.configure_tas()
        self.configure_ngn(node=node)
        self.del_key_by_val(self._template_ims)
        return self._template_ims, self.set_identity_public(impu=True)
