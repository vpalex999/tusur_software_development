import json
import copy
import logging
from sources.domain.errors import *
from utilites.base_64 import B64


log_wp = logging.getLogger("migrate.web_portal")


class WpDN(object):

    _ims = json.load(open('templates/template_web_portal.json'))

    def __init__(self, number, config):
        self.number = number
        self.config = config
        self.ims = config.ims
        self.subscriber_dict = copy.deepcopy(self._ims)

    def __getattr__(self, value):
        return getattr(self.number, value)

    def __call__(self):
        self.make()
        return self.subscriber_dict

# ######################### IMS User Subscription #############################

    def configure_subcription(self):
        """ Конфигурируем поля IMS User Subscription """
        self.set_number()
        self.set_capabilities()
        self.set_preferred()
        return True

    def set_number(self):
        """
        Формирует поле Name *::

           - Value is calculated based on defined DN, NDC and CC data from NGN

        * Обязательный параметр.
        """
        if self.dn is None:
            raise MigrateError(f"Attribute with name 'DN' "
                               f"contains is None:{self.dn}")
        if not isinstance(self.dn, str):
            raise MigrateError(f"Inconsistent type: 'DN' "
                               f"should be type is string:"
                               f"{self.dn}")
        if self.dn in [""]:
            raise MigrateError(f"'Create field Name *'. Attribute with "
                               f"name 'DN' is Empty:{self.dn}")
        else:
            result_name = f"+{getattr(self.ims, 'NDC')}{self.dn}"
            if len(result_name) == 12 and result_name.startswith('+7'):
                self.subscriber_dict["IMS User Subscription"]["Name *"] = result_name
            else:
                raise MigrateError(f"DN has wrong format: NDC. "
                                   f"in the NDC should be included "
                                   f"the firts digit '7' "
                                   f"if DN has not it."
                                   f"format NDC + digits of DN: "
                                   f"{getattr(self.ims, 'NDC')}:{self.dn}")

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
        capabilities = getattr(self.ims, 'Capabilities Set')
        if capabilities is None:
            log_wp.info(f"Not found or got 'null' the label 'Capabilities Set'"
                        f" in '--config_wp' data, so taked data from"
                        f" template_IMS")
        else:
            if not isinstance(capabilities, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Capabilities Set' should be type"
                                   f" of string: {capabilities}")
            if capabilities not in [""]:
                if not capabilities.isdigit():
                    raise MigrateError(f"Inconsistent data, the type "
                                       f"'Capabilities Set' should be"
                                       f" of digits: {capabilities}")

                self.subscriber_dict["IMS User Subscription"]["Capabilities Set"] = capabilities

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
        preferred = getattr(self.ims, 'Preferred S-CSCF Set')
        if preferred is None:
            log_wp.info(f"Not found or got 'null' the label 'Preferred S-CSCF "
                        f"Set' in '--config_wp' data, so taked data from"
                        f" template_IMS")
        else:
            if not isinstance(preferred, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Preferred S-CSCF Set' should be"
                                   f" type is string: {prefered}")
            if preferred not in [""]:
                if not preferred.isdigit():
                    raise MigrateError(f"Inconsistent data, the type "
                                       f"'Preferred S-CSCF Set' should"
                                       f" be digits:{prefered}")

                self.subscriber_dict["IMS User Subscription"]["Preferred S-CSCF Set"] = preferred

# ############################### IMS Private User Identity ###################

    def configure_private_user(self):
        """Конфигурируем поля IMS Private User Identity """
        # self.set_identity()
        self.set_authorization_schemes()
        self.set_def_auth_scheme()
        self.set_secret_key_k()
        return True

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
        auth_scheme = getattr(self.ims, 'Authorization Schemes')
        if auth_scheme is not None:
            if not isinstance(auth_scheme, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Authorization Schemes' should be"
                                   f" type is string:"
                                   f"{auth_scheme}")
            if auth_scheme not in [""]:
                if not auth_scheme.isdigit():
                    raise MigrateError(f"Inconsistent data, the type "
                                       f"'Authorization Schemes' should"
                                       f" be consist of digits:"
                                       f"{auth_scheme}")
                if int(auth_scheme) < 0 or int(auth_scheme) > 255:
                    raise MigrateError(f"Inconsistent data, the value "
                                       f"'Authorization Schemes' should"
                                       f" be between 0 & 255:"
                                       f"{auth_scheme}")

                self.subscriber_dict['IMS Private User Identity']['Authorization Schemes'] = auth_scheme

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
        def_auth = getattr(self.ims, 'Default Auth. Scheme')
        if def_auth is not None:
            if not isinstance(def_auth, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Default Auth. Scheme' should be "
                                   f"type is string:"
                                   f"{def_auth}")
            if def_auth not in choose_var:
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Default Auth. Scheme' should be "
                                   f"choose of ({choose_var})in "
                                   f"{def_auth}")

            self.subscriber_dict['IMS Private User Identity']['Default Auth. Scheme'] = def_auth

    def set_secret_key_k(self):
        """
        Формируем поле Secret Key K *::

        - SIP password for authentication of SIP terminal to IMS

        * Определяется на стороне номера.
        * Для PSTN абонентов пароль формируется на этапе формирования
          дополнительных данных. Если не указан, то подставляем пороль
          iskratel.
        * Обязательный параметр.
        """
        secret_key = self.password
        if secret_key is None:
            raise MigrateError(f"The password value cannot be None"
                               f"Chek the attribute with name "
                               f"'Secret Key K *' in config_IMS. "
                               f" Source Number: {self.number}")
        if not isinstance(secret_key, str):
            raise MigrateError(f"Inconsistent data. "
                               f"The password should be type is string: "
                               f"Chek the attribute with name "
                               f"'Secret Key K *' in config_IMS. "
                               f" Source Number: {self.number}")
        if secret_key in [""]:
            raise MigrateError(f"Inconsistent data. "
                               f"The password contains is empty string"
                               f"Chek the attribute with name "
                               f"'Secret Key K *' in config_IMS. "
                               f" Source Number: {self.number}")

        secret_key = B64(secret_key)
        self.subscriber_dict['IMS Private User Identity']['Secret Key K *'] = secret_key()

