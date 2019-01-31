
import pytest
from sources.domain.custom_service_set import CustomServiceSet
        

def test_init_service(mapping_service):
    """ Проверка инициализации """

    custom = CustomServiceSet()

    assert isinstance(custom, CustomServiceSet)


def test_get_custom_service_ser_from_dict():

    custom = CustomServiceSet()

    res = custom()

    assert len(res) == 43
