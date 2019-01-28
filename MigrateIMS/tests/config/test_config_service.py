import pytest
from sources.config.config import Config
from sources.domain.service import Service


def test_set_service(set_service):
    config = Config(set_service=set_service)

    assert config.set_service == set_service


def test_make_service_obj(set_service):
    config = Config(set_service=set_service)
    config.make_service()

    assert isinstance(config.service, Service)


