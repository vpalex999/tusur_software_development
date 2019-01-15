import pytest
from unittest import mock

from sources.domain.defaultsubscriber import DefaultSubscriber as DSubs
from sources.shared.main_interactor import MainInteractor


@pytest.fixture
def domain_defsubscribers():
    def_subs1 = DSubs('3436873639')
    def_subs2 = DSubs('3436873640')
    def_subs3 = DSubs('3436873641')

    return [def_subs1, def_subs2, def_subs3]


def test_defaultsubscriber_list(domain_defsubscribers):

    repo = mock.Mock()
    repo.list.return_value = domain_defsubscribers

    m_interactor = MainInteractor(repo)
    result = m_interactor.execute()

    repo.list.assert_called_once_with()

    assert result == domain_defsubscribers