# ############################### IMS Public User Identity ####################

    def configure_public_user(self):
        self.set_type_public()
        self.set_barring()
        self.set_service_profile()
        self.set_charging_info()
        self.set_wildcard_psi()
        self.set_display_name()
        self.set_psi_activation()
        self.set_can_register()
        self.set_allowed_roaming()
        return True

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
        choose_type = ['Public User Identity', 'Distinct PSI',
                       'Wildcarded PSI', ""]
        public_type = getattr(self.ims, 'Type')
        if public_type is not None:
            if not isinstance(public_type, str):
                raise MigrateError(f"Inconsistent data, the type 'Type'"
                                   f" should be type is string:"
                                   f"DN:{self.dn}:{public_type}")
            if public_type not in choose_type:
                raise MigrateError(f"Inconsistent data, the type 'Type'"
                                   f" should be choose of (choose_type)"
                                   f":DN:{self.dn}:{public_type}:{choose_type}")

            self.subscriber_dict['IMS Public User Identity']['Type'] = public_type

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
        barring = getattr(self.ims, 'Barring')
        if barring is None:
            log_wp.info(f"Not found or got 'null' the label 'Barring' in "
                        f"'--config_wp' data, so taked data from "
                        f"template_IMS: {self.ims}")
        else:
            if not isinstance(barring, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Barring' should be type is "
                                   f"string:{self.ims}")
            if barring not in choose_barring:
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Barring' should be choose of "
                                   f"({choose_barring}):"
                                   f"{self.ims}")

            self.subscriber_dict['IMS Public User Identity']['Barring'] = barring

    def set_service_profile(self):
        """
        Формируем поле 'Service Profile'. Номер профиля TAS сервера.
        Определено на стороне IMS.
        Должен быть заранее создан на HSS.
        Если такого поля нет, то по дефолту выставляем: "".
        Значение должено быть представлено числом в строковом формате.

        - Обязательный параметр.
        """
        s_profile = getattr(self.ims, 'Service Profile')
        if s_profile is None:
            raise MigrateError(f"Not found attribute with name "
                               f"'Service Profile' or contains is None:"
                               f"\n{self.ims}")
        if not isinstance(s_profile, str):
            raise MigrateError(f"Inconsistent data, the type "
                               f"'Service Profile' should be type "
                               f"is string:{self.ims}")
        if not s_profile.isdigit():
            raise MigrateError(f"Inconsistent data, the type "
                               f"'Service Profile' should be consist of"
                               f" digits:{self.ims}")

        self.subscriber_dict['IMS Public User Identity']['Service Profile'] = s_profile

    def set_charging_info(self):
        """
        Формируем поле 'Charging Info'
        Определено на стороне IMS.
        Если такого поля нет, то по дефолту выставляем: "".
        Значение должено быть представлено числом в строковом формате.
        Необязательный параметр.
        """
        charg_info = getattr(self.ims, 'Charging Info')
        if charg_info is not None:
            if not isinstance(charg_info, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Charging Info' should be type "
                                   f"is string:{self.ims}")
            if charg_info not in [""]:
                if not charg_info.isdigit():
                    raise MigrateError(f"Inconsistent data, the type "
                                       f"'Charging Info' should be "
                                       f"consist of digits:"
                                       f"{self.ims}")

                self.subscriber_dict['IMS Public User Identity']['Charging Info'] = charg_info

    def set_wildcard_psi(self):
        """
        Формируем поле 'Wildcard PSI'.
        Определено на стороне IMS.
        Если такого поля нет, то по дефолту выставляем: "".
        Значение должено быть представлено числом в строковом формате
        с максимальным значением знаков: 255.
        Необязательный параметр.
        """
        wildcard = getattr(self.ims, 'Wildcard PSI')
        if wildcard is not None:
            if not isinstance(wildcard, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Wildcard PSI' should be type is "
                                   f"string:{self.ims}")
            if wildcard not in [""]:
                if len(wildcard) > 255:
                    raise MigrateError(f"Inconsistent data, the type "
                                       f"'Wildcard PSI' should be "
                                       f"less 255:{self.ims}")

                self.subscriber_dict['IMS Public User Identity']['Wildcard PSI'] = wildcard

    def set_display_name(self):
        """Формируем поле 'Display Name'.

        * Определяется на стороне IMS.
        * Если такого поля нет, то по дефолту выставляем: "".
        * Значение должено быть представлено в строковом формате.
          с максимальным значением знаков: 255.
        * Необязательный параметр.
        """
        display = getattr(self.ims, "Display Name")
        if display is not None:
            if not isinstance(display, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Display Name' should be type is "
                                   f"string:{self.ims}")
            if display not in [""]:
                if len(display) > 255:
                    raise MigrateError(f"Inconsistent data, the type "
                                       f"Display Name' should be less "
                                       f"255:{self.ims}")

                self.subscriber_dict['IMS Public User Identity']['Display Name'] = display

    def set_psi_activation(self):
        """Формируем поле 'PSI Activation'.
        Определено на стороне IMS.
        Может принимать значения ['no', 'yes', ""]
        Если нет поля, то выставляем ""
        Необязательный параметр.
        """
        choose_psi = ['no', 'yes', ""]
        psi_act = getattr(self.ims, 'PSI Activation')
        if psi_act is not None:
            if psi_act not in choose_psi:
                raise MigrateError(f"Read the incorrect value of "
                                   f"'PSI Activation', it should be set"
                                   f" to {choose_psi}:"
                                   f"{self.ims}")

            self.subscriber_dict['IMS Public User Identity']['PSI Activation'] = psi_act

    def set_can_register(self):
        """
        Формируем поле 'Can Register'.
        Определено на стороне IMS.
        Может принимать значения ['no', 'yes', ""]
        Если нет поля, то выставляем ""
        Необязательный параметр.
        !!! В процедуре миграции, данный параметр выставляется в 'no'
        """
        can_reg = getattr(self.ims, 'Can Register')
        if can_reg is not None:
            if can_reg not in ["no"]:
                raise MigrateError(f"Read the incorrect value, for "
                                   f"Migration this 'Can Register' "
                                   f"should be set to 'no': "
                                   f"{self.ims}")

            self.subscriber_dict['IMS Public User Identity']['Can Register'] = can_reg

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
        roaming = getattr(self.ims, 'Allowed Roaming')
        if roaming is not None:
            if roaming in [""]:
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Allowed Roaming' not should be "
                                   f"type is empty string:"
                                   f"{self.ims}")
            if not isinstance(roaming, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Allowed Roaming' should be type "
                                   f"is string:{self.ims}")
            r = []
            for roam in roaming.split(','):
                if not roam.strip().isdigit():
                    raise MigrateError(f"Inconsistent data, the type "
                                       f"'Allowed Roaming' should be "
                                       f"values is digit:"
                                       f"{self.ims}")
                r.append(roam.strip())

            self.subscriber_dict['IMS Public User Identity']['Allowed Roaming'] = ",".join(r)

