import osmnx as ox
from utils.utils import get_elevation_data, add_elevation_data


# method to validate the type of elevation user wants,
# the percent increase for shortest path is within 100% and
# the mode selected by user is either waling or biking
def validate_params(elevation_type, percent_increase, mode):
    if elevation_type not in ['max', 'min']:
        return False
    if percent_increase > 100:
        return False
    if mode not in ['walk', 'bike']:
        return False
    return True


# method to get the elevation data of the graph and assign it to each node respectively
def get_elevated_graph(source, mode):
    graph = ox.graph_from_point(source, dist=1000, dist_type='bbox', network_type=mode)
    elevation_data = get_elevation_data(graph)
    return add_elevation_data(graph, elevation_data)


# Route class that models all the input data from user for their desired route
# as well as the graph and resulting shortest path based on user's criteria
class Route:
    def __init__(self, source, destination, elevation_type, percent_increase, mode):
        # validate the parameters
        validated = validate_params(elevation_type, percent_increase, mode)

        # if validated, assign to route class, else assign default value
        if validated:
            self.elevation_type = elevation_type
            self.percent_increase = percent_increase
            self.mode = mode
        else:
            self.elevation_type = 'min'
            self.percent_increase = 50
            self.mode = 'walk'
        self.source = source
        self.destination = destination
        self.graph = get_elevated_graph(source, mode)
        self.distance = 0
        self.elevation = 0
        self.shortest_path = []


