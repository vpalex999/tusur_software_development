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
    config.PSTN = 'PSTN'
    config.ims = IMS(mapping_ims)
    return config


@pytest.fixture
def wp(config):
    subs = DS(dn='6873639',
              password="iskratel",
              type_dn='PSTN',
              interface='1',
              access='1')
    return WpDN(subs, config)


def test_configure_public_iirs(wp):

    assert wp.configure_public_iirs() is True


@pytest.mark.parametrize("uri", ["", 'telUri', 'sipUri'])
def test_set_uri_type(wp, uri):

    setattr(wp.ims, 'URI Type', uri)

    wp.set_uri_type()

    assert wp.subscriber_dict['IMS Public Identities from implicit registration set']['URI Type'] == uri


def test_set_uri_type_is_None(wp):

    setattr(wp.ims, 'URI Type', None)

    wp.set_uri_type()

    assert wp.subscriber_dict['IMS Public Identities from implicit registration set']['URI Type'] == ""


@pytest.mark.parametrize('uri', [123, 'ABC'])
def test_set_uri_type_is_Wrong(wp, uri):

    setattr(wp.ims, 'URI Type', uri)

    with pytest.raises(MigrateError):
        wp.set_uri_type()


@pytest.mark.parametrize('mode, result', [('none', 'none'), ('hotd', 'hotd'), ("hoti", "hoti"), (None, "none")])
def test_set_hotline_enable(wp, mode, result):

    setattr(wp.ims, 'Hotline Enable', mode)

    wp.set_hotline_enable()
    assert wp.subscriber_dict['IMS Public Identities from implicit registration set']['Hotline Enable'] == result


@pytest.mark.parametrize('mode', [123, 'ABC'])
def test_set_hotline_enable_is_Wrong(wp, mode):

    setattr(wp.ims, 'Hotline Enable', mode)

    with pytest.raises(MigrateError):
        wp.set_hotline_enable()


@pytest.mark.parametrize('msn', ["", "no", "yes"])
def test_set_msn(wp, msn):

    setattr(wp.ims, 'Set as MSN Number', msn)

    wp.set_msn()
    assert wp.subscriber_dict['IMS Public Identities from implicit registration set']['Set as MSN Number'] == msn


def test_set_msn_is_None(wp):

    setattr(wp.ims, 'Set as MSN Number', None)

    wp.set_msn()
    assert wp.subscriber_dict['IMS Public Identities from implicit registration set']['Set as MSN Number'] == ""


@pytest.mark.parametrize('msn', [123, "ABC"])
def test_set_msn_is_Wrong(wp, msn):

    setattr(wp.ims, 'Set as MSN Number', msn)

    with pytest.raises(MigrateError):
        wp.set_msn()
