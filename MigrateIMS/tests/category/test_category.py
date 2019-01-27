
import pytest
from sources.domain.category import Category
        

def test_init_category(set_category):
    """ Проверка инициализации """

    category = Category(set_category)

    assert isinstance(category, Category)


def test_wrong_set_category_is_not_dict():
    """ use_case_set_category 2.1 """
    with pytest.raises(Exception): 
        Category('wrong')


def test_wrong_set_category_is_not_key_valid_PROVIDERS():
    """ use_case_set_category 2.2 """
    with pytest.raises(KeyError): 
        Category({"PROVIDERS_err": []})


def test_init_wrong_set_category_is_not_key_valid_Default():
    """ use_case_set_category 2.2 """
    with pytest.raises(KeyError):
        Category({"PROVIDERS": [], "DEFAULT_err": []})


def test_init_wrong_set_category_is_not_list_Default():
    """ use_case_set_category 2.2 """
    with pytest.raises(Exception):
        Category({"PROVIDERS": [], "DEFAULT": 77})


def test_init_wrong_set_category_is_empty_list_Default():
    """ use_case_set_category 2.2 """
    with pytest.raises(IndexError):
        Category({"PROVIDERS": [], "DEFAULT": []})

def test_set_category_is_empty_list_PROVIDERS():
    """ use_case_set_category 4.1.1 """ 
    category = Category({"PROVIDERS": [], "DEFAULT": [{"AON": "1", "id": "56"}]})
    
    assert category([]) == '56'




def test_get_default_category(set_category):
    """ Проверка функции получения категории по умолчанию """
    category = Category(set_category)

    assert category.get_default_category() == '56'


def test_get_default_category_wrong():
    """ use_case_set_category 2.3 """
    category = Category({'PROVIDERS': [], 'DEFAULT': [{}]})
    
    with pytest.raises(KeyError):
        category.get_default_category()



def test_get_category_sing_key(set_category):
    """ use_case_set_category 4 """ 

    category = Category(set_category)

    assert category(["SR4"]) == '56'


def test_get_category_many_sing_key(set_category):
    """ use_case_set_category 4 """ 

    category = Category(set_category)

    assert category(["tt", "SR4", "ee", "SR7"]) == '61'


def test_get_category_many_sing_key_2(set_category):
    """ use_case_set_category 4 """ 

    category = Category(set_category)

    assert category(["tt", "SR11 SR0", "ee", "SR7"]) == '64'



def test_get_category_list_options_is_empty(set_category):
    """ use_case_set_category 3.1.1 """ 

    category = Category(set_category)

    assert category([]) == '56'


def test_get_category_list_options_is_None(set_category):
    """ use_case_set_category 3.2.1 """ 

    category = Category(set_category)

    assert category(None) == '56'


def test_get_category_list_options_has_not_category(set_category):
    """ use_case_set_category 3.3.1 """ 

    category = Category(set_category)

    assert category([""]) == '56'


def test_sort_category_rules(set_category):
    
    category = Category(set_category)

    res = category.sort_list_rules()
    assert res[0] == ('SR11 SR0', '64')
