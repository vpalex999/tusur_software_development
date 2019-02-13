
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
