import pytest
from sources.config import Config


def test_init_object_Config():

    config = Config({})

    assert config.run_config is None
    assert config.type_sip is None
    assert config.type_pstn is None
    assert config.type_all is None


def test_set_type_sip():
    config = Config({'--sip': True})

    assert config.type_sip is 'sip'
    assert config.type_pstn is None
    assert config.type_all is None


def test_set_type_pstn():
    config = Config({'--pstn': True})

    assert config.type_sip is None
    assert config.type_pstn is 'pstn'
    assert config.type_all is None


def test_set_type_all():
    config = Config({'--all': True})

    assert config.type_sip is None
    assert config.type_pstn is None
    assert config.type_all is 'all'


def test_get_type_sip():
    config = Config({'--sip': True})

    assert config.type_dn == 'sip'


def test_get_type_pstn():
    config = Config({'--pstn': True})

    assert config.type_dn == 'pstn'


def test_get_type_all():
    config = Config({'--all': True})

    assert config.type_dn == 'all'


def test_check_type_ok():
    config = Config({})

    assert config.check_type_dn() is None


def test_check_type_ok_2():
    config = Config({'--sip': True})

    assert config.check_type_dn() is None


def test_check_type_dn_many():
    with pytest.raises(Exception):
        config = Config({'--sip': True, '--pstn': True})
