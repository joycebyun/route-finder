from typing import NamedTuple, List


class Edge(NamedTuple):
    u: int
    v: int
    key: int
    length: float

    def __str__(self):
        return str((self.u, self.v, self.key, self.length))

    def __repr__(self):
        return self.__str__()

    def flip(self) -> "Edge":
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
