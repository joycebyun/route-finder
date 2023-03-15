import pytest
import osmnx as ox
from route_finder import RouteFinder
from edge import Edge


@pytest.fixture
def source(G, center_point):
    return ox.distance.nearest_nodes(G, *center_point, return_dist=False)


@pytest.fixture
def rf(G, source):
    max_distance = 500.0
    return RouteFinder(G, source, max_distance)


def test_route_finder_init(G, rf, source):
    assert rf.source in G.nodes
    assert rf.source == source
    assert rf.max_distance == pytest.approx(500.0)


def test_get_incident_edges(G, rf, source):
    n = source
    incident_edges = rf.get_incident_edges(n)

    # check that incident_edges does not include any non-incident edges
    for e in incident_edges:
        assert e.u == n or e.v == n

    # check that we are not missing any incident edges
    all_edges = [Edge(*i) for i in G.edges(data='length', keys=True)]
    for e in all_edges:
        if (e.u == n or e.v == n):
            flipped = Edge(u=e.v, v=e.u, key=e.key, length=e.length)
            assert e in incident_edges or flipped in incident_edges
