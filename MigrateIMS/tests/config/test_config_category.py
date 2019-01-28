import pytest
from sources.config.config import Config
from sources.domain.category import Category


def test_set_category(set_category):
    config = Config(set_category=set_category)

    assert config.set_category == set_category


def test_make_category_obj(set_category):
    config = Config(set_category=set_category)
    config.make_category()

    assert isinstance(config.category, Category)


