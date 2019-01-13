
from sources.domain.defaultsubscriber import DefaultSubscriber


def test_defaultsubscriber_model_init():

    dn = '3436873639'
    category = '56'

    def_subs = DefaultSubscriber(dn, category)

    assert def_subs.dn == '3436873639'
    assert def_subs.category == '56'
    assert def_subs.services is None
    assert def_subs.service_set == '-1'
    assert def_subs.custom_service_set is None
    assert def_subs.active_services is None


def test_defaultsubscriber_model_from_dict():

    dn = '3436873639'
    category = '56'

    def_subs = DefaultSubscriber.from_dict(
        {
            'dn': dn,
            'category': category
        }
    )

    assert def_subs.dn == '3436873639'
    assert def_subs.category == '56'
    assert def_subs.services is None
    assert def_subs.service_set == '-1'
    assert def_subs.custom_service_set is None
    assert def_subs.active_services is None
