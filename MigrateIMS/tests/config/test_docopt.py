
import pytest
from sources.config.docopt import DocOpt


def test_init_object_DoctOpt():

    docopt = DocOpt({})

    assert isinstance(docopt, DocOpt)


def test_get_type_dn_PSTN_from_DoctOpt():

    docopt = DocOpt({'--pstn': True})

    assert docopt.get_type_dn() == 'pstn'


def test_get_type_dn_SIP_from_DoctOpt():

    docopt = DocOpt({'--sip': True})

    assert docopt.get_type_dn() == 'sip'


def test_get_type_dn_ALL_from_DoctOpt():

    docopt = DocOpt({'--all': True})

    assert docopt.get_type_dn() == 'other'


def test_get_type_dn_from_DocOpt_None():

    docopt = DocOpt({})
    with pytest.raises(Exception):
        docopt.get_type_dn()


def test_get_type_dn_from_cli_many_select():

    docopt = DocOpt({'--pstn': True, '--all': True})
    with pytest.raises(Exception):
        docopt.get_type_dn()
