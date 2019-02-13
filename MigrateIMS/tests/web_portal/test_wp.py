""" Тесты для обработчика данных номера в формат импорта на WEB PORTAL"""
import pytest
from unittest import mock
from sources.domain.defaultsubscriber import DefaultSubscriber as DS
from sources.domain.ims import IMS
from sources.domain.wp import WpDN
from sources.domain.custom_service_set import CustomServiceSet


@pytest.fixture
def config(mapping_ims):
    config = mock.Mock()
    config.ims = IMS(mapping_ims)
    return config


@pytest.fixture
def wp(config):
    subs = DS(dn='6873639',
              password='iskratel',
              category='56',
              custom_service_set=CustomServiceSet())
    return WpDN(subs, config)


def test_init_wp(wp):

    assert isinstance(wp, WpDN)
    assert wp.number.dn == '6873639'


def test_call_wp_and_return_subscriber_by_dict(wp):

    assert len(wp()) == 7


def test_make_wp_from_source_subscriber(wp):

    assert wp.make() is True
