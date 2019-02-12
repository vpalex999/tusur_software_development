
import pytest
from unittest import mock
from sources.repository.mockrepository import MockRepo


@pytest.fixture
def config():
    config = mock.Mock()
    config.source_file_db = 'data/node_test/data/ATC_MAKET.xlsx'
    return config


@pytest.fixture
def node(config):
    return MockRepo(config)


def test_init_mock_repo(config):

    node = MockRepo(config)

    assert isinstance(node, MockRepo)


def test_parce_node_repo(node):

    node.execute()

    assert node.list()[0].dn == '6873639'

