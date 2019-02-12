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


def test_configure_ngn(wp):

    assert wp.configure_ngn() is True


def test_set_tas_node(wp):

    setattr(wp.ims, "TAS Node", '7777')

    wp.set_tas_node()

    assert wp.subscriber_dict['Telephony Application Server']['TAS Node'] == '7777'


@pytest.mark.parametrize('tas', [None, 123, 'ABC'])
def test_set_tas_node_is_Wrong(wp, tas):

    setattr(wp.ims, "TAS Node", tas)

    with pytest.raises(MigrateError):
        wp.set_tas_node()


@pytest.mark.parametrize('tz', ['delete', "", "1"])
def test_set_time_zone(wp, tz):

    setattr(wp.ims, "Time Zone", tz)

    wp.set_time_zone()

    assert wp.subscriber_dict['Additional parameters needed  for migration']['Time Zone'] == tz


@pytest.mark.parametrize('tz', [123, 'ABC'])
def test_set_time_zone_is_Wrong(wp, tz):

    setattr(wp.ims, "Time Zone", tz)

    with pytest.raises(MigrateError):
        wp.set_time_zone()


@pytest.mark.parametrize('geo', ['delete', "", "1"])
def test_set_geo_area(wp, geo):

    setattr(wp.ims, "Geographical Area", geo)

    wp.set_geo_area()

    assert wp.subscriber_dict['Additional parameters needed  for migration']['Geographical Area'] == geo


@pytest.mark.parametrize('geo', [123, 'ABC'])
def test_set_geo_area_is_Wrong(wp, geo):

    setattr(wp.ims, "Geographical Area", geo)

    with pytest.raises(MigrateError):
        wp.set_geo_area()