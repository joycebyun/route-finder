from typing import List
from edge import Edge


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
