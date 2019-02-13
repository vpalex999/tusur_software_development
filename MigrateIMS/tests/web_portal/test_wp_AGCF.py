""" Тесты для обработчика данных номера в формат импорта на WEB PORTAL"""
import pytest
from unittest import mock
from sources.domain.defaultsubscriber import DefaultSubscriber as DS
from sources.domain.ims import IMS
from sources.domain.wp import WpDN
from sources.domain.errors import MigrateError


@pytest.fixture
def config(mapping_ims):
    config = mock.Mock()
    config.PSTN = 'PSTN'
    config.ims = IMS(mapping_ims)
    return config


@pytest.fixture
def wp(config):
    subs = DS(dn='6873639',
              password="iskratel",
              type_dn='PSTN',
              interface='1',
              access='1')
    return WpDN(subs, config)


def test_configure_agcf(wp):

    assert wp.configure_agcf() is True


def test_set_type_agcf(wp):

    wp.set_type_agcf()
    assert wp.subscriber_dict['Access Gateway Control Function']['Type *'] == 'Analog Subscriber'


def test_set_node_agcf(wp):

    wp.set_node_agcf()
    assert wp.subscriber_dict['Access Gateway Control Function']['Node *'] == '3333'


def test_set_node_agcf_is_None(wp):
    setattr(wp.ims, 'Node *', None)

    with pytest.raises(MigrateError):
        wp.set_node_agcf()


def test_set_node_agcf_is_not_String(wp):
    setattr(wp.ims, 'Node *', 123)

    with pytest.raises(MigrateError):
        wp.set_node_agcf()


def test_set_node_agcf_is_not_Digits(wp):
    setattr(wp.ims, 'Node *', "ABC")

    with pytest.raises(MigrateError):
        wp.set_node_agcf()


def test_set_uri_type_agcf(wp):

    wp.set_uri_type_agcf()
    assert wp.subscriber_dict['Access Gateway Control Function']['URI Type *'] == 'telUri'


def test_set_uri_type_agcf_is_None(wp):

    setattr(wp.ims, "URI Type *", None)

    with pytest.raises(MigrateError):
        wp.set_uri_type_agcf()


def test_set_uri_type_agcf_is_not_String(wp):

    setattr(wp.ims, "URI Type *", 123)

    with pytest.raises(MigrateError):
        wp.set_uri_type_agcf()


def test_set_uri_type_agcf_is_not_Chosen(wp):

    setattr(wp.ims, "URI Type *", '127')

    with pytest.raises(MigrateError):
        wp.set_uri_type_agcf()


def test_set_interface(wp):

    wp.number.interface = '2000'
    wp.set_interface()

    assert wp.subscriber_dict['Access Gateway Control Function']['Interface *'] == '2000'


def test_set_interface_is_None(wp):

    wp.interface = None

    with pytest.raises(MigrateError):
        wp.set_interface()


def test_set_interface_is_not_String(wp):

    wp.number.interface = 2000

    with pytest.raises(MigrateError):
        wp.set_interface()


def test_set_service_profile_is_not_Digits(wp):

    wp.number.interface = 'ABC'

    with pytest.raises(MigrateError):
        wp.set_interface()


def test_set_access(wp):

    wp.number.access = '1'
    wp.set_access()
    assert wp.subscriber_dict['Access Gateway Control Function']['Access *'] == '1'


def test_set_access_is_None(wp):

    wp.access = None

    with pytest.raises(MigrateError):
        wp.set_access()


def test_set_access_is_not_String(wp):

    wp.number.access = 1

    with pytest.raises(MigrateError):
        wp.set_access()


def test_set_access_is_not_Digits(wp):

    wp.number.access = 'ABC'

    with pytest.raises(MigrateError):
        wp.set_access()


@pytest.mark.parametrize('variant', ['1'])
def test_set_access_variant(wp, variant):

    setattr(wp.ims, "Access Variant *", variant)

    wp.set_type_agcf()
    wp.set_access_variant()

    assert wp.subscriber_dict['Access Gateway Control Function']['Access Variant *'] == variant


@pytest.mark.parametrize('variant', [None, 123, 'ABC'])
def test_set_access_variant_is_Wrong(wp, variant):

    setattr(wp.ims, "Access Variant *", variant)

    wp.set_type_agcf()

    with pytest.raises(MigrateError):
        wp.set_access_variant()


