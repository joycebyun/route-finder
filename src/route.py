from typing import List
from edge import Edge


class Route():
    def __init__(self) -> None:
        self.nodes: List[int] = []
        self.edges: List[Edge] = []
        self.distance: float = 0

    def __str__(self):
        return str(self.nodes)

    def add_edge(self, e: Edge):
        self.nodes.append(e.v)
        self.edges.append(e)
        self.distance += e.length

    def remove_edge(self):
        self.nodes.pop()
        e = self.edges.pop()
        self.distance -= e.length
