import route


def test_route(G):
    r = route.Route(G)

    for u in r.G.nodes():
        assert r.G.nodes[u]['visited'] is False

    assert r.nodes == []
    assert r.edges == []
    assert r.distance == 0