@pytest.mark.parametrize('rtp_profile, type_dn', [('2', 'ISDN Subscriber'), ("", "Analog Subscriber")])
def test_set_rtp_profile(wp, rtp_profile, type_dn):

    setattr(wp.ims, 'RTP Profile *', rtp_profile)
    wp.subscriber_dict['Access Gateway Control Function']['Type *'] = type_dn

    wp.set_rtp_profile()

    assert wp.subscriber_dict['Access Gateway Control Function']['RTP Profile *'] == rtp_profile


@pytest.mark.parametrize('rtp_profile', [None, 123, 'ABC', ""])
@pytest.mark.parametrize('type_dn', ['ISDN Subscriber'])
def test_set_rtp_profile_wrong(wp, rtp_profile, type_dn):

    setattr(wp.ims, 'RTP Profile *', rtp_profile)
    wp.subscriber_dict['Access Gateway Control Function']['Type *'] = type_dn

    with pytest.raises(MigrateError):
        wp.set_rtp_profile()


def test_set_password(wp):

    wp.subscriber_dict['IMS Private User Identity']['Secret Key K *'] = 'test_pswd'

    wp.set_password()

    assert wp.subscriber_dict['Access Gateway Control Function']['Password *'] == 'test_pswd'


@pytest.mark.parametrize('password', [None, 123, ""])
def test_set_password_wrong(wp, password):

    wp.subscriber_dict['IMS Private User Identity']['Secret Key K *'] = password

    with pytest.raises(MigrateError):
        wp.set_password()


@pytest.mark.parametrize('id_alias, result', [('4', '4'), (None, ''), ("", "")])
def test_set_private_id_alias(wp, id_alias, result):

    setattr(wp.ims, 'Private Id Alias', id_alias)
    wp.set_private_id_alias()

    assert wp.subscriber_dict['Access Gateway Control Function']['Private Id Alias'] == result


@pytest.mark.parametrize('id_alias', [123, 'ABC'])
def test_set_private_id_alias_wrong(wp, id_alias):

    setattr(wp.ims, 'Private Id Alias', id_alias)

    with pytest.raises(MigrateError):
        wp.set_private_id_alias()


@pytest.mark.parametrize('embed, result', [('no', 'no'), ('yes', 'yes'), ("", ""), (None, "")])
def test_set_embed_teluri(wp, embed, result):

    setattr(wp.ims, 'Embed telURI into SIP URI', embed)

    wp.set_embed_teluri()

    assert wp.subscriber_dict['Access Gateway Control Function']['Embed telURI into SIP URI'] == result


@pytest.mark.parametrize('embed', [123, 'ABC'])
def test_set_embed_teluri_wrong(wp, embed):

    setattr(wp.ims, 'Embed telURI into SIP URI', embed)

    with pytest.raises(MigrateError):
        wp.set_embed_teluri()


@pytest.mark.parametrize('dtmf, result', [('no', 'no'), ('yes', 'yes'), ("", ""), (None, "")])
def test_set_dtmf(wp, dtmf, result):

    setattr(wp.ims, 'DTMF Authorization', dtmf)

    wp.set_dtmf()
    assert wp.subscriber_dict['Access Gateway Control Function']['DTMF Authorization'] == result


def test_set_dtmf_wrong(wp):

    setattr(wp.ims, 'DTMF Authorization', 'ABC')

    with pytest.raises(MigrateError):
        wp.set_dtmf()


@pytest.mark.parametrize('out, result', [('no', 'no'), ('yes', 'yes'), ("", ""), (None, "")])
def test_set_out_of_service(wp, out, result):

    setattr(wp.ims, 'Out of Service Indication', out)

    wp.set_out_of_service()
    assert wp.subscriber_dict['Access Gateway Control Function']['Out of Service Indication'] == result


@pytest.mark.parametrize('out', [123, 'ABC'])
def test_set_out_of_service_wrong(wp, out):

    setattr(wp.ims, 'Out of Service Indication', out)

    with pytest.raises(MigrateError):
        wp.set_out_of_service()


@pytest.mark.parametrize('active, result', [('no', 'no'), ('yes', 'yes'), ("", ""), (None, "")])
def test_set_active_subscriber(wp, active, result):

    setattr(wp.ims, 'Active Subscriber', active)

    wp.set_active_subscriber()

    assert wp.subscriber_dict['Access Gateway Control Function']['Active Subscriber'] == result


@pytest.mark.parametrize('active', [123, 'ABC'])
def test_set_active_subscriber_wrong(wp, active):

    setattr(wp.ims, 'Active Subscriber', active)

    with pytest.raises(MigrateError):
        wp.set_active_subscriber()


