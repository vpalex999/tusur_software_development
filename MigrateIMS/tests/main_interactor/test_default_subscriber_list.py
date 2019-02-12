import pytest
from unittest import mock

from sources.domain.defaultsubscriber import DefaultSubscriber as DSubs
from sources.shared.main_interactor import MainInteractor
from sources.repository.imsrepository import ImsSubsRepo


@pytest.fixture
def def_subs_repo():
    def_subs1 = DSubs('3436873639')
    def_subs2 = DSubs('3436873640')
    def_subs3 = DSubs('3436873641')

    return ImsSubsRepo([def_subs1, def_subs2, def_subs3])


@pytest.fixture
def node_subs_repo():
    return ImsSubsRepo()


def test_defaultsubscriber_list(def_subs_repo, node_subs_repo):

    repo = mock.Mock()
    repo.list.return_value = def_subs_repo
    config = mock.Mock()

    m_interactor = MainInteractor(repo, node_subs_repo, config)
    result = m_interactor.execute()

    repo.list.assert_called_once_with()

    assert result == def_subs_repo