# ############################### Access Gateway Control Function #############

    def configure_agcf(self):
        """ Конфигурируем Access Gateway Control Function """
        if self.type_dn == (self.config.PSTN or self.config.ISDN):
            self.set_type_agcf()
            self.set_node_agcf()
            self.set_uri_type_agcf()
            self.set_interface()
            self.set_access()
            self.set_access_variant()
            self.set_rtp_profile()
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

            return True

    def set_type_agcf(self):
        """
        Формируем поле 'Type *'.
        Определяется на стороне номера.
        Значение в диапазоне: ['Analog Subscriber', 'ISDN Subscriber', '']
        Если не PSTN номер, то дефолтное значение: "" берётся из шаблона IMS.
        Oбязательный параметр для PSTN.
        """
        choose_type_asterisk = ['Analog Subscriber', 'ISDN Subscriber']
        dict_type_dn = {'PSTN': 'Analog Subscriber', 'ISDN': 'ISDN Subscriber'}

        if dict_type_dn[self.type_dn] not in choose_type_asterisk:
            raise MigrateError(f"Inconsistent data, the type 'Type *' "
                               f"should be choose of "
                               f"({choose_type_asterisk}): "
                               f"{self.type_dn}")

        self.subscriber_dict['Access Gateway Control Function']['Type *'] = dict_type_dn[self.type_dn]

    def set_node_agcf(self):
        """
        Формируем поле 'Node *' - номер AGCF.
        Определено на стороне IMS.
        Значение должено быть представлено числом в строковом формате.
        Если не PSTN номер, то дефолтное значение: "".
        Обязательный параметр для PSTN.
        """
        node_ = getattr(self.ims, 'Node *')
        if node_ is None:
            raise MigrateError(f"Not found attribute with name 'Node *'"
                               f" or contains is None: "
                               f"{self.ims}")
        if not isinstance(node_, str):
            raise MigrateError(f"Inconsistent data, the type 'Node *' "
                               f"should be type is string: "
                               f"{self.ims}")
        if not node_.isdigit():
            raise MigrateError(f"Inconsistent data, the type 'Node *' "
                               f"in AGCF should be consist of digits: "
                               f"{self.ims}")

        self.subscriber_dict['Access Gateway Control Function']['Node *'] = node_

    def set_uri_type_agcf(self):
        """
        Формируем поле URI 'Type *'.
        Определено на стороне IMS.
        Может принимать значения ["", 'telUri', 'sipUri']
        Если нет поля, то выставляем: ""(=telUri).
        Oбязательный параметр для PSTN.
        """
        choose_uri_agcf = ["", 'telUri', 'sipUri']
        uri_ = getattr(self.ims, 'URI Type *')
        if uri_ is None:
            raise MigrateError(f"Not found attribute with name "
                               f"'URI Type *' or contains is None:"
                               f"{self.ims}'")
        if not isinstance(uri_, str):
            raise MigrateError(f"Inconsistent data, the type "
                               f"'URI Type *' should be type is string:"
                               f"{self.ims}'")
        if uri_ not in choose_uri_agcf:
            raise MigrateError(f"Inconsistent data, the type "
                               f"'URI Type *' in AGCF should be consist"
                               f" one of {choose_uri_agcf}:"
                               f"{self.ims}'")

        self.subscriber_dict['Access Gateway Control Function']['URI Type *'] = uri_

    def set_interface(self):
        """
        Формируем поле 'Interface *'.
        Определено на стороне номера.
        Строка должна содержать номер(ID)интерфейса AGCF.
        Обязательный параметр.
        """
        _interface = self.interface
        if _interface is None:
            raise MigrateError(f"Not found attribute with name "
                               f"'Interface *' or contains is None:"
                               f"'{self.number}'")
        if not isinstance(_interface, str):
            raise MigrateError(f"Inconsistent data, the type "
                               f"'Interface *' should be type is "
                               f"string:'{self.number}'")
        if not _interface.isdigit():
            raise MigrateError(f"Inconsistent data, the type "
                               f"'Interface *' in AGCF should be "
                               f"consist of digits:'{self.number}'")

        self.subscriber_dict['Access Gateway Control Function']['Interface *'] = _interface

    def set_access(self):
        """
        Формируем поле 'Access *'.
        Определено на стороне номера.
        Строка должна содержать номер(ID) порта в интерфейсе на AGCF .
        Обязательный параметр.
        """
        _access = self.access
        if _access is None:
            raise MigrateError(f"Not found attribute with name "
                               f"'Access *' or contains is None:"
                               f"'{self.number}'")
        if not isinstance(_access, str):
            raise MigrateError(f"Inconsistent data, the type 'Access *'"
                               f" should be type is string:"
                               f"'{self.number}'")
        if not _access.isdigit():
            raise MigrateError(f"DN {self.dn}: Inconsistent data, the type 'Access *'"
                               f" in AGCF should be consist of digits:"
                               f"'{self.number}'")

        self.subscriber_dict['Access Gateway Control Function']['Access *'] = _access

    def set_access_variant(self):
        """
        Формируем поле Access 'Variant *'.

        * Определяется на стороне IMS.
        * Строка должна содержать номер(ID) варианта порта доступа в AGCF 
          интерфейсе.
        * Используется только для Аналоговых номеров, Для ISDN оставляем "".
        * Значение должено быть представлено числом в строковом формате.
        * Обязательный параметр для PSTN.
        """
        _access_var = getattr(self.ims, 'Access Variant *')
        _type_agcf = self.subscriber_dict['Access Gateway Control Function']['Type *']
        if _access_var is None:
            raise MigrateError(f"Not found attribute with name "
                               f"'Access Variant *' or contains is "
                               f"None:'{_access_var}'")
        if not isinstance(_access_var, str):
            raise MigrateError(f"Inconsistent data, the type "
                               f"'Access Variant *' should be type is "
                               f"string:'{_access_var}'")
        if _type_agcf == 'Analog Subscriber':
            if not _access_var.isdigit():
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Access Variant *' in AGCF should "
                                   f"be consist of digits:"
                                   f"'{_access_var}'")

            self.subscriber_dict['Access Gateway Control Function']['Access Variant *'] = _access_var

        elif _access_var not in [""]:
            raise MigrateError(f"Inconsistent data, the type "
                               f"'Access Variant *' in AGCF should be "
                               f"consist of '':'{_access_var}'")

    def set_rtp_profile(self):
        """
        Формируем поле RTP 'Profile *'.

        * Определяется на стороне IMS?.
        * Строка должна содержать номер(ID) RTP профиля порта доступа в AGCF
          интерфейсе.
        * Используется только для ISDN.
        * Для Аналоговых оставляем: "".
        * Обязательный параметр.
        """
        _rtp_profile = getattr(self.ims, "RTP Profile *")
        _type_agcf = self.subscriber_dict['Access Gateway Control Function']['Type *']

        if _type_agcf == 'ISDN Subscriber':
            if _rtp_profile is None:
                raise MigrateError(f"Not found attribute with name "
                                   f"'RTP Profile *' or contains is None:"
                                   f"'{_rtp_profile}'")
            if not isinstance(_rtp_profile, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'RTP Profile *' should be type is "
                                   f"string:'{_rtp_profile}'")
            if _rtp_profile in [""]:
                raise MigrateError((f"Inconsistent data, the type "
                                    f"'RTP Profile *' in AGCF should be "
                                    f"not empty string for ISDN:"
                                    f"'{_rtp_profile}'"))

            if not _rtp_profile.isdigit():
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'RTP Profile *' in AGCF should be "
                                   f"consist of digits:"
                                   f"'{_rtp_profile}'")

            self.subscriber_dict['Access Gateway Control Function']['RTP Profile *'] =_rtp_profile
        else:
            self.subscriber_dict['Access Gateway Control Function']['RTP Profile *'] = ""

    def set_password(self):
        """
        Формируем поле 'Password *'::

           - Password for IMS user authentication during IMS registration.

        * Копируется с поля: Secret Key K *.
        * Обязательный параметр.
        """
        _password = self.subscriber_dict['IMS Private User Identity']['Secret Key K *']

        if _password is None:
            raise MigrateError(f"Not found attribute with name "
                               f"'Secret Key K *' contains is None in "
                               f"source Number:'{_password}'")
        if not isinstance(_password, str):
            raise MigrateError(f"Inconsistent data, the type "
                               f"'Secret Key K *' contains is empty "
                               f"string in source Number:'{_password}'")
        if _password in "":
            raise MigrateError(f"Inconsistent data, the type "
                               f"'Secret Key K *' contains is empty "
                               f"string in source Number:'{_password}'")

        self.subscriber_dict['Access Gateway Control Function']['Password *'] = _password

    def set_private_id_alias(self):
        """
        Формируем поле 'Private Id Alias'
        Определено на стороне IMS.
        Значение должено быть представлено числом в строковом формате.
        Если нет поля, то выставляем "".
        Необязательный параметр.
        """
        _priv_id_alias = getattr(self.ims, 'Private Id Alias')
        if _priv_id_alias is not None:
            if _priv_id_alias not in [""]:
                if not isinstance(_priv_id_alias, str):
                    raise MigrateError(f"Inconsistent data, the type "
                                       f"'Private Id Alias' should be "
                                       f"type is string:"
                                       f"{self.ims}")
                if not _priv_id_alias.isdigit():
                    raise MigrateError(f"Inconsistent data, the type "
                                       f"'Private Id Alias' in AGCF "
                                       f"should be consist of digits:"
                                       f"{self.ims}")

                self.subscriber_dict['Access Gateway Control Function']['Private Id Alias'] = _priv_id_alias

    def set_embed_teluri(self):
        """
        Формируем поле 'Embed telURI into SIP URI'
        Определено на стороне IMS.
        Значение в диапазоне ['no', 'yes', ""]
        Если нет поля, то выставляем ""(=yes).
        Необязательный параметр.
        """
        choose_embed = ['no', 'yes', ""]
        _embed = getattr(self.ims, 'Embed telURI into SIP URI')
        if _embed is not None:
            if not isinstance(_embed, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Embed telURI into SIP URI' should"
                                   f" be type is string:"
                                   f"{self.ims}")
            if _embed not in choose_embed:
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Type public' should be choose of "
                                   f"({choose_embed}):"
                                   f"{self.ims}")

            self.subscriber_dict['Access Gateway Control Function']['Embed telURI into SIP URI'] = _embed

    def set_dtmf(self):
        """
        Формируем поле 'DTMF Authorization'.
        Определяется на стороне IMS.
        Значение в диапазоне ['no', 'yes', ""]
        Если нет поля, то выставляем ""(=no).
        Необязательный параметр.
        """
        choose_dtmf = ['no', 'yes', ""]
        _dtmf = getattr(self.ims, 'DTMF Authorization')
        if _dtmf is not None:
            if _dtmf not in choose_dtmf:
                raise MigrateError(f"Inconsistent data, the type "
                                          f"'DTMF Authorization' should be "
                                          f"choose of ({choose_dtmf}):"
                                          f"'{_dtmf}'")

            self.subscriber_dict['Access Gateway Control Function']['DTMF Authorization'] = _dtmf

    def set_out_of_service(self):
        """
        Формируем поле 'Out of Service Indication'
        Определяется на стороне номера.
        Значение в диапазоне ['no', 'yes', ""]
        Если нет поля, то выставляем ""(=no).
        Необязательный параметр.
        """
        choose_out = ['no', 'yes', ""]
        _out_of_service = getattr(self.ims, 'Out of Service Indication')

        if _out_of_service is not None:
            if not isinstance(_out_of_service, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Out of Service Indication' should"
                                   f" be type is string:"
                                   f"'{_out_of_service}'")
            if _out_of_service not in choose_out:
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Out of Service Indication' should"
                                   f" be choose of ({choose_out}):"
                                   f"'{_out_of_service}'")

            self.subscriber_dict['Access Gateway Control Function']['Out of Service Indication'] = _out_of_service

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
        _active = getattr(self.ims, 'Active Subscriber')

        if _active is not None:
            if not isinstance(_active, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Active Subscriber' should be type"
                                   f" is string:\n{self.ims}")
            if _active not in choose_active:
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Active Subscriber' should be "
                                   f"choose of ({choose_active}):"
                                   f"{self.ims}")

            self.subscriber_dict['Access Gateway Control Function']['Active Subscriber'] = _active

    def set_initiate_reg_startup(self):
        """
        Формируем поле 'Initiate registration at system startup'.
        Определяется на IMS.
        Значение в диапазоне ['no', 'yes', ""]
        Если нет поля, то выставляем ""(=no).
        Необязательный параметр.
        Для PSTN выставляем "yes'
        """
        choose_startup = ['no', 'yes', ""]
        _init_reg_startup = getattr(self.ims, 'Initiate registration at system startup')

        if _init_reg_startup is not None:
            if not isinstance(_init_reg_startup, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Initiate registration' at system "
                                   f"startup' should be type is string:"
                                   f"'{_init_reg_startup}'")
            if _init_reg_startup not in choose_startup:
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Initiate registration' at system"
                                   f" startup' should be choose of "
                                   f"({choose_startup}):"
                                   f"'{_init_reg_startup}'")

            self.subscriber_dict['Access Gateway Control Function']['Initiate registration at system startup'] = _init_reg_startup

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
        _d_ring_t = getattr(self.ims, 'Display/Ring Type')

        if _d_ring_t is not None:
            if not isinstance(_d_ring_t, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Display/Ring Type' at system "
                                   f"startup' should be type is string:"
                                   f"'{_d_ring_t}'")
            if _d_ring_t not in choose_disp_ring:
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Display/Ring Type' at system "
                                   f"startup' should be choose of "
                                   f"({choose_disp_ring}):"
                                   f"'{_d_ring_t}'")

            self.subscriber_dict['Access Gateway Control Function']['Display/Ring Type'] = _d_ring_t

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
        _in_band = getattr(self.ims, 'In-band Indication Type')
    
        if _in_band is not None:
            if not isinstance(_in_band, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'In-band Indication Type' at "
                                   f"system startup' should be type is "
                                   f"string:'{_in_band}'")
            if _in_band not in choose_inband:
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'In-band Indication Type' at "
                                   f"system startup' should be choose "
                                   f"of ({choose_inband}):"
                                   f"'{_in_band}'")
    
            self.subscriber_dict['Access Gateway Control Function']['In-band Indication Type'] = _in_band

    def set_tariff_origin_code(self):
        """
        Формируем поле 'Tariff Origin Code'.
        Определено на стороне IMS.
        Значение должено быть представлено числом в строковом формате.
        Если нет поля, то выставляем: '1'.
        Необязательный параметр.
        """
        _tariff = getattr(self.ims, 'Tariff Origin Code')

        if _tariff is None:
            _tariff = "1"
        elif _tariff not in ["1"]:
            if not isinstance(_tariff, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Tariff Origin Code' should be "
                                   f"type is string:"
                                   f"{self.ims}")
            if not _tariff.isdigit():
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Tariff Origin Code' in AGCF "
                                   f"should be consist of digits:"
                                   f"{self.ims}")
    
        self.subscriber_dict['Access Gateway Control Function']['Tariff Origin Code'] = _tariff

    def set_standalone_mode(self):
        """
        Формируем поле 'Standalone Mode Calls'.
        Определено на стороне IMS.
        Значение в диапазоне ['no', 'yes', '']
        Если нет поля, то выставляем: ""(=no).
        Необязательный параметр.
        """
        choose_mode = ['no', 'yes', '']
        _standalone = getattr(self.ims, 'Standalone Mode Calls')

        if _standalone is not None:
            if not isinstance(_standalone, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Standalone Mode Calls' should be "
                                   f"type is string:"
                                   f"{self.ims}")
            if _standalone not in choose_mode:
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Standalone Mode Calls' should be"
                                   f" choose of ({choose_mode}):"
                                   f"{self.ims}")

            self.subscriber_dict['Access Gateway Control Function']['Standalone Mode Calls'] = _standalone

    def set_hotline_agcf(self):
        """
        Формируем поле Hotline Enable.
        Определяется на стороне номера.
        Значение в диапазоне ['none', 'hotd', 'hoti']
        Если нет поля, то выставляем: "none".
        Необязательный параметр.
        """
        choose_hotline = ['hotd', 'hoti', 'none']
        _hotline = getattr(self.ims, 'Hotline Enable')

        if _hotline is None:
            _hotline = 'none'
        
        if not isinstance(_hotline, str):
            raise MigrateError(f"Inconsistent data, the type "
                               f"'Hotline Enable' should be type is"
                               f" string:'{_hotline}'")
        if _hotline not in choose_hotline:
            raise MigrateError(f"Inconsistent data, the type "
                               f"'Hotline Enable' should be choose"
                               f" of ({choose_hotline}):"
                               f"'{_hotline}'")

        self.subscriber_dict['Access Gateway Control Function']['Hotline Enable'] = _hotline

