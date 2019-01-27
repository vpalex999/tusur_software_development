
import pytest
from sources.domain.customservice import CustomServiceSet
        

def test_init_custom_service(set_custom_service):
    """ Проверка инициализации """

    custom_service = CustomServiceSet(set_custom_service)

    assert isinstance(custom_service, CustomServiceSet)


@pytest.mark.skip()
def test_wrong_set_service_is_not_dict():
    """ use_case_set_service 2.1 """
    with pytest.raises(Exception): 
        Service('wrong')


@pytest.mark.skip()
def test_wrong_set_service_is_not_key_valid_SI():
    """ use_case_set_service 2.2 """
    with pytest.raises(KeyError): 
        Service({"SI_err": []})


@pytest.mark.skip()
def test_set_service_is_empty_list_options():
    """ use_case_set_service 3.1.1 """

    service = Service({"SI": {"RVT": "CFU"}})
    
    assert service([]) == []


@pytest.mark.skip()
def test_get_service_list_options_is_None(set_service):
    """ use_case_set_service 3.2.1 """ 

    service = Service(set_service)

    assert service(None) == []


@pytest.mark.skip()
def test_get_service_list_options_has_not_service(set_service):
    """ use_case_set_service 3.3.1 """ 

    service = Service(set_service)

    assert service([""]) == []


@pytest.mark.skip()
def test_set_service_is_empty():
    """ use_case_set_service 4.1.1 """ 

    service = Service({"SI": {}})

    assert service("RVT") == []


@pytest.mark.skip()
def test_set_service_has_not_rules_for_subscriber_options(set_service):
    """ use_case_set_service 4.2.1 """ 

    service = Service(set_service)

    assert service(["BLA", "BLA", "BLA"]) == []


@pytest.mark.skip()
def test_get_services_singl_key(set_service):
    """ use_case_set_service 4 """ 

    service = Service(set_service)

    assert service(["RVA"]) == ["ACS"]


@pytest.mark.skip()
def test_get_services_many_sing_keys(set_service):
    """ use_case_set_service 4 """ 

    service = Service(set_service)

    assert service(["tt", "RVT", "RVA", "SR7"]) == ["CFU", "ACS"]


@pytest.mark.skip()
def test_get_service_double_sing_key(set_service):
    """ use_case_set_service 4.3.1 """  

    service = Service(set_service)

    assert service(["tt", "RVA DOUBLE", "RVA", "SR7"]) == ["DOUBLE", "ACS"]


@pytest.mark.skip()
def test_sort_services_rules(set_service):
    
    service = Service(set_service)

    res = service.sort_list_rules()
    assert res[0] == ['RVA DOUBLE', ['DOUBLE']]
