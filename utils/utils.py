import osmnx as ox
import networkx as nx
import requests
import os
import pickle
import math
import geopy.distance


# method to fetch elevation data from open topo data for all nodes i the graph
def get_elevation_data(graph):
    url = 'https://api.opentopodata.org/v1/aster30m?locations='
    locations = []
    locations += [(data['y'], data['x']) for node, data in graph.nodes(data=True)]

    # batch size for each request
    batch_size = 100

    # list to store elevation data
    elevation_data = []

    # locations split into batches
    batches = [locations[i:i + batch_size] for i in range(0, len(locations), batch_size)]
    print("Number of batches: ", len(batches))

    # iterate over the batches and retrieve elevation data
    for batch in batches:
        locations_str = '|'.join([f"{lat},{lon}" for lat, lon in batch])

        # update url
        updated_url = url + locations_str

        # request to the OpenTopoData API
        response = requests.get(updated_url)
        data = response.json()

        # elevation data from the response
        for result in data["results"]:
            elevation = result["elevation"]
            elevation_data.append({"elevation": elevation})

    print('get_elevation_data - Done')
    return elevation_data


# method to add elevation as an attribute for each node in the graph and return the graph
def add_elevation_data(graph):
    elevation_data = get_elevation_data(graph)
    elevation_dict = {}
    for node, elevation in zip(graph.nodes, elevation_data):
        elevation_dict.update({node: elevation})

    nx.set_node_attributes(graph, elevation_dict)
    print('add_elevation_data - Done')
    return graph


# method to validate the type of elevation user wants,
# the percent increase for shortest path is within 100% and
# the mode selected by user is either waling or biking
def validate_for_errors(source, destination, elevation_type, percent_increase, mode):
    source_coordinates = ox.geocode(source)
    destination_coordinates = ox.geocode(destination)
    if len(source_coordinates) != 2:
        return True, "Source coordinates are not correct."
    if len(destination_coordinates) != 2:
        return True, "Destination coordinates are not correct."
    if geopy.distance.geodesic(source_coordinates, destination_coordinates).km > 10:
        return True, "Source and destination are further than 10km. Please enter places within 10km radius."
    else:
        print("distance between the points, ", geopy.distance.geodesic(source_coordinates, destination_coordinates).km)
    if elevation_type not in ['max', 'min']:
        return True, "Elevation Type is incorrect. Please select either minimum or maximum elevation"
    if percent_increase > 100 and percent_increase < 0:
        return True, "Percentage increase in the shortest route is incorrect. Please select a value between " \
                      "0-100"
    if mode not in ['walk', 'bike']:
        return True, "Mode of transport is incorrect. Please select either walking or biking"
    return False, ''


def get_coordinates_from_node(graph, node):
    return graph.nodes[node]['x'], graph.nodes[node]['y']


def get_node_from_coordinates(graph, coordinates):
    if graph is None:
        print("WHHOPS")
    return ox.nearest_nodes(graph, coordinates[1], coordinates[0])


def distance_till_dest(graph, node, dest):
    node_coordinates = get_coordinates_from_node(graph, node)
    dest_coordinates = get_coordinates_from_node(graph, dest)
    return math.dist(node_coordinates, dest_coordinates)


def elevation_diff_with_dest(graph, node, dest):
    return graph.nodes[node]['elevation'] - graph.nodes[dest]['elevation']

# method to make graph for a given city and mode of transport
def get_place_mode_graph(city, state, mode):
    path = f"./graphs/{city}_{mode}.pickle"

    # check if graph is already present, load if present from files
    if os.path.isfile(path):
        print("Graph already saved, loading")
        graph = pickle.load(open(path, 'rb'))

    # if not present get graph from osmnx
    else:
        print("Graph not saved, fetching from osmnx")
        query = city + ", " + state
        graph = ox.graph_from_place(query, network_type=mode)
        graph = add_elevation_data(graph)
        pickle.dump(graph, open(path, 'wb'))

    print('get_place_mode_graph - Done')
    return graph


def get_radius_mode_graph(source, mode):
    path = f"./graphs/{source}_{mode}.pickle"
    source_coordinates = ox.geocode(source)

    # check if graph is already present, load if present from files
    if os.path.isfile(path):
        print("Graph already saved, loading")
        graph = pickle.load(open(path, 'rb'))

    # if not present get graph from osmnx
    else:
        print("Graph not saved, fetching from osmnx")
        graph = ox.graph_from_point(source_coordinates, dist=10000, dist_type='bbox', network_type='walk')
        graph = add_elevation_data(graph)
        pickle.dump(graph, open(path, 'wb'))
    print("get_radius_mode_graph - Done")
    return graph

# method to make graph with 10 km radius from source and mode of transport
def make_graph(source, dest, mode):
    source_list = source.replace(" ", "").split(",")
    dest_list = dest.replace(" ", "").split(",")
    if dest_list[-3] == source_list[-3]:
        print("Cities match, getting graph for city")
        graph = get_place_mode_graph(dest_list[-3], dest_list[-2], mode)
    else:
        print("Cities do not match, getting graph of 10 km radius from source")
        graph = get_radius_mode_graph(source, mode)
    return graph


# method to get total distance of a path
def get_path_distance(graph, path):
    distance = 0
    for i in range(len(path)-1):
        edge_data = graph.edges[path[i], path[i+1], 0]
        distance += edge_data['length']
    return distance/1000


def get_max_elevation(graph, path):
    ele = 0
    for node in path:
        ele = graph.nodes[node]['elevation'] if graph.nodes[node]['elevation'] > ele else ele
    return ele


def get_min_elevation(graph, path):
    ele = math.inf
    for node in path:
        ele = graph.nodes[node]['elevation'] if graph.nodes[node]['elevation'] < ele else ele
    return ele


def get_time_for_mode(distance, mode):
    if mode == 'walk':
        return distance/4
    else:
        return distance/20
