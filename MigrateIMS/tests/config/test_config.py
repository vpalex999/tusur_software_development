from sources.config.config import Config


def test_init_object_Config():

    config = Config()

    assert config.node is None
    assert config.source_db is None
    assert config.source_file_db is None
    assert config.source_dir_db is None
    assert config.set_category is None
    assert config.set_service is None
    assert config.type_dn == 'sip'
    assert config.cli is None
