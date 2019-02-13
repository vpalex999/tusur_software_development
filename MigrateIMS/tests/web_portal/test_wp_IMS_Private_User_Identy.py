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


def test_configure_private_user(wp):

    assert wp.configure_private_user() is True


def test_set_authorization_schemes(wp):

    wp.set_authorization_schemes()
    assert wp.subscriber_dict['IMS Private User Identity']['Authorization Schemes'] == '255'


def test_set_authorization_schemes_is_None(wp):

    setattr(wp.ims, 'Authorization Schemes', None)

    wp.set_authorization_schemes()
    assert wp.subscriber_dict['IMS Private User Identity']['Authorization Schemes'] == ''


def test_set_authorization_schemes_is_not_String(wp):
    setattr(wp.ims, 'Authorization Schemes', 123)

    with pytest.raises(MigrateError):
        wp.set_authorization_schemes()


def test_set_authorization_schemes_is_empty_String(wp):
    setattr(wp.ims, 'Authorization Schemes', "")

    wp.set_authorization_schemes()
    assert wp.subscriber_dict['IMS Private User Identity']['Authorization Schemes'] == ''


def test_set_authorization_schemes_s_not_digits(wp):
    setattr(wp.ims, 'Authorization Schemes', "ABC")

    with pytest.raises(MigrateError):
        wp.set_authorization_schemes()


def test_set_authorization_schemes_less_0(wp):
    setattr(wp.ims, 'Authorization Schemes', "-1")

    with pytest.raises(MigrateError):
        wp.set_authorization_schemes()


def test_set_authorization_schemes_more_255(wp):
    setattr(wp.ims, 'Authorization Schemes', "256")

    with pytest.raises(MigrateError):
        wp.set_authorization_schemes()


def test_set_def_auth_scheme(wp):

    wp.set_def_auth_scheme()
    assert wp.subscriber_dict['IMS Private User Identity']['Default Auth. Scheme'] == '128'


def test_set_def_auth_scheme_is_None(wp):

    setattr(wp.ims, "Default Auth. Scheme", None)

    wp.set_def_auth_scheme()
    assert wp.subscriber_dict['IMS Private User Identity']['Default Auth. Scheme'] == ''


def test_set_def_auth_scheme_is_not_String(wp):

    setattr(wp.ims, "Default Auth. Scheme", 123)

    with pytest.raises(MigrateError):
        wp.set_def_auth_scheme()


def test_set_def_auth_scheme_is_not_Chosen(wp):

    setattr(wp.ims, "Default Auth. Scheme", '127')

    with pytest.raises(MigrateError):
        wp.set_def_auth_scheme()


def test_set_secret_key_k(wp):
    wp.number.password = 'iskratel'
    wp.set_secret_key_k()

    assert wp.subscriber_dict['IMS Private User Identity']['Secret Key K *'] == 'aXNrcmF0ZWw='


def test_set_secret_key_k_is_None(wp):

    wp.number.password = None

    with pytest.raises(MigrateError):
        wp.set_secret_key_k()


def test_set_secret_key_k_is_not_String(wp):

    wp.number.password = 123

    with pytest.raises(MigrateError):
        wp.set_secret_key_k()


def test_set_secret_key_k_is_empty_String(wp):

    wp.number.password = ""

    with pytest.raises(MigrateError):
        wp.set_secret_key_k()
