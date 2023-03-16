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


@pytest.fixture
def rf_grid(grid):
    source = 0
    max_distance = 4.0
    return RouteFinder(grid, source, max_distance)


def test_get_incident_edges_grid(rf_grid):
    incident_edges = rf_grid.get_incident_edges(u=0)
    assert len(incident_edges) == 4
    assert Edge(0, 2, 0, 1.0) in incident_edges
    assert Edge(0, 4, 0, 1.0) in incident_edges
    assert Edge(0, 6, 0, 1.0) in incident_edges
    assert Edge(0, 8, 0, 1.0) in incident_edges

    incident_edges = rf_grid.get_incident_edges(u=8)
    assert len(incident_edges) == 3
    assert Edge(8, 1, 0, 1.0) in incident_edges
    assert Edge(8, 0, 0, 1.0) in incident_edges
    assert Edge(8, 7, 0, 1.0) in incident_edges


def test_get_viable_edges_grid(grid, rf_grid):
    route = Route(grid)
    route.nodes = [0, 2, 3]
    route.edges.append(Edge(0, 2, 0, 1.0))
    route.edges.append(Edge(2, 3, 0, 1.0))
    route.distance = 2.0

    viable_edges = rf_grid.get_viable_edges(route)
    assert len(viable_edges) == 2
    assert Edge(3, 2, 0, 1.0) in viable_edges
    assert Edge(3, 4, 0, 1.0) in viable_edges


def test_brute_force_finds_all(rf_grid):
    rf_grid.brute_force()
    assert len(rf_grid.all_routes) == 32


def test_brute_force_distances(rf_grid):
    rf_grid.brute_force()
    for r in rf_grid.all_routes:
        assert r.distance == pytest.approx(4.0)


def test_brute_force_route_nodes(rf_grid):
    rf_grid.brute_force()

    nodes = set()
    for r in rf_grid.all_routes:
        nodes.add(str(r.nodes))

    assert str([0, 2, 0, 2, 0]) in nodes
    assert str([0, 2, 0, 4, 0]) in nodes
    assert str([0, 2, 0, 6, 0]) in nodes
    assert str([0, 2, 0, 8, 0]) in nodes

    assert str([0, 4, 0, 2, 0]) in nodes
    assert str([0, 4, 0, 4, 0]) in nodes
    assert str([0, 4, 0, 6, 0]) in nodes
    assert str([0, 4, 0, 8, 0]) in nodes

    assert str([0, 6, 0, 2, 0]) in nodes
    assert str([0, 6, 0, 4, 0]) in nodes
    assert str([0, 6, 0, 6, 0]) in nodes
    assert str([0, 6, 0, 8, 0]) in nodes

    assert str([0, 8, 0, 2, 0]) in nodes
    assert str([0, 8, 0, 4, 0]) in nodes
    assert str([0, 8, 0, 6, 0]) in nodes
    assert str([0, 8, 0, 8, 0]) in nodes

    assert str([0, 2, 3, 2, 0]) in nodes
    assert str([0, 4, 3, 4, 0]) in nodes

    assert str([0, 4, 5, 4, 0]) in nodes
    assert str([0, 6, 5, 6, 0]) in nodes

    assert str([0, 6, 7, 6, 0]) in nodes
    assert str([0, 8, 7, 8, 0]) in nodes

    assert str([0, 8, 1, 8, 0]) in nodes
    assert str([0, 2, 1, 2, 0]) in nodes

    assert str([0, 2, 3, 4, 0]) in nodes
    assert str([0, 4, 3, 2, 0]) in nodes

    assert str([0, 4, 5, 6, 0]) in nodes
    assert str([0, 6, 5, 4, 0]) in nodes

    assert str([0, 6, 7, 8, 0]) in nodes
    assert str([0, 8, 7, 6, 0]) in nodes

    assert str([0, 8, 1, 2, 0]) in nodes
    assert str([0, 2, 1, 8, 0]) in nodes


def test_maximize_new_nodes(rf_grid):
    rf_grid.brute_force()
    routes = RouteFinder.maximize_new_nodes(rf_grid.all_routes)
    assert len(routes) == 8

