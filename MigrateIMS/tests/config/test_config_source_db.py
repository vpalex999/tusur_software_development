import pytest
from sources.config.config import Config


def test_Config_source_db_not_selected():

    config = Config()

    with pytest.raises(Exception):
        config.check_source_db()


def test_Config_select_soure_db_from_file():

    config = Config(sf_db='test_db.txt')

    assert config.check_source_db() is None


def test_Config_select_soure_db_from_dir():

    config = Config(sd_db='test_db')

    assert config.check_source_db() is None
