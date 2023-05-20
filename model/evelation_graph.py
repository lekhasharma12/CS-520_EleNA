import osmnx as ox
import networkx as nx
import requests
import json


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

    # # iterate over the batches and retrieve elevation data
    # for batch in batches:
    #     locations_str = '|'.join([f"{lat},{lon}" for lat, lon in batch])
    #
    #     # update url
    #     updated_url = url + locations_str
    #
    #     # request to the OpenTopoData API
    #     response = requests.get(updated_url)
    #     data = response.json()
    #
    #     # elevation data from the response
    #     for result in data['results']:
    #         elevation = result['elevation']
    #         elevation_data.append({"elevation":elevation})
    #
    # print("Elevation data:", elevation_data)
    # with open("elevation_data_puffers.txt", "w") as output:
    #     output.write(str(elevation_data))

    elevation_file = open("elevation_data.txt", "r")
    elevation_data = elevation_file.read()
    elevation_data = json.loads(elevation_data)
    return elevation_data


def get_elevation_graph(graph, elevation_data):
    elevation_dict = {}
    for node, elevation in zip(graph.nodes, elevation_data):
        elevation_dict.update({node: elevation})

    # elevation_diff_dict = {}
    # for edge in graph.edges:
    #     diff = elevation_dict[edge]
    #     elevation_diff_dict.update({})

    nx.set_node_attributes(graph, elevation_dict)
    return graph


