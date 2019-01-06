from sources.config import Config


def test_init_object_Config():

    config = Config()

    assert config.source_db == []
    assert config.type_dn == 'sip'
    assert config.cli is None
