import pytest
import osmnx as ox
import route


@pytest.fixture
def G():
    address = "501 E 9th St, Tucson, AZ 85705"

    MDG = ox.graph.graph_from_address(address=address,
                                      dist=1000,  # meters from center
                                      dist_type='bbox',
                                      network_type='drive',
                                      simplify=False,
                                      retain_all=True,
                                      truncate_by_edge=False,
                                      return_coords=False,
                                      clean_periphery=False,
                                      custom_filter=None)

    # Remove interstitial nodes (nodes that are not intersections or dead-ends)
    MDG = ox.simplification.simplify_graph(MDG,
                                           strict=False,
                                           remove_rings=False,
                                           track_merged=False)

    MG = ox.utils_graph.get_undirected(MDG)
    return MG


def test_route(G):
    r = route.Route(G)

    for u in r.G.nodes():
        assert r.G.nodes[u]['visited'] is False

    assert r.nodes == []
    assert r.edges == []
    assert r.distance == 0
