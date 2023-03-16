import pytest
import os
import networkx as nx

# Force geopandas to use Shapely 2.0 instead of PyGEOS
# (PyGEOS was merged with Shapely, and will stop working in a future release of GeoPandas)
os.environ['USE_PYGEOS'] = '0'

import osmnx as ox


@pytest.fixture
def center_point():
    return (32.231774, -110.9438645)


@pytest.fixture
def G(center_point):
    MDG = ox.graph.graph_from_point(center_point=center_point,
                                    dist=1000,  # meters from center
                                    dist_type='bbox',
                                    network_type='drive',
                                    simplify=False,
                                    retain_all=True,
                                    truncate_by_edge=False,
                                    clean_periphery=False,
                                    custom_filter=None)

    # Remove interstitial nodes (nodes that are not intersections or dead-ends)
    MDG = ox.simplification.simplify_graph(MDG,
                                           strict=False,
                                           remove_rings=False,
                                           track_merged=False)

    MG = ox.utils_graph.get_undirected(MDG)
    return MG


@pytest.fixture
def grid():
    # create a 3x3 grid of nodes, where 0 is in the middle
    G = nx.MultiGraph()

    G.add_edge(1, 2, 0)
    G.add_edge(2, 3, 0)
    G.add_edge(3, 4, 0)
    G.add_edge(4, 5, 0)
    G.add_edge(5, 6, 0)
    G.add_edge(6, 7, 0)
    G.add_edge(7, 8, 0)
    G.add_edge(8, 1, 0)

    G.add_edge(0, 2, 0)
    G.add_edge(0, 4, 0)
    G.add_edge(0, 6, 0)
    G.add_edge(0, 8, 0)

    nx.set_edge_attributes(G, name='length', values=1.0)
    return G
