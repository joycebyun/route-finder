import copy
import networkx as nx


class Route():
    def __init__(self, G):

        self.G = copy.deepcopy(G)

        # set all nodes to have attribute 'visited' = False
        nx.set_node_attributes(self.G, name='visited', values=False)

        self.nodes = []
        self.edges = []
        self.distance = 0
