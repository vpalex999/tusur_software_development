from sources.config import Config


def test_make_Config_from_cli_by_type_dn():

    config = Config.from_cli({'--pstn': True})

    assert config.type_dn == 'pstn'
