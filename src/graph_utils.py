from edge import Edge
import networkx as nx
from typing import List

def get_incident_edges(G: nx.MultiGraph, u: int) -> List[Edge]:
    """For an input node, get a list of all the incident edges
    (all edges that start at the input node).

    :param G: Input graph
    :type G: MultiGraph
    :param u: Node
    :type u: int
    :return: List of edges that are incident on this node
    :rtype: List[Edge]
    """
    return [Edge(*e) for e in G.edges(nbunch=u, data='length', keys=True)]

def is_unvisited(G: nx.MultiGraph, u: int) -> bool:
    """Returns True if the input node is unvisited, and false otherwise.

    :param G: Input graph
    :type G: MultiGraph
    :param u: Input node
    :type u: int
    :return: True if node is unvisited, and false otherwise
    :rtype: bool
    """
    return G.nodes[u]['visited'] is False

def is_edge_to_unvisited_node(G: nx.MultiGraph, e: Edge) -> bool:
    """Returns True if the edge ends at an unvisited node, and false otherwise.

    :param G: Input graph
    :type G: MultiGraph
    :param e: Input edge
    :type e: Edge
    :return: True if the edge leads to an unvisited node, and false otherwise
    :rtype: bool
    """
    return is_unvisited(G, e.v)

def mark_as_visited(G: nx.MultiGraph, n: int) -> None:
    """Marks the input node as visited.

    :param G: Input graph
    :type G: MultiGraph
    :param n: Input node
    :type n: int
    """
    G.add_node(n, visited=True)

def parallel_edges_between_u_and_v(G: nx.MultiGraph, u: int, v: int) -> List[Edge]:
    """Returns a list of all edges between two input nodes.

    :param G: Input graph
    :type G: MultiGraph
    :param n: Input node
    :param u: First node
    :type u: int
    :param v: Second node
    :type v: int
    :return: List of all edges between the two nodes
    :rtype: List[Edge]
    """
    edges = []
    k = 0
    while G.has_edge(u, v, key=k):
        edges.append(Edge(u, v, k, G.edges[u, v, k]['length']))
        k += 1
    return edges

def get_edges_from_path(G: nx.MultiGraph, path: List[int]) -> List[Edge]:
    """Translates a path given as a list of nodes into a list of edges.
    If there are parallel edges, always use the shortest edge available.

    :param G: Input graph
    :type G: MultiGraph
    :param path: Path given as a list of nodes.
    :type path: List[int]
    :return: List of edges corresponding to the shortest path visiting the same nodes in order.
    :rtype: List[Edge]
    """

    path_edges = []
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        edges = parallel_edges_between_u_and_v(G, u, v)
        if len(edges) == 1:
            path_edges += edges
        else:
            path_edges += edge.shortest_edge(edges)

    return path_edges

