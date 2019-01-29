import pytest
from sources.config.config import Config
from sources.domain.ims import IMS


def test_set_IMS(mapping_ims):
    config = Config(mapping_ims=mapping_ims)

    assert config.mapping_ims == mapping_ims


def test_make_service_obj(mapping_ims):
    config = Config(mapping_ims=mapping_ims)
    config.make_service()

    assert isinstance(config.ims, IMS)


