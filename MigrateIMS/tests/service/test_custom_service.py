
import pytest
from sources.domain.custom_service_set import CustomServiceSet
        

def test_init_service(mapping_service):
    """ Проверка инициализации """

    custom = CustomServiceSet()

    assert isinstance(custom, CustomServiceSet)


def test_get_custom_service_set_from_dict():

    custom = CustomServiceSet()

    res = custom()

    assert len(res) == 43


def test_custom_service_set_convert_licence():

    custom = CustomServiceSet()
    custom.subsctg = '44'
    custom.make([])

    assert custom.get_id_by_name('basicLicense') == '21'


def test_make_custom_service_set():
    custom = CustomServiceSet()
    custom.make([], category='55', license_type='basicLicense')

    assert custom.subsctg == '55'
    assert custom.licenseType == '21'
