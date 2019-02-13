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
    node_subs.list_dn_options = ["RVA"]

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


def test_defaultsubscriber_list(repo_def_subs, repo_node_subs, mapping_ims, mapping_category, mapping_service):

    config = Config(node="AXE-10", type_dn="OTHER")
    config.ims = IMS(mapping_ims)
    config.category = Category(mapping_category)
    config.service = Service(mapping_service)

    m_interactor = MainInteractor(repo_def_subs, repo_node_subs, config)
    m_interactor.make_subscribers()

    assert repo_def_subs.list()[0] == DSubs('3436873639')
    assert len(repo_def_subs.list()) == 1
