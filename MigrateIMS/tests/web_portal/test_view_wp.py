
from sources.domain.view_wp import ViewWP

def test_init_view_wp():

    view_wp = ViewWP([])

    assert isinstance(view_wp, ViewWP)


def test_view_wp_get_first_header(def_subs_wp):

    view_wp = ViewWP([def_subs_wp])

    assert view_wp.header_1() == "IMS User Subscription|||IMS Private User Identity|||IMS Public User Identity|||||||||Access Gateway Control Function|||||||||||||||||||IMS Public Identities from implicit registration set|||Telephony Application Server||||||||Additional parameters needed  for migration||||||\n"


def test_view_wp_get_second_header(def_subs_wp):

    view_wp = ViewWP([def_subs_wp])

    assert view_wp.header_2() == "Name *|Capabilities Set|Preferred S-CSCF Set|Secret Key K *|Authorization Schemes|Default Auth. Scheme|Type|Barring|Service Profile|Charging Info|Wildcard PSI|Display Name|PSI Activation|Can Register|Allowed Roaming|Type *|Node *|URI Type *|Interface *|Access *|Access Variant *|RTP Profile *|Password *|Private Id Alias|Embed telURI into SIP URI|DTMF Authorization|Out of Service Indication|Active Subscriber|Initiate registration at system startup|Display/Ring Type|In-band Indication Type|Tariff Origin Code|Standalone Mode Calls|Hotline Enable|URI Type|Hotline Enable|Set as MSN Number|TAS Node|Supplementary Service Set|Concurrent Sessions|License Type*|Subscriber Category|m.SipProfile.class|Business Group|Custom Service Set|NGN Interface *|NGN Access *|NGN Access Variant *|NGN RTP Profile *|Time Zone|Geographical Area|\n"


def test_view_wp_make_number(def_subs_wp):

    view_wp = ViewWP([def_subs_wp])

    assert view_wp.make_number(def_subs_wp) == "|||aXNrcmF0ZWw=||||||||||no|1||||||||||||||||||||||||||||1|||||||||\n"


def test_view_wp_call(def_subs_wp):

    view_wp = ViewWP([def_subs_wp])

    assert view_wp() == [
        "IMS User Subscription|||IMS Private User Identity|||IMS Public User Identity|||||||||Access Gateway Control Function|||||||||||||||||||IMS Public Identities from implicit registration set|||Telephony Application Server||||||||Additional parameters needed  for migration||||||\n",
        "Name *|Capabilities Set|Preferred S-CSCF Set|Secret Key K *|Authorization Schemes|Default Auth. Scheme|Type|Barring|Service Profile|Charging Info|Wildcard PSI|Display Name|PSI Activation|Can Register|Allowed Roaming|Type *|Node *|URI Type *|Interface *|Access *|Access Variant *|RTP Profile *|Password *|Private Id Alias|Embed telURI into SIP URI|DTMF Authorization|Out of Service Indication|Active Subscriber|Initiate registration at system startup|Display/Ring Type|In-band Indication Type|Tariff Origin Code|Standalone Mode Calls|Hotline Enable|URI Type|Hotline Enable|Set as MSN Number|TAS Node|Supplementary Service Set|Concurrent Sessions|License Type*|Subscriber Category|m.SipProfile.class|Business Group|Custom Service Set|NGN Interface *|NGN Access *|NGN Access Variant *|NGN RTP Profile *|Time Zone|Geographical Area|\n",
        "|||aXNrcmF0ZWw=||||||||||no|1||||||||||||||||||||||||||||1|||||||||\n"
    ]


def test_view_wp_call_empty_list():

    view_wp = ViewWP([])

    assert view_wp() == []
    