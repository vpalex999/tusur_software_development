
import pytest
import json


@pytest.fixture
def mapping_category():
    return {
            "PROVIDERS": [
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
            "DEFAULT": [{"AON": "1", "id": "56"}]
            }


@pytest.fixture
def mapping_service():
    return {
        "SI": {
            "RVT": ["CFU"],
            "RVA": ["ACS"],
            "DAI": ["HOLD", "CW"],
            "DAP": ["HOLD", "ECT"],
            "DCA": ["HOLD", "3PTY"],
            "IAM": ["OIP"],
            "RVA DOUBLE": ["DOUBLE"]
        },
        "SUSPEND": [
            {"name": "Suspension Hard", "key": ["DF1"], "type": "out_inc"},
            {"name": "Suspension Soft", "key": ["PPR"], "type": "out"},
            {"name": "Suspension Soft", "key": ["SR8", "DF1"], "type": "out"}
        ]
    }


@pytest.fixture
def mapping_ims():
    return {
        "IMS": {
            "test ims": "test_ims1"
        },
        "SUBSCRIBER": {
            "NDC": "7343",
            "PASSWORD": "iskratel",
            "LICENSE": "basicLicense",
            "Capabilities Set": "1",
            "Preferred S-CSCF Set": "2",
            "Authorization Schemes": "255",
            "Default Auth. Scheme": "128",
            "Secret Key K *": "iskratel",
            "Type": '',
            "Barring": "no",
            'Service Profile': "1",
            'Charging Info': '2',
            'Wildcard PSI': "wildcard",
            "Display Name": "Vacya",
            'PSI Activation': "yes",
            'Can Register': 'no',
            'Allowed Roaming': '1,  2',
            'Type *': '',
            'Node *': '3333',
            'URI Type *': 'telUri',
            'Interface *': '',
            'Access *': '',
            'Access Variant *': '1',
            'RTP Profile *': '2',
            'Password *': '',
            'Private Id Alias': '5',
            'Embed telURI into SIP URI': 'no',
            'DTMF Authorization': 'yes',
            'Out of Service Indication': "",
            'Active Subscriber': 'yes',
            'Initiate registration at system startup': "",
            'Display/Ring Type': "",
            'In-band Indication Type': "",
            'Tariff Origin Code': '1',
            'Standalone Mode Calls': "",
            'Hotline Enable': 'none',
            'URI Type': "",
            'Set as MSN Number': "",
            "TAS Node": "7777",
            'Supplementary Service Set': "901",
            'Concurrent Sessions': '1',
            'License Type*': 'basicLicense',
            'Subscriber Category': '56',
            'm.SipProfile.class': '92',
            'Business Group': '5',
            'Custom Service Set': "",
            'NGN Interface *': '',
            "Time Zone": "",
            "Geographical Area": "",
        }
    }


@pytest.fixture
def def_subs_wp():
    return json.load(open('templates/template_web_portal.json'))
