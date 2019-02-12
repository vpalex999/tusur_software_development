import pytest
from unittest import mock

from sources.config.config import Config
from sources.domain.category import Category
from sources.domain.service import Service
from sources.domain.ims import IMS
from sources.domain.defaultsubscriber import DefaultSubscriber as DSubs
from sources.shared.main_interactor import MainInteractor
from sources.repository.imsrepository import ImsSubsRepo


@pytest.fixture
def def_subs_repo():
    node_subs = mock.Mock()
    node_subs.dn = '3436873639'
    node_subs.password = 'iskratel_test'
    return [node_subs]


@pytest.fixture
def repo_def_subs():
    repo = ImsSubsRepo()
    return repo


@pytest.fixture
def repo_node_subs(def_subs_repo):
    repo = mock.Mock()
    repo.list.return_value = def_subs_repo
    return repo


@pytest.fixture
def config(mapping_ims):
    config = Config(node="AXE-10", type_dn="OTHER")
    config.ims = IMS(mapping_ims)
    return config


def test_main_interactor_get_password(repo_def_subs, repo_node_subs, config):

    m_interactor = MainInteractor(repo_def_subs, repo_node_subs, config)
    password = m_interactor.get_password('iskratel_test')

    assert password == 'iskratel_test'


@pytest.mark.parametrize('pswd', ["", None, 123])
def test_main_interactor_get_password_dn_is_wrong(pswd, repo_def_subs, repo_node_subs, config):

    m_interactor = MainInteractor(repo_def_subs, repo_node_subs, config)
    password = m_interactor.get_password(pswd)

    assert password == 'iskratel'