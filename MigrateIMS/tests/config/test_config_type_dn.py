import pytest
from sources.config.config import Config


def test_set_type_sip():
    config = Config()

    assert config.type_dn == 'sip'


def test_set_type_pstn():
    config = Config(type_dn='pstn')

    assert config.type_dn == 'pstn'


def test_set_type_all():
    config = Config(type_dn='other')

    assert config.type_dn == 'other'


def test_check_type_dn_ok():
    config = Config()

    assert config.check_type_dn() is None


def test_check_type_dn_wrong():
    config = Config(type_dn='wrong')
    with pytest.raises(Exception):
        config.check_type_dn()
