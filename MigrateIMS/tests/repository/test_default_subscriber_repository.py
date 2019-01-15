import pytest

from sources.domain.defaultsubscriber import DefaultSubscriber as DSubs
from sources.repository.defsubsrepository import DefSubsRepo


@pytest.fixture
def domain_defsubscribers():
    def_subs1 = DSubs('3436873639')
    def_subs2 = DSubs('3436873640')
    def_subs3 = DSubs('3436873641')

    return [def_subs1, def_subs2, def_subs3]


def test_repository_list_without_parameters(domain_defsubscribers):

    repo = DefSubsRepo(domain_defsubscribers)

    assert len(domain_defsubscribers) == len(repo.list())


def test_add_subscriber_to_repository():

    repo = DefSubsRepo()

    assert repo.add(DSubs('1234567')) is True
    assert len(repo.list()) == 1
    assert DSubs('1234567') in repo.list()


def test_add_duplicate_subscriber_to_repository():

    repo = DefSubsRepo()
    repo.add(DSubs('1234567'))

    assert repo.add(DSubs('1234567')) is False
    assert len(repo.list()) == 1
    assert DSubs('1234567') in repo.list()


def test_get_count_repository():

    repo = DefSubsRepo()

    assert len(repo) == 0


def test_get_count_repository_with_item():

    repo = DefSubsRepo()
    repo.add(DSubs('1234567'))

    assert len(repo) == 1


def test_get_subscriber_by_filters_dn():

    repo = DefSubsRepo()
    repo.add(DSubs('1234567'))

    assert repo.list(filters={'dn': '1234567'}) == [DSubs('1234567')]


def test_get_subscriber_by_filters_dn_wrong():

    repo = DefSubsRepo()
    repo.add(DSubs('1234567'))

    assert repo.list(filters={'dn': '1234568'}) == []