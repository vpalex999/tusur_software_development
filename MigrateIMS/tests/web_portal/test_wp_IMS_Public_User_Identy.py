""" Тесты для обработчика данных номера в формат импорта на WEB PORTAL"""
import pytest
from unittest import mock
from sources.domain.defaultsubscriber import DefaultSubscriber as DS
from sources.domain.ims import IMS
from sources.domain.wp import WpDN
from sources.domain.errors import MigrateError


@pytest.fixture
def config(mapping_ims):
    config = mock.Mock()
    config.ims = IMS(mapping_ims)
    return config


@pytest.fixture
def wp(config):
    subs = DS(dn='6873639', password="iskratel")
    return WpDN(subs, config)


def test_configure_public_user(wp):

    assert wp.configure_public_user() is True


def test_set_type_public(wp):
    setattr(wp.ims, 'Type', 'Public User Identity')

    wp.set_type_public()
    assert wp.subscriber_dict['IMS Public User Identity']['Type'] == 'Public User Identity'


def test_set_type_public_is_None(wp):

    setattr(wp.ims, 'Type', None)

    wp.set_type_public()
    assert wp.subscriber_dict['IMS Public User Identity']['Type'] == ''


def test_set_type_public_is_not_String(wp):
    setattr(wp.ims, 'Type', 123)

    with pytest.raises(MigrateError):
        wp.set_type_public()


def test_set_type_public_is_not_Choosen(wp):
    setattr(wp.ims, 'Type', "ABC")

    with pytest.raises(MigrateError):
        wp.set_type_public()


def test_set_barring(wp):

    wp.set_barring()
    assert wp.subscriber_dict['IMS Public User Identity']['Barring'] == 'no'


def test_set_barring_is_None(wp):

    setattr(wp.ims, "Barring", None)

    wp.set_barring()
    assert wp.subscriber_dict['IMS Public User Identity']['Barring'] == ''


def test_set_barring_is_not_String(wp):

    setattr(wp.ims, "Barring", 123)

    with pytest.raises(MigrateError):
        wp.set_barring()


def test_set_barring_is_not_Chosen(wp):

    setattr(wp.ims, "Barring", '127')

    with pytest.raises(MigrateError):
        wp.set_barring()


def test_set_service_profile(wp):

    wp.set_service_profile()

    assert wp.subscriber_dict['IMS Public User Identity']['Service Profile'] == '1'


def test_set_service_profile_is_None(wp):

    setattr(wp.ims, "Service Profile", None)

    with pytest.raises(MigrateError):
        wp.set_service_profile()


def test_set_service_profile_is_not_String(wp):

    setattr(wp.ims, "Service Profile", 123)

    with pytest.raises(MigrateError):
        wp.set_service_profile()


def test_set_service_profile_is_not_Digits(wp):

    setattr(wp.ims, "Service Profile", 'ABC')

    with pytest.raises(MigrateError):
        wp.set_service_profile()


def test_set_charging_info(wp):

    wp.set_charging_info()
    assert wp.subscriber_dict['IMS Public User Identity']['Charging Info'] == '2'


def test_set_charging_info_is_None(wp):

    setattr(wp.ims, "Charging Info", None)

    wp.set_charging_info()
    assert wp.subscriber_dict['IMS Public User Identity']['Charging Info'] == ''


def test_set_charging_info_is_not_String(wp):

    setattr(wp.ims, "Charging Info", 123)

    with pytest.raises(MigrateError):
        wp.set_charging_info()


def test_set_charging_info_is_not_Digits(wp):

    setattr(wp.ims, "Charging Info", 'ABC')

    with pytest.raises(MigrateError):
        wp.set_charging_info()


def test_set_wildcard_psi(wp):

    wp.set_wildcard_psi()
    assert wp.subscriber_dict['IMS Public User Identity']['Wildcard PSI'] == 'wildcard'


def test_set_wildcard_psi_is_None(wp):

    setattr(wp.ims, "Wildcard PSI", None)

    wp.set_wildcard_psi()
    assert wp.subscriber_dict['IMS Public User Identity']['Wildcard PSI'] == ''


def test_set_wildcard_psi_is_not_String(wp):

    setattr(wp.ims, "Wildcard PSI", 123)

    with pytest.raises(MigrateError):
        wp.set_wildcard_psi()


def test_set_wildcard_psi_is_more_255(wp):

    setattr(wp.ims, "Wildcard PSI", ''.join([str(1) for i in range(256)]))

    with pytest.raises(MigrateError):
        wp.set_wildcard_psi()


def test_set_display_name(wp):

    wp.set_display_name()
    assert wp.subscriber_dict['IMS Public User Identity']['Display Name'] == 'Vacya'


def test_set_display_name_is_None(wp):

    setattr(wp.ims, "Display Name", None)

    wp.set_display_name()
    assert wp.subscriber_dict['IMS Public User Identity']['Display Name'] == ''


def test_set_display_name_is_not_String(wp):

    setattr(wp.ims, "Display Name", 123)

    with pytest.raises(MigrateError):
        wp.set_display_name()


def test_set_display_name_is_more_255(wp):

    setattr(wp.ims, "Display Name", ''.join([str(1) for i in range(256)]))

    with pytest.raises(MigrateError):
        wp.set_display_name()


def test_set_psi_activation(wp):

    wp.set_psi_activation()
    assert wp.subscriber_dict['IMS Public User Identity']['PSI Activation'] == 'yes'


def test_set_psi_activation_is_None(wp):

    setattr(wp.ims, "PSI Activation", None)

    wp.set_psi_activation()
    assert wp.subscriber_dict['IMS Public User Identity']['PSI Activation'] == ''


def test_set_psi_activation_is_not_Chosen(wp):

    setattr(wp.ims, "PSI Activation", '127')

    with pytest.raises(MigrateError):
        wp.set_psi_activation()


def test_set_can_register(wp):

    wp.set_can_register()
    assert wp.subscriber_dict['IMS Public User Identity']['Can Register'] == 'no'


def test_set_can_register_is_None(wp):

    setattr(wp.ims, "Can Register", None)

    wp.set_can_register()
    assert wp.subscriber_dict['IMS Public User Identity']['Can Register'] == 'no'


def test_set_can_register_is_Yes(wp):

    setattr(wp.ims, "Can Register", "yes")

    with pytest.raises(MigrateError):
        wp.set_can_register()


def test_set_allowed_roaming(wp):

    wp.set_allowed_roaming()
    assert wp.subscriber_dict['IMS Public User Identity']['Allowed Roaming'] == '1,2'


def test_set_allowed_roaming_is_None(wp):

    setattr(wp.ims, "Allowed Roaming", None)

    wp.set_allowed_roaming()
    assert wp.subscriber_dict['IMS Public User Identity']['Allowed Roaming'] == '1'


def test_set_allowed_roaming_is_empty_String(wp):

    setattr(wp.ims, "Allowed Roaming", "")

    with pytest.raises(MigrateError):
        wp.set_allowed_roaming()


def test_set_allowed_roaming_is_not_String(wp):

    setattr(wp.ims, "Allowed Roaming", 123)

    with pytest.raises(MigrateError):
        wp.set_allowed_roaming()


def test_set_allowed_roaming_is_not_Digits(wp):

    setattr(wp.ims, "Allowed Roaming", '1, a')

    with pytest.raises(MigrateError):
        wp.set_allowed_roaming()
