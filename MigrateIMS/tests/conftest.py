
import pytest


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
                {"ARCTEL": {"AON": "8", "RULE": {"SR11 SR0": "64"}}},
                {"MTT": {"AON": "9", "RULE": {"SR1": "60"}}},
                {"CHOOSE_CALL": {"AON": "0", "RULE": {"SR4 SR7": "61"}}}
            ],
            "Default": [{"AON": "1", "id": "56"}]
            }

