""" Тесты для обработчика данных номера в формат импорта на WEB PORTAL"""
import pytest
from unittest import mock
from sources.domain.defaultsubscriber import DefaultSubscriber as DS
from sources.domain.ims import IMS
from sources.domain.wp import WpDN


@pytest.fixture
def config(mapping_ims):
    config = mock.Mock()
    config.ims = IMS(mapping_ims)
    return config


@pytest.fixture
def wp(config):
    subs = DS('6873639')
    return WpDN(subs, config)


def test_configure_subcription(wp):

    assert wp.configure_subcription() is True


def test_set_number(wp):

    wp.set_number()
    assert wp.subscriber_dict['IMS User Subscription']["Name *"] == '+73436873639'


def test_set_number_dn_is_None(wp):
    wp.number.dn = None

    with pytest.raises(Exception):
        wp.set_number()


def test_set_number_dn_is_not_String(wp):
    wp.number.dn = 12345

    with pytest.raises(Exception):
        wp.set_number()


def test_set_number_dn_is_empty_String(wp):
    wp.number.dn = ""

    with pytest.raises(Exception):
        wp.set_number()


def test_set_number_dn_has_more_than_12_digits(wp):
    wp.number.dn = "1234567890123"

    with pytest.raises(Exception):
        wp.set_number()


def test_set_number_dn_has_not_7_in_NDC(wp):
    wp.ims.NDC = "2343"

    with pytest.raises(Exception):
        wp.set_number()


def test_set_capabilities(wp):

    wp.set_capabilities()
    assert wp.subscriber_dict['IMS User Subscription']["Capabilities Set"] == '1'


def test_set_capabilities_is_None(wp):

    setattr(wp.ims, "Capabilities Set", None)

    wp.set_capabilities()
    assert wp.subscriber_dict['IMS User Subscription']["Capabilities Set"] == ''


def test_set_capabilities_is_not_String(wp):

    setattr(wp.ims, "Capabilities Set", 123)

    with pytest.raises(Exception):
        wp.set_capabilities()


def test_set_capabilities_is_not_Digits(wp):

    setattr(wp.ims, "Capabilities Set", 'ABC')

    with pytest.raises(Exception):
        wp.set_capabilities()


def test_set_preferred(wp):

    wp.set_preferred()

    assert wp.subscriber_dict['IMS User Subscription']["Preferred S-CSCF Set"] == '2'


def test_set_preferred_is_None(wp):

    setattr(wp.ims, "Preferred S-CSCF Set", None)

    wp.set_preferred()
    assert wp.subscriber_dict['IMS User Subscription']["Preferred S-CSCF Set"] == ''


def test_set_preferred_is_not_String(wp):

    setattr(wp.ims, "Preferred S-CSCF Set", 123)

    with pytest.raises(Exception):
        wp.set_preferred()


def test_set_preferred_is_not_Digits(wp):

    setattr(wp.ims, "Preferred S-CSCF Set", 'ABS')

    with pytest.raises(Exception):
        wp.set_preferred()
