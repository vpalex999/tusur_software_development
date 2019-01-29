import pytest
from sources.config.config import Config
from sources.domain.service import Service


def test_set_service(mapping_service):
    config = Config(mapping_service=mapping_service)

    assert config.mapping_service == mapping_service


def test_make_service_obj(mapping_service):
    config = Config(mapping_service=mapping_service)
    config.make_service()

    assert isinstance(config.service, Service)


