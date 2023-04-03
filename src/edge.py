from typing import NamedTuple, List


class Edge(NamedTuple):
    """Subclass of ``typing.NamedTuple`` that holds (u, v, key, length) 
    for identifying an edge.
    """
    u: int
    v: int
    key: int
    length: float

    def __str__(self):
        return str((self.u, self.v, self.key, self.length))

    def __repr__(self):
        return self.__str__()

    def flip(self) -> "Edge":
        """Return a new edge with the u and v nodes switched.

        :return: A new edge that is the same as the existing edge, except with u and v nodes switched.
        :rtype: Edge
        """
        return Edge(self.v, self.u, self.key, self.length)


def total_length(edges: List[Edge]) -> float:
    """Calculate the total length for a list of edges.

    :param edges: A list of edges
    :type edges: List[Edge]
    :return: Sum of the lengths of all edges
    :rtype: float
    """
    total: float = 0
    for e in edges:
        total += e.length
    return total


def shortest_edge(edges: List[Edge]) -> Edge:
    """Return the shortest edge from a list of edges.

    :param edges: A list of edges
    :type edges: List[Edge]
    :return: The shortest edge
    :rtype: Edge
    """
    return min(edges, key=lambda e: e.length)