# ############# IMS Public Identities from implicit registration set ##########

    def configure_public_iirs(self):
        """
        Конфигурируем IMS Public Identities from implicit registration set
        """
        self.set_uri_type()
        self.set_hotline_enable()
        self.set_msn()

        return True

    def set_uri_type(self):
        """
        Формируем поле URI Type
        Определяется на стороне IMS.
        Может принимать значения ["", 'telUri', 'sipUri']
        Если нет поля, то выставляем "".
        Необязательный параметр.
        """
        choose_uri = ["", "telUri", "sipUri"]
        _uri_type = getattr(self.ims, 'URI Type')

        if _uri_type is not None:
            if _uri_type not in choose_uri:
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'URI type' should be choose of "
                                   f"({choose_uri}):"
                                   f"{self.ims}")
            self.subscriber_dict['IMS Public Identities from implicit registration set']['URI Type'] = _uri_type


    def set_hotline_enable(self):
        """
        Формируем поле Hotline Enable.
        Определяется на стороне номера так же как для AGCF.
        Может принимать значения ["none", 'hotd', 'hoti']
        Если нет поля, то выставляем "none".
        Необязательный параметр.
        """
        choose_hotline_ = ["none", 'hotd', 'hoti']
        _hot = getattr(self.ims, 'Hotline Enable')
    
        if _hot is None:
            _hot = 'none'
        if _hot not in choose_hotline_:
            raise MigrateError(f"Inconsistent data, the type "
                                      f"'Hotline Enable' should be choose"
                                      f" of ({choose_hotline_}):{_hot}")

        self.subscriber_dict['IMS Public Identities from implicit registration set']['Hotline Enable'] = _hot

    def set_msn(self):
        """
        Формируем поле Set as MSN Number.
        Определяется на стороне номера.
        Может принимать значения ["", 'no, 'yes'].
        Если нет поля, то выставляем "".
        Необязательный параметр.
        """
        choose_msn = ["", "no", "yes"]
        _msn = getattr(self.ims, 'Set as MSN Number')

        if _msn is not None:
            if _msn not in choose_msn:
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Set as MSN Number' should be"
                                   f" choose of ({choose_msn}):{_msn}")

            self.subscriber_dict['IMS Public Identities from implicit registration set']['Set as MSN Number'] = _msn

