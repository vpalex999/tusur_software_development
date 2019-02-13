import pytest
from sources.domain.ims import IMS


def test_init_IMS(mapping_ims):

    ims = IMS(mapping_ims)

    assert isinstance(ims, IMS)


def test_get_attr_from_IMS(mapping_ims):

    ims = IMS(mapping_ims)

    assert getattr(ims, 'Capabilities Set') == '1'


def test_get_attr_from_IMS_other_key(mapping_ims):

    ims = IMS(mapping_ims)
    with pytest.raises(AttributeError):
        getattr(ims, 'test ims1')
