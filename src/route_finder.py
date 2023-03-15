import copy


class RouteFinder():
    def __init__(self, G, source, max_distance):
        self.G = copy.deepcopy(G)
        self.source: int = source
        self.max_distance: float = max_distance

