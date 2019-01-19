
import pytest
from sources.domain.category import Category


@pytest.fixture
def set_category():
    return {
            "Providers": [
                {"RT": {"AON": "1", "RULE": {"SR4": "56"}}},
                {"MTC": {"AON": "2", "RULE": {"SR3": "62"}}},
                {"VIMPEL": {"AON": "3", "RULE": {"SR5": "65"}}},
                {"EKVANT": {"AON": "4", "RULE": {"SR12": "63"}}},
                {"TRANST": {"AON": "6", "RULE": {"SR6": "58"}}},
                {"SINTERRA": {"AON": "7", "RULE": {"SR0": "59"}}},
                {"ARCTEL": {"AON": "8", "RULE": {"SR11": "64"}}},
                {"MTT": {"AON": "9", "RULE": {"SR1": "60"}}},
                {"CHOOSE_CALL": {"AON": "0", "RULE": {"SR7": "61"}}}
            ],
            "Default": [{"AON": "1", "id": "56"}]
            }
        

def test_init_category(set_category):

    category = Category(set_category)

    assert isinstance(category, Category)


def test_wrong_set_category_is_not_dict():

    with pytest.raises(TypeError): 
        Category('wrong')


def test_wrong_set_category_is_not_key_valid_Providers():
    
    with pytest.raises(KeyError): 
        Category({"Providers_err": []})

def test_wrong_set_category_is_not_key_valid_Default():

    with pytest.raises(KeyError):
        Category({"Providers": [], "Default_err": []})


def test_wrong_set_category_is_not_list_Default():

    with pytest.raises(Exception):
        Category({"Providers": [], "Default": 77})

def test_wrong_set_category_is_empty_list_Default():

    with pytest.raises(IndexError):
        Category({"Providers": [], "Default": []})



def test_get_category_sing_key(set_category):

    category = Category(set_category)

    assert category(["SR4"]) == '56'