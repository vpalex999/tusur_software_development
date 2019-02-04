
import pytest
from sources.domain.custom_service_set import CustomServiceSet
        

def test_init_custom_service():
    """ Проверка инициализации """

    custom_service = CustomServiceSet()

    assert isinstance(custom_service, CustomServiceSet)


def test_make_custom_set_service_from_list_service():
    """ use_case_set_custom_service_set_4 """
    custom_service = CustomServiceSet()

    custom_service.make(["CW", "CFU"])

    assert custom_service.cwAuth == "1"
    assert custom_service.cfuAuth == "1"
    assert custom_service.subsctg == "56"



def test_add_category_to_custom_set_():
    """ use_case_set_custom_service_set_6 """

    custom_service = CustomServiceSet()

    custom_service.make([], category="57")

    dict_result = custom_service()

    assert dict_result["subsctg"] == "57"
    assert dict_result["cfuAuth"] == "0"


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
