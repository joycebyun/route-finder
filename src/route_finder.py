import copy
from edge import Edge


class RouteFinder():
    def __init__(self, G, source, max_distance):
        self.G = copy.deepcopy(G)
        self.source: int = source
        self.max_distance: float = max_distance

    def get_incident_edges(self, u):
        # get list of edges incident on u, where each edge is a tuple (u,v,k,length)
        return [Edge(*e) for e in self.G.edges(nbunch=u, data='length', keys=True)]

