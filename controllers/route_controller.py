import osmnx as ox
import networkx as nx
from models.route import Route
from utils.utils import validate_for_errors
from flask import request
from flask import jsonify
import time

from services.route_finder import dijkstras, astar


def index():
    return "Hello, this is EleNA"


# def shortest_path(source, destination, elevation_type, percent_increase, mode, city, state):
def shortest_path():
    city, state = "Amherst", "MA"

    data = request.json
    print(data)
    source, destination, elevation_type, percent_increase, mode = data["source"], data["destination"], data["elevation_type"], int(data["percent_increase"]), data["mode"]

    st = time.time()
    error, error_msg = validate_for_errors(source, destination, elevation_type, percent_increase, mode)

    if error:
        print(error_msg)
        return error_msg
    else:
        route = Route(source, destination, elevation_type, percent_increase, mode, city, state)

        shortest_path = nx.shortest_path(route.graph, route.source_node, route.destination_node, weight='length')

        result_dijkstras = dijkstras(route.graph, route.source_node, route.destination_node)
        result_astar = astar(route.graph, route.source_node, route.destination_node)
        # print(result_dijkstras['path'])
        # print("astar path", result_astar['path'])
        # print(result_dijkstras['elevation'])
        # print(result_dijkstras['distance'])

        if elevation_type == 'min':
            result = result_astar if result_astar['elevation'] < result_dijkstras['elevation'] else result_dijkstras
        else:
            result = result_astar if result_astar['elevation'] > result_dijkstras['elevation'] else result_dijkstras

        route_map = ox.plot_route_folium(route.graph, shortest_path, color='#000000', opacity=0.5)
        route_map = ox.plot_route_folium(route.graph, result_dijkstras['path'], color='#0000ff', opacity=0.5)
        route_map = ox.plot_route_folium(route.graph, result_astar['path'], route_map=route_map, color='#ff0000', opacity=0.5)
        route_map.save('route.html')

        et = time.time()
        print("Time elapsed ", et-st)
        return jsonify(result)