@pytest.mark.parametrize('status_reg, result', [('no', 'no'), ('yes', 'yes'), ("", ""), (None, "")])
def test_set_initiate_reg_startup(wp, status_reg, result):

    setattr(wp.ims, 'Initiate registration at system startup', status_reg)

    wp.set_initiate_reg_startup()
    assert wp.subscriber_dict['Access Gateway Control Function']['Initiate registration at system startup'] == result


@pytest.mark.parametrize('status_reg', [123, 'ABC'])
def test_set_initiate_reg_startup_wrong(wp, status_reg):

    setattr(wp.ims, 'Initiate registration at system startup', status_reg)

    with pytest.raises(MigrateError):
        wp.set_initiate_reg_startup()


@pytest.mark.parametrize('ring', ['Analog Public', 'Analog PBX', 'Not Used', ""])
def test_set_display_ring_type(wp, ring):

    setattr(wp.ims, 'Display/Ring Type', ring)

    wp.set_display_ring_type()

    assert wp.subscriber_dict['Access Gateway Control Function']['Display/Ring Type'] == ring


def test_set_display_ring_type_is_None(wp):

    setattr(wp.ims, 'Display/Ring Type', None)

    wp.set_display_ring_type()

    assert wp.subscriber_dict['Access Gateway Control Function']['Display/Ring Type'] == ""


@pytest.mark.parametrize('ring', [123, 'ABC'])
def test_set_display_ring_type_wrong(wp, ring):

    setattr(wp.ims, 'Display/Ring Type', ring)

    with pytest.raises(MigrateError):
        wp.set_display_ring_type()


@pytest.mark.parametrize('inband', ['ISDN Public', 'Analog Public', 'ISDN PBX', 'Analog PBX', 'PC', ''])
def test_set_inband(wp, inband):

    setattr(wp.ims, 'In-band Indication Type', inband)

    wp.set_inband()

    assert wp.subscriber_dict['Access Gateway Control Function']['In-band Indication Type'] == inband


def test_set_inband_is_None(wp):

    setattr(wp.ims, 'In-band Indication Type', None)

    wp.set_inband()

    assert wp.subscriber_dict['Access Gateway Control Function']['In-band Indication Type'] == ''


@pytest.mark.parametrize('inband', [123, 'ABC'])
def test_set_inband_is_Wrong(wp, inband):

    setattr(wp.ims, 'In-band Indication Type', inband)

    with pytest.raises(MigrateError):
        wp.set_inband()


@pytest.mark.parametrize('tarif, result', [('2', "2"), (None, "1")])
def test_set_tariff_origin_code(wp, tarif, result):

    setattr(wp.ims, 'Tariff Origin Code', tarif)

    wp.set_tariff_origin_code()

    assert wp.subscriber_dict['Access Gateway Control Function']['Tariff Origin Code'] == result


@pytest.mark.parametrize('tarif', [123, 'ABC'])
def test_set_tariff_origin_code_is_Wrong(wp, tarif):

    setattr(wp.ims, 'Tariff Origin Code', tarif)

    with pytest.raises(MigrateError):
        wp.set_tariff_origin_code()


@pytest.mark.parametrize('mode, result', [('no', 'no'), ('yes', 'yes'), ("", ""), (None, "")])
def test_set_standalone_mode(wp, mode, result):

    setattr(wp.ims, 'Standalone Mode Calls', mode)

    wp.set_standalone_mode()
    assert wp.subscriber_dict['Access Gateway Control Function']['Standalone Mode Calls'] == result


@pytest.mark.parametrize('mode', [123, 'ABC'])
def test_set_standalone_mode_wrong(wp, mode):

    setattr(wp.ims, 'Standalone Mode Calls', mode)

    with pytest.raises(MigrateError):
        wp.set_standalone_mode()


@pytest.mark.parametrize('mode, result', [('none', 'none'), ('hotd', 'hotd'), ("hoti", "hoti"), (None, "none")])
def test_set_hotline_agcf(wp, mode, result):

    setattr(wp.ims, 'Hotline Enable', mode)

    wp.set_hotline_agcf()
    assert wp.subscriber_dict['Access Gateway Control Function']['Hotline Enable'] == result


@pytest.mark.parametrize('mode', [123, 'ABC'])
def test_set_hotline_agcf_is_Wrong(wp, mode):

    setattr(wp.ims, 'Hotline Enable', mode)

    with pytest.raises(MigrateError):
        wp.set_hotline_agcf()
