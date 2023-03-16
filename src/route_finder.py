import copy
from edge import Edge
from route import Route
import networkx as nx
from typing import List


class RouteFinder():
    def __init__(self, G, source, max_distance):
        self.G = copy.deepcopy(G)
        self.source: int = source
        self.max_distance: float = max_distance

        self.all_routes: List[Route] = []  # store all routes found through brute force

    def get_incident_edges(self, u: int) -> List[Edge]:
        # get list of edges incident on u, where each edge is a tuple (u,v,k,length)
        return [Edge(*e) for e in self.G.edges(nbunch=u, data='length', keys=True)]

    def get_viable_edges(self, route: Route) -> List[Edge]:
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

    def recursive_brute_force(self, route: Route) -> None:
        viable_edges = self.get_viable_edges(route)

        if viable_edges:
            for e in viable_edges:
                route.edges.append(e)
                route.nodes.append(e.v)
                route.distance += e.length

                self.recursive_brute_force(route)

                # backtrack
                route.edges.pop()
                route.nodes.pop()
                route.distance -= e.length
        else:
            self.all_routes.append(copy.deepcopy(route))

    def brute_force(self) -> None:
        temp_route = Route()
        temp_route.nodes.append(self.source)
        self.recursive_brute_force(temp_route)

    @staticmethod
    def count_unique_nodes(route: Route) -> int:
        return len(set(route.nodes))

    @staticmethod
    def maximize_new_nodes(routes: List[Route]) -> List[Route]:
        # return routes that have the largest number of new nodes
        max_new_nodes = max([__class__.count_unique_nodes(r) for r in routes])
        return [r for r in routes if __class__.count_unique_nodes(r) == max_new_nodes]
