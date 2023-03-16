import copy
from edge import Edge
from route import Route
import networkx as nx

class RouteFinder():
    def __init__(self, G, source, max_distance):
        self.G = copy.deepcopy(G)
        self.source: int = source
        self.max_distance: float = max_distance

    def get_incident_edges(self, u):
        # get list of edges incident on u, where each edge is a tuple (u,v,k,length)
        return [Edge(*e) for e in self.G.edges(nbunch=u, data='length', keys=True)]

    def get_viable_edges(self, route: Route):
        # a viable edge is an incident edge that we could traverse, 
        # and still get back to source with distance <= max_distance

        u = route.nodes[-1]
        incident_edges = self.get_incident_edges(u)

        viable = []
        for e in incident_edges:
            if (route.distance + e.length
                + nx.shortest_path_length(self.G,
                                          source=e.v,
                                          target=self.source,
                                          weight='length')) <= self.max_distance:
                viable.append(e)

        return viable
