from utils.utils import get_place_mode_graph, get_node_from_coordinates


# Route class that models all the input data from user for their desired route
# as well as the graph and resulting shortest path based on user's criteria
class Route:
    def __init__(self, source, destination, elevation_type, percent_increase, mode, city, state):
        self.elevation_type = elevation_type
        self.percent_increase = percent_increase
        self.mode = mode
        self.elevation_type = 'min'
        self.percent_increase = 50
        self.mode = 'walk'
        self.graph = get_place_mode_graph(city, state, mode)
        self.source_node = get_node_from_coordinates(self.graph, source)
        self.destination_node = get_node_from_coordinates(self.graph, destination)
        self.distance = 0
        self.elevation = 0
        self.shortest_path = []


