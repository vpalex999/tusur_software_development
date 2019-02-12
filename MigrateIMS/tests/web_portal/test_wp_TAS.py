""" Тесты для обработчика данных номера в формат импорта на WEB PORTAL"""
import pytest
from unittest import mock
from sources.domain.defaultsubscriber import DefaultSubscriber as DS
from sources.domain.ims import IMS
from sources.domain.wp import WpDN
from sources.domain.errors import MigrateError
from sources.domain.custom_service_set import CustomServiceSet



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
              access='1',
              category='56',
              custom_service_set=CustomServiceSet())
    return WpDN(subs, config)


def test_configure_tas(wp):

    assert wp.configure_tas() is True


def test_set_tas_node(wp):

    setattr(wp.ims, "TAS Node", '7777')

    wp.set_tas_node()

    assert wp.subscriber_dict['Telephony Application Server']['TAS Node'] == '7777'


@pytest.mark.parametrize('tas', [None, 123, 'ABC'])
def test_set_tas_node_is_Wrong(wp, tas):

    setattr(wp.ims, "TAS Node", tas)

    with pytest.raises(MigrateError):
        wp.set_tas_node()


@pytest.mark.parametrize('supl_set', ['901', '-1'])
def test_set_supl_serv_set(wp, supl_set):

    wp.number.service_set = supl_set

    wp.set_supl_serv_set()

    assert wp.subscriber_dict['Telephony Application Server']['Supplementary Service Set'] == supl_set


@pytest.mark.parametrize('supl_set', [None, 123, 'ABC'])
def test_set_supl_serv_set_is_Wrong(wp, supl_set):

    wp.number.service_set = supl_set

    with pytest.raises(MigrateError):
        wp.set_supl_serv_set()


def test_set_concurent_session(wp):

    setattr(wp.ims, 'Concurrent Sessions', '30')

    wp.set_concurent_session()

    assert wp.subscriber_dict['Telephony Application Server']['Concurrent Sessions'] == '30'


@pytest.mark.parametrize('concr', [None, 123, '5'])
def test_set_concurent_session_is_Wrong(wp, concr):

    setattr(wp.ims, 'Concurrent Sessions', concr)

    with pytest.raises(MigrateError):
        wp.set_concurent_session()


def test_set_license_type(wp):

    setattr(wp.ims, 'License Type*', 'basicLicense')

    wp.set_license_type()

    assert wp.subscriber_dict['Telephony Application Server']['License Type*'] == 'basicLicense'


@pytest.mark.parametrize('lic', [None, 123, "wrong"])
def test_set_license_type_is_Wrong(wp, lic):

    setattr(wp.ims, 'License Type*', lic)

    with pytest.raises(MigrateError):
        wp.set_license_type()


def test_set_subscriber_category(wp):

    wp.number.category = '57'

    wp.set_subscriber_category()

    assert wp.subscriber_dict['Telephony Application Server']['Subscriber Category'] == '57'


@pytest.mark.parametrize('cat', [None, 123, 'ABC'])
def test_set_subscriber_category_is_Wrong(wp, cat):

    wp.number.category = cat

    with pytest.raises(MigrateError):
        wp.set_subscriber_category()


def test_set_m_sip_profile_class(wp):

    setattr(wp.ims, 'm.SipProfile.class', '93')

    wp.set_m_sip_profile_class()

    assert wp.subscriber_dict['Telephony Application Server']['m.SipProfile.class'] == '93'


@pytest.mark.parametrize('sip', [None, 123, 'ABC'])
def test_set_m_sip_profile_class_is_Wrong(wp, sip):

    setattr(wp.ims, 'm.SipProfile.class', sip)

    with pytest.raises(MigrateError):
        wp.set_m_sip_profile_class()


@pytest.mark.parametrize('bg, result', [('6', '6'), ("", ""), (None, '')])
def test_set_business_group(wp, bg, result):

    setattr(wp.ims, 'Business Group', bg)

    wp.set_business_group()

    assert wp.subscriber_dict['Telephony Application Server']['Business Group'] == result


@pytest.mark.parametrize('bg', [123, 'ABC'])
def test_set_business_group_is_Wrong(wp, bg):

    setattr(wp.ims, 'Business Group', bg)

    with pytest.raises(MigrateError):
        wp.set_business_group()


def test_set_custom_servise_set(wp):

    wp.subscriber_dict['Telephony Application Server']['Supplementary Service Set'] = '-1'

    wp.set_custom_servise_set()

    assert str(CustomServiceSet()()) ==  wp.subscriber_dict['Telephony Application Server']['Custom Service Set']


def test_set_custom_servise_set_empty(wp):

    wp.subscriber_dict['Telephony Application Server']['Supplementary Service Set'] = '901'

    wp.set_custom_servise_set()

    assert wp.subscriber_dict['Telephony Application Server']['Custom Service Set'] == ""

