from sources.config import Config


def test_init_object_Config():

    config = Config({})

    assert config.run_config is None
    assert config.type_sip is None
    assert config.type_pstn is None
    assert config.type_all is None
    assert config.source_file_db is None