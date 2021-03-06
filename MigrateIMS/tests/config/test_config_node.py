import pytest
from sources.config.config import Config


def test_Config_node():

    config = Config()

    assert config.node is None


def test_check_node_ok():

    config = Config(node='DEMO')
    config.check_node()
    assert config.node == 'DEMO'


def test_check_node_not_in_type():

    config = Config()
    with pytest.raises(Exception):
        config.check_node()
