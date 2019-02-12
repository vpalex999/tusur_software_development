
from sources.domain.defaultsubscriber import DefaultSubscriber


def test_defaultsubscriber_model_init():

    dn = '3436873639'
    password = 'test_pswd'
    category = '56'

    def_subs = DefaultSubscriber(dn=dn, password=password, category=category)

    assert def_subs.dn == '3436873639'
    assert def_subs.type_dn is None
    assert def_subs.password == 'test_pswd'
    assert def_subs.category == '56'
    assert def_subs.services is None
    assert def_subs.service_set == '-1'
    assert def_subs.custom_service_set is None
    assert def_subs.active_services is None
    assert def_subs.interface is None
    assert def_subs.access is None


def test_defaultsubscriber_model_from_dict():

    dn = '3436873639'
    category = '56'

    def_subs = DefaultSubscriber.from_dict(
        {
            'dn': dn,
            'type_dn': "SIP",
            'password': "iskratel",
            'category': category
        }
    )

    assert def_subs.dn == '3436873639'
    assert def_subs.type_dn == 'SIP'
    assert def_subs.password == 'iskratel'
    assert def_subs.category == '56'
    assert def_subs.services is None
    assert def_subs.service_set == '-1'
    assert def_subs.custom_service_set is None
    assert def_subs.active_services is None
    assert def_subs.interface is None
    assert def_subs.access is None
