import osmnx as ox
import networkx as nx
import requests
import json
import os
import pickle
import math


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

    with open("elevation_data.txt", "w") as output:
        output.write(str(elevation_data))

    # elevation_file = open("elevation_data_100kms.txt", "r")
    # elevation_data = elevation_file.read()
    # elevation_data = json.loads(elevation_data)
    print('get_elevation_data - Done')
    return elevation_data


def add_elevation_data(graph):
    elevation_data = get_elevation_data(graph)
    elevation_dict = {}
    for node, elevation in zip(graph.nodes, elevation_data):
        elevation_dict.update({node: elevation})

    nx.set_node_attributes(graph, elevation_dict)
    print('add_elevation_data - Done')
    return graph


def get_place_mode_graph(city, state, mode):
    path = f"./graphs/{city}_{mode}.pickle"
    graph = nx.Graph()
    if os.path.isfile(path):
        print("Graph already saved, loading")
        graph = pickle.load(open(path, 'rb'))
    else:
        print("Graph not saved, fetching from osmnx")
        query = city + ", " + state
        graph = ox.graph_from_place(query, network_type=mode)
        graph = add_elevation_data(graph)
        pickle.dump(graph, open(path, 'wb'))

    print('get_graph_for_place - Done')
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
    if math.dist(source_coordinates, destination_coordinates) > 10000:
        return True, "Source and destination are further than 10km. Please enter places within 10km radius."
    if elevation_type not in ['max', 'min']:
        return True, "Elevation Type is incorrect. Please select either minimum or maximum elevation"
    if percent_increase > 100:
        return True, "Percentage increase in the shortest route is greater than 100. Please select a value between " \
                      "0-100"
    if mode not in ['walk', 'bike']:
        return True, "Mode of transport is incorrect. Please select either walking or biking"
    return False, ''


def get_coordinates_from_node(graph, node):
    return graph.nodes[node]['x'], graph.nodes[node]['y']


def get_node_from_coordinates(graph, coordinates):
    return ox.nearest_nodes(graph, coordinates[1], coordinates[0])


def distance_till_dest(graph, node, dest):
    node_coordinates = get_coordinates_from_node(graph, node)
    dest_coordinates = get_coordinates_from_node(graph, dest)
    return math.dist(node_coordinates, dest_coordinates)


def make_graph(source, mode):
    path = f"./graphs/{source}_{mode}.pickle"
    source_coordinates = ox.geocode(source)
    if os.path.isfile(path):
        print("Graph already saved, loading")
        graph = pickle.load(open(path, 'rb'))
    else:
        print("Graph not saved, fetching from osmnx")
        graph = ox.graph_from_point(source_coordinates, dist=15000, dist_type='bbox', network_type='walk')
        graph = add_elevation_data(graph)
        pickle.dump(graph, open(path, 'wb'))
    print("make_graph - Done")
    return graph


