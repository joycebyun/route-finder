import pytest
import edge


@pytest.fixture
def e():
    return edge.Edge(u=1, v=2, key=0, length=100.0)


def test_edge(e):
    assert e.u == 1
    assert e.v == 2
    assert e.key == 0
    assert e.length == pytest.approx(100.0)


def test_edge_str(e):
    assert str(e) == str((1, 2, 0, 100.0))


def test_edge_repr(e):
    assert repr(e) == str(e)


@pytest.fixture
def edges():
    edges = []
    edges.append(edge.Edge(u=1, v=2, key=0, length=100.0))
    edges.append(edge.Edge(u=1, v=2, key=1, length=200.0))
    edges.append(edge.Edge(u=2, v=3, key=0, length=110.0))
    return edges


def test_total_length(edges):
    assert edge.total_length(edges) == pytest.approx(410.0)


def test_shortest_edge(edges):
    assert edge.shortest_edge(edges) == edges[0]
