import pytest
from sources.config.config import Config
from sources.config.config import *


def test_set_type_sip():
    config = Config()

    assert config.type_dn == OTHER


def test_set_type_pstn():
    config = Config(type_dn=PSTN)

    assert config.type_dn == PSTN


def test_set_type_all():
    config = Config(type_dn=OTHER)

    assert config.type_dn == OTHER


def test_check_type_dn_ok():
    config = Config()

    assert config.check_type_dn() is None


def test_check_type_dn_wrong():
    config = Config(type_dn='wrong')
    with pytest.raises(Exception):
        config.check_type_dn()
