import copy
from edge import Edge
import edge
from route import Route
import networkx as nx
from typing import List, Tuple
import graph_utils


class RouteFinder():
    def __init__(self, G: nx.MultiGraph, source: int, max_distance: float):
        """Create an instance of RouteFinder, which is uniquely identified
        by a graph, a source node (which must also be the ending node),
        and a maximum allowed total distance for a generated route.

        :param G: Input graph
        :type G: MultiGraph
        :param source: Starting node (which will also be the ending node)
        :type source: int
        :param max_distance: Maximum distance for the route
        :type max_distance: float
        """
        self.G = copy.deepcopy(G)
        self.source: int = source
        self.max_distance: float = max_distance

        self.distance_from_source = None

    def get_viable_edges(self, route: Route) -> List[Edge]:
        """From the last node of the input route, get a list of incident edges
        that end at viable nodes. A viable node is defined as one that we can go to
        and still get back to the route's starting node with a total distance
        less than or equal to the route's allowed maximum distance.

        :param route: Route traversed so far
        :type route: Route
        :return: A list of incident edges that start at the route's last node and ends at a viable node
        :rtype: List[Edge]
        """

        u = route.nodes[-1]
        incident_edges = graph_utils.get_incident_edges(self.G, u)

        viable = []
        for e in incident_edges:
            if (route.distance + e.length
                + nx.shortest_path_length(self.G,
                                          source=e.v,
                                          target=self.source,
                                          weight='length')) <= self.max_distance:
                viable.append(e)

        return viable

    def _recursive_brute_force(self, route: Route, routes: List[Route]) -> None:
        viable_edges = self.get_viable_edges(route)
        if viable_edges:
            for e in viable_edges:
                route.add_edge(e)
                self._recursive_brute_force(route, routes)
                route.pop_edge()  # backtracking
        else:
            routes.append(copy.deepcopy(route))

    def brute_force(self) -> List[Route]:
        """Use an algorithm based on Depth First Search (DFS) to find all possible routes
        that start from (and end at) the route finder's starting node and has a
        total distance less than the route finder's maximum distance.

        :return: List of all possible routes
        :rtype: List[Route]
        """
        all_routes: List[Route] = []  # store all routes found through brute force

        route = Route()
        route.nodes.append(self.source)
        self._recursive_brute_force(route, all_routes)

        # Important caveat: brute force here will always keep going as long
        # as it is possible without the distance being too large. So routes
        # that could end early (because they go back to the start node) are not
        # separately included.

        return all_routes

    #@staticmethod
    #def count_unique_nodes(route: Route) -> int:
    #    return len(set(route.nodes))

    #@staticmethod
    #def maximize_new_nodes(routes: List[Route]) -> List[Route]:
        # return routes that have the largest number of new nodes
    #    max_new_nodes = max([__class__.count_unique_nodes(r) for r in routes])
    #    return [r for r in routes if __class__.count_unique_nodes(r) == max_new_nodes]

    def path_to_next_node(self, route: Route) -> List[int]:
        """Finds the nearest viable unvisited node, and returns the path to it.
        If there are no viable unvisited nodes, returns a path to the nearest viable visited node.

        :param route: Route traversed so far
        :type route: Route
        :return: Path to the nearest viable unvisited node, if it exists. If no such node exists, returns a path to the nearest viable visited node.
        :rtype: List[int]
        """

        # find the distance of every node from the source (out to max dist/2)
        if self.distance_from_source is None:
            self.distance_from_source = nx.single_source_dijkstra_path_length(self.G, self.source,
                                                                              cutoff=self.max_distance/2,
                                                                              weight='length')

        # find the distance of every node from current node u
        u = route.nodes[-1]
        distance_from_u, path_from_u = nx.single_source_dijkstra(self.G, u, target=None,
                                                                 cutoff=self.max_distance - route.distance,
                                                                 weight='length')
        del distance_from_u[u]  # we do not allow going from u to u
        distance_from_u = dict(sorted(distance_from_u.items(), key=lambda item: item[1]))

        closest_viable_visited_node = None
        for v in distance_from_u.keys():
            if (v in self.distance_from_source) and (route.distance + distance_from_u[v] + self.distance_from_source[v] <= self.max_distance):
                if graph_utils.is_unvisited(self.G, v):
                    return path_from_u[v]
                elif closest_viable_visited_node is None:
                    closest_viable_visited_node = v

        return path_from_u[closest_viable_visited_node]

    def _recursive_greedy_nearest(self, route: Route) -> None:
        viable_edges = self.get_viable_edges(route)

        # if none of the adjacent nodes are viable, route must be completed
        if len(viable_edges) == 0:
            return

        # check whether any viable incident edges go to an unvisited node
        edges_to_unvisited = [e for e in viable_edges if graph_utils.is_edge_to_unvisited_node(self.G, e)]

        if edges_to_unvisited:
            e = edge.shortest_edge(edges_to_unvisited)
            route.add_edge(e)
            graph_utils.mark_as_visited(self.G, e.v)
        else:
            # if none of the adjacent nodes are unvisited, look further for the next node
            path = self.path_to_next_node(route)
            edges = graph_utils.get_edges_from_path(self.G, path)
            for e in edges:
                route.add_edge(e)
                graph_utils.mark_as_visited(self.G, e.v)

        self._recursive_greedy_nearest(route)

    def greedy_nearest(self) -> Route:
        """Generates a route by using a greedy algorithm: the next node is always chosen
        to the nearest viable unvisited node whenever possible, and if no such node exists,
        choose the next node to be the nearest viable visited node.

        :return: Route found using a greedy algorithm
        :rtype: Route
        """
        route = Route()
        route.nodes.append(self.source)
        graph_utils.mark_as_visited(self.G, self.source)
        self._recursive_greedy_nearest(route)
        return route
