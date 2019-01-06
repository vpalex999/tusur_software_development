import pytest
from sources.config import Config


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


def test_get_type_dn_from_cli_sip():

    config = Config(cli={'--sip': True})
    config.parce_type_dn_cli()

    assert config.type_dn == 'sip'


def test_get_type_dn_from_cli_pstn():

    config = Config(cli={'--pstn': True})
    config.parce_type_dn_cli()

    assert config.type_dn == 'pstn'


def test_get_type_dn_from_cli_all():

    config = Config(cli={'--all': True})
    config.parce_type_dn_cli()

    assert config.type_dn == 'other'


def test_get_type_dn_from_cli_empty():

    config = Config(cli={})
    with pytest.raises(Exception):
        config.parce_type_dn_cli()


def test_get_type_dn_from_cli_not():

    config = Config()
    config.parce_type_dn_cli()

    assert config.type_dn == 'sip'


def test_get_type_dn_from_cli_not_type_dn():

    config = Config(cli={'some': True})
    with pytest.raises(Exception):
        config.parce_type_dn_cli()


def test_get_type_dn_from_cli_many_select():

    config = Config(cli={'--pstn': True, '--all': True})
    with pytest.raises(Exception):
        config.parce_type_dn_cli()
