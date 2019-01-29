
import pytest
from sources.domain.service import Service
        

def test_init_service(mapping_service):
    """ Проверка инициализации """

    service = Service(mapping_service)

    assert isinstance(service, Service)


def test_wrong_set_service_is_not_dict():
    """ use_case_set_service 2.1 """
    with pytest.raises(Exception): 
        Service('wrong')


def test_wrong_set_service_is_not_key_valid_SI():
    """ use_case_set_service 2.2 """
    with pytest.raises(KeyError): 
        Service({"SI_err": []})


def test_set_service_is_empty_list_options():
    """ use_case_set_service 3.1.1 """

    service = Service({"SI": {"RVT": "CFU"}})
    
    assert service([]) == []


def test_get_service_list_options_is_None(mapping_service):
    """ use_case_set_service 3.2.1 """ 

    service = Service(mapping_service)

    assert service(None) == []


def test_get_service_list_options_has_not_service(mapping_service):
    """ use_case_set_service 3.3.1 """ 

    service = Service(mapping_service)

    assert service([""]) == []


def test_set_service_is_empty():
    """ use_case_set_service 4.1.1 """ 

    service = Service({"SI": {}})

    assert service("RVT") == []


def test_set_service_has_not_rules_for_subscriber_options(mapping_service):
    """ use_case_set_service 4.2.1 """ 

    service = Service(mapping_service)

    assert service(["BLA", "BLA", "BLA"]) == []


def test_get_services_singl_key(mapping_service):
    """ use_case_set_service 4 """ 

    service = Service(mapping_service)

    assert service(["RVA"]) == ["ACS"]


def test_get_services_many_sing_keys(mapping_service):
    """ use_case_set_service 4 """ 

    service = Service(mapping_service)

    assert service(["tt", "RVT", "RVA", "SR7"]) == ["CFU", "ACS"]


def test_get_service_double_sing_key(mapping_service):
    """ use_case_set_service 4.3.1 """  

    service = Service(mapping_service)

    assert service(["tt", "RVA DOUBLE", "RVA", "SR7"]) == ["DOUBLE", "ACS"]


def test_sort_services_rules(mapping_service):
    
    service = Service(mapping_service)

    res = service.sort_list_rules()
    assert res[0] == ['RVA DOUBLE', ['DOUBLE']]
