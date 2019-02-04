import pytest
from unittest import mock

from sources.domain.defaultsubscriber import DefaultSubscriber as DSubs
from sources.shared.main_interactor import MainInteractor
from sources.repository.defsubsrepository import DefSubsRepo
from sources.domain.service import Service


@pytest.fixture
def def_subs_repo():
    def_subs1 = DSubs('3436873639')
    def_subs2 = DSubs('3436873640')
    def_subs3 = DSubs('3436873641')

    return [def_subs1, def_subs2, def_subs3]


@pytest.fixture
def repo_def_subs():
    repo = DefSubsRepo()
    return repo


@pytest.fixture
def repo_node_subs(def_subs_repo):
    repo = mock.Mock()
    repo.list.return_value = def_subs_repo
    return repo

def test_defaultsubscriber_dn_get_service(repo_def_subs, repo_node_subs, mapping_service):

    config = mock.Mock()
    config.service = Service(mapping_service)

    m_interactor = MainInteractor(repo_def_subs, repo_node_subs, config)
    list_serv = m_interactor.get_services(["DAI"])

    assert list_serv == ['HOLD', 'CW']