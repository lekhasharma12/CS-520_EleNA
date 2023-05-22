from utils.utils import get_place_mode_graph, get_node_from_coordinates, make_graph
import osmnx as ox


# Route class that models all the input data from user for their desired route
# as well as the graph and resulting shortest path based on user's criteria
class Route:
    def __init__(self, source, destination, elevation_type, percent_increase, mode, city, state):
        self.elevation_type = elevation_type
        self.percent_increase = percent_increase
        self.mode = mode
        self.graph = make_graph(source, destination, mode)
        source_coordinates = ox.geocode(source)
        destination_coordinates = ox.geocode(destination)
        self.source_node = get_node_from_coordinates(self.graph, source_coordinates)
        self.destination_node = get_node_from_coordinates(self.graph, destination_coordinates)
        self.distance = 0
        self.elevation = 0
        self.shortest_path = []


