
import pytest
from sources.domain.license_type import LicenseType
from sources.domain.errors import MigrateError


@pytest.fixture
def lic():
    return LicenseType()


def lic_dict():
    return {
            'basicLicense': '21',
            'standardLicense': '20',
            'advancedLicense': '22'
        }


def test_init_license_type():
    """ Проверка инициализации """

    lic = LicenseType()

    assert isinstance(lic, LicenseType)


@pytest.mark.parametrize("lic_name, lic_id", [(key, val) for (key, val) in lic_dict().items()])
def test_get_license_type_id_by_name(lic, lic_name, lic_id):

    assert lic.get_id_by_name(lic_name) == lic_id


def test_get_license_type_id_by_name_wrong(lic):

    with pytest.raises(MigrateError):
        assert lic.get_id_by_name("wrong name license")


@pytest.mark.parametrize('suppl, lic_type', [([], 'basicLicense'), (['OIP'], 'basicLicense'), (['OIP', 'CFU'], 'standardLicense'), (['OIP', 'CFU', "ACR"], 'advancedLicense')])
def test_get_license_type(lic, suppl, lic_type):

        assert lic.get_lic(suppl) == lic_type


def test_get_license_type_out_of_set_lic(lic):

    with pytest.raises(MigrateError):
        lic.get_lic('BLA')


def test_get_id_by_list_set(lic):
    assert lic.get_id_lic_by_set(["OIP"]) == '21'


@pytest.mark.parametrize('lic_type', ['advancedLicense'])
@pytest.mark.parametrize('suppl_list', [["PEOC", "FCR"], ["CFU", "CFB"], ["OIP", "OIR"]])
def test_check_is_cover_license_advance(lic, lic_type, suppl_list):

    assert lic.is_cover_lic(lic_type, suppl_list) is True


@pytest.mark.parametrize('lic_type', ['standardLicense'])
@pytest.mark.parametrize('suppl_list', [["CFU", "CFB"], ["OIP", "OIR"]])
def test_check_is_cover_license_standart(lic, lic_type, suppl_list):

    assert lic.is_cover_lic(lic_type, suppl_list) is True


@pytest.mark.parametrize('lic_type', ['basicLicense'])
@pytest.mark.parametrize('suppl_list', [["OIP", "OIR"]])
def test_check_is_cover_license_basic(lic, lic_type, suppl_list):

    assert lic.is_cover_lic(lic_type, suppl_list) is True


@pytest.mark.parametrize('lic_type', ['basicLicense'])
@pytest.mark.parametrize('suppl_list', [["PEOC", "FCR"]])
def test_check_is_is_cover_license_basic_wrong(lic, lic_type, suppl_list):

    assert lic.is_cover_lic(lic_type, suppl_list) is False
