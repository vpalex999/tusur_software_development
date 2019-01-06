from sources.config.config import Config


def test_get_source_db_from_file():

    config = Config()
    config.get_source_file_db()

    assert config.source_file_db is None