# ############################### TAS #########################################

    def configure_tas(self):
        """ Конфигурируем TAS 'Telephony Application Server """
        self.set_tas_node()
        self.set_supl_serv_set()
        self.set_concurent_session()
        self.set_license_type()
        self.set_subscriber_category()
        self.set_m_sip_profile_class()
        self.set_business_group()
        self.set_custom_servise_set()
        return True

    def set_tas_node(self):
        """
        Формируем поле TAS Node.
        Определяется на стороне IMS.
        Значение должено быть представлено числом в строковом формате.
        Обязательный параметр.
        """
        _tas_node = getattr(self.ims, "TAS Node")

        if _tas_node is None:
            raise MigrateError(f"Not found attribute with name "
                               f"'TAS Node' or contains is None:"
                               f"{self.ims}")
        if not isinstance(_tas_node, str):
            raise MigrateError(f"Inconsistent data, the type "
                               f"'TAS Node' should be type is string:"
                               f"{self.ims}")
        if not _tas_node.isdigit():
            raise MigrateError(f"Inconsistent data, the type "
                               f"'TAS Node' should be consist of "
                               f"digits:{self.ims}")

        self.subscriber_dict['Telephony Application Server']['TAS Node'] = _tas_node

    def set_supl_serv_set(self):
        """
        Формируем поле Supplementary Service Set
        * Определено на стороне Абонента.
        * Значение должено быть представлено числом в строковом формате.
        * Если такого поля нет, то по дефолту выставляем: "902".
        * Oбязательный параметр.
        """
        _suppl_set = self.service_set

        if _suppl_set not in ["-1"]:
            if _suppl_set is None:
                raise MigrateError(f"Not found attribute with name "
                                   f"'Supplementary Service Set' or"
                                   f" contains is None:'{_suppl_set}'")
            if not isinstance(_suppl_set, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Supplementary Service Set' should"
                                   f" be type is string:'{_suppl_set}'")
            if not _suppl_set.isdigit():
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Supplementary Service Set' "
                                   f"should be consist of digits:'"
                                   f"{_suppl_set}'")

        self.subscriber_dict['Telephony Application Server']['Supplementary Service Set'] = _suppl_set

    def set_concurent_session(self):
        """
        Формируем поле Concurrent Sessions.
        Определяется на стороне номера.
        Допустимы значения: ['1', '2', '30']
        Значение должено быть представлено числом в строковом формате.
        """
        choose_concurent = ['1', '2', '30']
        _concurent = getattr(self.ims, 'Concurrent Sessions')

        if _concurent is None:
            raise MigrateError(f"Not found attribute with name "
                               f"'Concurrent Sessions' or contains is"
                               f" None:'{_concurent}'")
        if not isinstance(_concurent, str):
            raise MigrateError(f"Inconsistent data, the type "
                               f"'Concurrent Sessions' should be type"
                               f" is string:'{_concurent}'")
        if _concurent not in choose_concurent:
            raise MigrateError(f"Inconsistent data in "
                               f"'Concurrent session' "
                               f"({choose_concurent}):"
                               f"'{_concurent}'")

        self.subscriber_dict['Telephony Application Server']['Concurrent Sessions'] = _concurent

    def set_license_type(self):
        """
        Формируем поле License Type*.
        Определяется на стороне номера.
        Допустимы значения:
        ['basicLicense', 'standardLicense', 'advancedLicense']
        """
        _lic_type = ['basicLicense', 'standardLicense', 'advancedLicense']
        _subs_lic = getattr(self.ims, 'License Type*')

        if _subs_lic is None:
            raise MigrateError(f"Not found attribute with name "
                               f"'License Type*' or contains is"
                               f" None:'{_subs_lic}'")
        if not isinstance(_subs_lic, str):
            raise MigrateError(f"Inconsistent data, the type "
                               f"'License Type*' should be type"
                               f" is string:'{_subs_lic}'")
        if _subs_lic not in _lic_type:
            raise MigrateError(f"Inconsistent data 'License Type*:dn'"
                               f"in ({_lic_type}):"
                               f"'{_subs_lic}'")

        self.subscriber_dict['Telephony Application Server']['License Type*'] = _subs_lic


    def set_subscriber_category(self):
        """
        Формируем поле Subscriber Category.
        * Определяется на стороне номера.
        * Значение должено быть представлено числом в строковом формате.
        * Обязательный параметр
        """
        if self.category is None:
            raise MigrateError(f"Not found attribute with name "
                               f"'Subscriber Category' or contains is"
                               f" None:'{self.category}'")
        if not isinstance(self.category, str):
            raise MigrateError(f"Inconsistent data, the type "
                               f"'Subscriber Category' should be type"
                               f" is string:'{self.category}'")
        if not self.category.isdigit():
            raise MigrateError(f"Inconsistent data, the type "
                               f"'Subscriber Category' should be "
                               f"consist digits:'{self.category}'")

        self.subscriber_dict['Telephony Application Server']['Subscriber Category'] = self.category

    def set_m_sip_profile_class(self):
        """
        Формируем поле m.SipProfile.class.
        * Определяется на стороне номера.
        * Значение должено быть представлено числом в строковом формате.
        * Обязательный параметр, по дефолту ставим '1'
        """
        _mSipProfile = getattr(self.ims, 'm.SipProfile.class')

        if _mSipProfile is None:
            raise MigrateError(f"Not found attribute with name "
                               f"'m.SipProfile.class' or contains "
                               f"is None:'{_mSipProfile}'")
        if not isinstance(_mSipProfile, str):
            raise MigrateError(f"Inconsistent data, the type "
                               f"'m.SipProfile.class' should be type is"
                               f" string:'{_mSipProfile}'")
        if not _mSipProfile.isdigit():
            raise MigrateError(f"Inconsistent data, the type "
                               f"'m.SipProfile.class' should be consist"
                               f" of digits:'{_mSipProfile}'")

        self.subscriber_dict['Telephony Application Server']['m.SipProfile.class'] = _mSipProfile

    def set_business_group(self):
        """
        Формируем поле Business Group.
        * Определяется на стороне номера.
        * Значение должено быть представлено числом в строковом формате.
        * Небязательный параметр, по дефолту ставим ''
        """
        _bus_group = getattr(self.ims, 'Business Group')

        if _bus_group is not None:
            if not isinstance(_bus_group, str):
                raise MigrateError(f"Inconsistent data, the type "
                                   f"'Business Group' should be type is"
                                   f" string:'{_bus_group}'")
            if _bus_group not in [""]:
                if not _bus_group.isdigit():
                    raise MigrateError(f"Inconsistent data, the type "
                                       f"'Business Group' should be"
                                       f" consist of digits:"
                                       f"'{_bus_group}'")

                self.subscriber_dict['Telephony Application Server']['Business Group'] = _bus_group

    def set_custom_servise_set(self):
        suppl_set= self.subscriber_dict['Telephony Application Server']['Supplementary Service Set']
        if suppl_set in "-1":
            if self.custom_service_set is None:
                raise MigrateError(f"The Custom_Service_Set dont shold be None!")

            self.subscriber_dict['Telephony Application Server']['Custom Service Set'] = str(self.custom_service_set())

