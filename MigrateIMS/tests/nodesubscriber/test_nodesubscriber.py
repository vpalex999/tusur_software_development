from sources.domain.nodesubscriber import NodeSubscriber


def test_init_node_subscriber():
    node_s = NodeSubscriber("3436873639")

    assert isinstance(node_s, NodeSubscriber)
    assert node_s.dn == "3436873639"
    assert node_s.type_dn == 'OTHER'
    assert node_s.password == ''
    assert node_s.interface is None
    assert node_s.access is None
    assert node_s.list_dn_options == []


def test_node_subscriber_from_dict():

    node_s = NodeSubscriber.from_dict(
        {
            'dn': "3436873639",
            'type_dn': "SIP",
            'password': 'iskratel',
            'interface': '2000',
            'access': '1',
            'list_dn_options': []
        }
    )

    assert node_s.dn == "3436873639"
    assert node_s.type_dn == 'SIP'
    assert node_s.password == 'iskratel'
    assert node_s.interface == '2000'
    assert node_s.access == '1'
    assert node_s.list_dn_options == []
