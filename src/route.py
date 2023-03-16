import copy
import networkx as nx  # type: ignore
from typing import List
from edge import Edge


class Route():
    def __init__(self, G) -> None:

        self.G = copy.deepcopy(G)

        # set all nodes to have attribute 'visited' = False
        nx.set_node_attributes(self.G, name='visited', values=False)

        self.nodes: List[int] = []
        self.edges: List[Edge] = []
        self.distance: float = 0

