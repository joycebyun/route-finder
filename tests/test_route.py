from route import Route


def test_route():
    r = Route()
    assert r.nodes == []
    assert r.edges == []
    assert r.distance == 0
