import pytest
import osmnx as ox
from route_finder import RouteFinder


@pytest.fixture
def rf(G, center_point):
    source = ox.distance.nearest_nodes(G, *center_point, return_dist=False)
    max_distance = 500.0
    return RouteFinder(G, source, max_distance)


def test_route_finder_init(G, rf):
    assert rf.source in G.nodes
    assert rf.source == 7477543909
    assert rf.max_distance == pytest.approx(500.0)
