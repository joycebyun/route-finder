from typing import List
from edge import Edge
import graph_utils
import networkx as nx


class Route():
    """Route consists of a list of nodes, a list of edges, and a total distance.
    Strictly, a list of edges are all that is needed to uniquely identify a route,
    but we also keep a list of nodes and the total distance out of convenience.

    :ivar nodes: A list of integers that label the nodes visited
    :ivar edges: A list of ``Edge`` objects that label the edges traversed
    :ivar distance: The total distance of the route
    """
    def __init__(self) -> None:
        """Initialize an empty route with no nodes, no edges, and zero distance.
        """
        self.nodes: List[int] = []
        self.edges: List[Edge] = []
        self.distance: float = 0

        self._is_new_node: List[bool] = []

    def __str__(self):
        return str(self.nodes)

    def add_edge(self, e: Edge):
        """Add an edge to the end of the route.

        :param e: The edge to add
        :type e: Edge
        """
        self.nodes.append(e.v)
        self.edges.append(e)
        self.distance += e.length

    def pop_edge(self):
        """Remove the last edge from the route.
        """
        self.nodes.pop()
        e = self.edges.pop()
        self.distance -= e.length

    def _get_node_positions(self):
        """Return a dict where the (key, value) pairs are (node id, list of positions where node
        appears in route).
        """
        node_positions = {}
        for i, n in enumerate(self.nodes):
            if n in node_positions:
                node_positions[n].append(i)
            else:
                node_positions[n] = [i]
        return node_positions

    def _set_is_new_node(self, G: nx.MultiGraph):
        """Return a list of bools where the i-th element is True if the corresponding i-th node in
        the route is being visited for the first time, and False otherwise.

        :param G: Original graph, before the route is run
        :type G: MultiGraph
        """
        self._is_new_node = []
        visited_nodes = set()
        for n in self.nodes:
            if graph_utils.is_visited(G, n):
                self._is_new_node.append(False)
            else:
                if n in visited_nodes:
                    self._is_new_node.append(False)
                else:
                    self._is_new_node.append(True)
                    visited_nodes.add(n)

    def prune(self, G: nx.MultiGraph):

        node_positions = self._get_node_positions()
        print(node_positions)

        self._set_is_new_node(G)
        print(self._is_new_node)

        pruned_route = []

        i = 0
        while i < len(self.nodes):
            print(i)
            n = self.nodes[i]
            pruned_route.append(n)
            node_positions[n].pop(0)
            if len(node_positions[n]) > 0:
                j = node_positions[n][-1]
                k = i + 1
                while k < j:
                    if self._is_new_node[k]:
                        break
                    k = k + 1
                if k == j:
                    # pop(0) for nodes i+1 to j, inclusive
                    for a in range(i + 1, j + 1):
                        node_positions[self.nodes[a]].pop(0)
                    i = j + 1
                else:
                    # pop(0) for nodes i+1 to k-1, inclusive
                    for a in range(i + 1, k):
                        node_positions[self.nodes[a]].pop(0)
                    i = k
            else:
                i = i + 1

        print(pruned_route)
        print(node_positions)  # should only have empty lists as values for all keys

        return pruned_route
