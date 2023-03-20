import copy
from edge import Edge
import edge
from route import Route
import networkx as nx
from typing import List, Tuple


class RouteFinder():
    def __init__(self, G, source, max_distance):
        self.G = copy.deepcopy(G)
        self.source: int = source
        self.max_distance: float = max_distance

        # could cutoff here be max/2?
        self.distance_to_source = nx.single_source_dijkstra_path_length(self.G, self.source,
                                                                        cutoff=self.max_distance,
                                                                        weight='length')

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

    def recursive_brute_force(self, route: Route, routes: List[Route]) -> None:
        viable_edges = self.get_viable_edges(route)
        if viable_edges:
            for e in viable_edges:
                route.add_edge(e)
                self.recursive_brute_force(route, routes)
                route.remove_edge()  # backtracking
        else:
            routes.append(copy.deepcopy(route))

    def brute_force(self) -> List[Route]:
        all_routes: List[Route] = []  # store all routes found through brute force

        route = Route()
        route.nodes.append(self.source)
        self.recursive_brute_force(route, all_routes)

        return all_routes

    #@staticmethod
    #def count_unique_nodes(route: Route) -> int:
    #    return len(set(route.nodes))

    #@staticmethod
    #def maximize_new_nodes(routes: List[Route]) -> List[Route]:
        # return routes that have the largest number of new nodes
    #    max_new_nodes = max([__class__.count_unique_nodes(r) for r in routes])
    #    return [r for r in routes if __class__.count_unique_nodes(r) == max_new_nodes]

    def is_unvisited(self, u: int) -> bool:
        return self.G.nodes[u]['visited'] is False

    def to_unvisited_node(self, e: Edge) -> bool:
        return self.is_unvisited(e.v)

    def mark_as_visited(self, n: int) -> None:
        self.G.add_node(n, visited=True)

    def path_to_nearest_unvisited_node(self, route: Route) -> List[int]:
        # attempts to find the closest unvisited (viable) node.
        # if there is no viable node that is unvisited, 
        # return the closest visited (viable) node.

        u = route.nodes[-1]

        distance, path = self.single_source_dijkstra(route)
        del distance[u]
        distance = dict(sorted(distance.items(), key=lambda item: item[1]))

        closest_visited_node = None
        for v in distance.keys():
            viable = (route.distance + distance[v]
                      + self.distance_to_source[v] <= self.max_distance)
            if viable:
                if self.is_unvisited(v):
                    return path[v]
                elif closest_visited_node is None:
                    closest_visited_node = v

        return path[closest_visited_node]

    def single_source_dijkstra(self, route: Route):
        # wrapper for nx.single_source_dijkstra
        # get distances and paths to viable nodes accessible from current node
        u = route.nodes[-1]
        distance, path = nx.single_source_dijkstra(self.G, u, target=None,
                                                   cutoff=self.max_distance - route.distance,
                                                   weight='length')
        return distance, path

    def all_edges_between_u_and_v(self, u: int, v: int) -> List[Edge]:
        edges = []
        k = 0
        while self.G.has_edge(u, v, key=k):
            edges.append(Edge(u, v, k, self.G.edges[u, v, k]['length']))
            k += 1
        return edges

    def get_edges_from_path(self, path: List[int]) -> List[Edge]:
        # always use the shortest edge available, if there are parallel edges

        path_edges = []
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            edges = self.all_edges_between_u_and_v(u, v)
            if len(edges) == 1:
                path_edges += edges
            else:
                path_edges += edge.shortest_edge(edges)

        return path_edges

    def recursive_greedy_nearest(self, route: Route) -> None:
        viable_edges = self.get_viable_edges(route)

        # if none of the adjacent nodes are viable, route must be completed
        if len(viable_edges) == 0:
            return

        # check whether any incident edges go to an unvisited node
        edges_to_unvisited = [e for e in viable_edges if self.to_unvisited_node(e)]

        if edges_to_unvisited:
            e = edge.shortest_edge(edges_to_unvisited)
            route.add_edge(e)
            self.mark_as_visited(e.v)
        else:
            # none of the adjacent nodes are unvisited,
            # so find the nearest viable unvisited node
            path = self.path_to_nearest_unvisited_node(route)
            edges = self.get_edges_from_path(path)
            for e in edges:
                route.add_edge(e)
                self.mark_as_visited(e.v)

        self.recursive_greedy_nearest(route)

    def greedy_nearest(self) -> Route:
        route = Route()
        route.nodes.append(self.source)
        self.mark_as_visited(self.source)
        self.recursive_greedy_nearest(route)
        return route
