import pytest
from sources.config.config import Config
from sources.domain.category import Category


def test_set_category(mapping_category):
    config = Config(mapping_category=mapping_category)

    assert config.mapping_category == mapping_category


def test_make_category_obj(mapping_category):
    config = Config(mapping_category=mapping_category)
    config.make_category()

    assert isinstance(config.category, Category)


