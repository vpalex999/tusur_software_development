from sources.config.config import Config


def test_init_object_Config():

    config = Config()

    assert config.node is None
    assert config.source_db is None
    assert config.source_file_db is None
    assert config.source_dir_db is None
    assert config.mapping_category is None
    assert config.mapping_service is None
    assert config.mapping_ims is None
    assert config.type_dn == 'SIP'

    assert config.category is None
    assert config.service is None
    assert config.ims is None
