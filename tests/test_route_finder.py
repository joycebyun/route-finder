import pytest

import os
# Force geopandas to use Shapely 2.0 instead of PyGEOS
# (PyGEOS was merged with Shapely, and will stop working in a future release of GeoPandas)
os.environ['USE_PYGEOS'] = '0'
import osmnx as ox 

from route_finder import RouteFinder
from edge import Edge, flip
from route import Route
import networkx as nx


@pytest.fixture
def source(G, center_point):
    return ox.distance.nearest_nodes(G, *center_point, return_dist=False)


@pytest.fixture
def rf(G, source):
    max_distance = 500.0
    return RouteFinder(G, source, max_distance)


def test_route_finder_init(rf, source):
    assert rf.source in rf.G.nodes
    assert rf.source == source
    assert rf.max_distance == pytest.approx(500.0)


def test_get_incident_edges(rf, source):
    n = source
    incident_edges = rf.get_incident_edges(n)

    # check that incident_edges does not include any non-incident edges
    for e in incident_edges:
        assert e.u == n

    # check that we are not missing any incident edges
    all_edges = [Edge(*i) for i in rf.G.edges(data='length', keys=True)]
    for e in all_edges:
        if e.u == n:
            assert e in incident_edges
        elif e.v == n:
            assert flip(e) in incident_edges


@pytest.fixture
def route_fixture(rf, source):
    r = Route(rf.G)
    r.nodes.append(source)
    return r


def test_get_viable_edges(rf, route_fixture):
    viable_edges = rf.get_viable_edges(route_fixture)

    # check that the edges are viable
    for e in viable_edges:
        assert (route_fixture.distance
                + e.length
                + nx.shortest_path_length(rf.G,
                                          source=e.v,
                                          target=rf.source,
                                          weight='length')) <= rf.max_distance

    # check that we are not missing any viable edges
    u = route_fixture.nodes[-1]
    incident_edges = rf.get_incident_edges(u)
    for e in incident_edges:
        if e not in viable_edges:
            assert (route_fixture.distance
                    + e.length
                    + nx.shortest_path_length(rf.G,
                                              source=e.v,
                                              target=rf.source,
                                              weight='length')) > rf.max_distance
