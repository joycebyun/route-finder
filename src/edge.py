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


def total_length(edges: List[Edge]) -> float:
    total: float = 0
    for e in edges:
        total += e.length
    return total


def shortest_edge(edges: List[Edge]) -> Edge:
    return min(edges, key=lambda e: e.length)