# ################ Additional parameters needed  for migration ###########################

    def configure_ngn(self):
        if self.type_dn == (self.config.PSTN or self.config.ISDN):
            self.set_ngn_interface()
            self.set_ngn_access()
            self.set_ngn_access_var()
            self.set_ngn_rtp_profile()
        self.set_time_zone()
        self.set_geo_area()

        return True

    def set_ngn_interface(self):
        """
        Формируем поле NGN Interface *.
        * Копирует поле Interface *.
        """
        _interface = self.subscriber_dict['Access Gateway Control Function']['Interface *']

        self.subscriber_dict['Additional parameters needed  for migration']['NGN Interface *'] = _interface

    def set_ngn_access(self):
        """
        Формируем поле NGN Access *.
        * Копирует поле Access *.
        """
        _access = self.subscriber_dict['Access Gateway Control Function']['Access *']

        self.subscriber_dict['Additional parameters needed  for migration']['NGN Access *'] = _access

    def set_ngn_access_var(self):
        """
        Формируем поле NGN Access Variant *.
        * Копирует поле Access Variant *.
        """
        _a_variant = self.subscriber_dict['Access Gateway Control Function']['Access Variant *']

        self.subscriber_dict['Additional parameters needed  for migration']['NGN Access Variant *'] = _a_variant

    def set_ngn_rtp_profile(self):
        """
        Формируем поле NGN RTP Profile *.
        * Копирует поле RTP Profile *.
        """
        _rtp_prof = self.subscriber_dict['Access Gateway Control Function']['RTP Profile *']

        self.subscriber_dict['Additional parameters needed  for migration']['NGN RTP Profile *'] = _rtp_prof

    def set_time_zone(self):
        """
        Обрабатываем поле Time Zone.
        Определяется на стороне IMS.
        Значение должено быть представлено числом в строковом формате.
        Необязательный параметр.

        Значение None или '' передаем как ''(пустая строка).
        """
        _time_zone = getattr(self.ims, "Time Zone", '')

        if _time_zone == 'delete':
            self.subscriber_dict['Additional parameters needed  for migration']['Time Zone'] = _time_zone
            return

        if _time_zone in [""]:
            log_wp.info(f"DN: {self.dn} The 'Time Zone' is not defined in config IMS")
            return

        if not isinstance(_time_zone, str):
                raise MigrateError(f"DN: {self.dn} Inconsistent data, the type "
                                   f"'Time Zone' should be type is"
                                   f" string:'{_time_zone}'")

        if not _time_zone.isdigit():
            raise MigrateError(f"DN: {self.dn} Inconsistent data, the"
                               f" type 'Time Zone' should be"
                               f" consist of digits:"
                               f"'{_time_zone}'")

        self.subscriber_dict['Additional parameters needed  for migration']['Time Zone'] = _time_zone

    def set_geo_area(self):
        """
        Обрабатываем поле Geographical Area.
        Определяется на стороне IMS.
        Значение должено быть представлено числом в строковом формате.
        Необязательный параметр.

        Значение None или '' передаем как ''(пустая строка).
        """
        _geo_area = getattr(self.ims, "Geographical Area", '')

        if _geo_area == 'delete':
            self.subscriber_dict['Additional parameters needed  for migration']['Geographical Area'] = _geo_area
            return

        if _geo_area in [""]:
            log_wp.info(f"DN: {self.dn} The 'Geographical Area' is not defined in config IMS")
            return

        if not isinstance(_geo_area, str):
                raise MigrateError(f"DN: {self.dn} Inconsistent data,"
                                   f" the type 'Geographical Area'"
                                   f" should be type is string:'{_geo_area}'")

        if not _geo_area.isdigit():
            raise MigrateError(f"DN: {self.dn} Inconsistent data,"
                               f" the type 'Geographical Area' should"
                               f" be consist of digits:"
                               f"'{_geo_area}'")

        self.subscriber_dict['Additional parameters needed  for migration']['Geographical Area'] = _geo_area

# #####################################################################################

    @staticmethod
    def del_key_by_val(dict_in):
        """ Удаление ключа в словаре по значению ключа - 'delete' """
        list_of_delete = ['delete']
        list_key = dict_in.keys()
        for k in list(list_key):
            if dict_in[k] in list_of_delete:
                del dict_in[k]
            elif isinstance(dict_in[k], dict):
                WpDN.del_key_by_val(dict_in[k])

    # ################ Create Import Data to Web Portal ###########################

    def make(self):
        """ Формирует словарь IMS по данным из атрибутов номера и шаблона конфигурации IMS """
        self.configure_subcription()
        self.configure_private_user()
        self.configure_public_user()
        self.configure_agcf()
        self.configure_public_iirs()
        self.configure_tas()
        self.configure_ngn()
        self.del_key_by_val(self.subscriber_dict)

        return True

# ########## Property ##########
