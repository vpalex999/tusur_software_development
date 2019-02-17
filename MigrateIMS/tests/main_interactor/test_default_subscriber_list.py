import pytest

from sources.domain.defaultsubscriber import DefaultSubscriber as DSubs
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
