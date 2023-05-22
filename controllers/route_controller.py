import osmnx as ox
import networkx as nx
from models.route import Route
from utils.utils import validate_for_errors
from flask import request
from flask import jsonify
import time

from services.route_finder import dijkstras_with_elevation, astar_with_elevation


def index():
    return "Hello, this is EleNA"


def shortest_path():
    city, state = "Amherst", "MA"

    data = request.json
    print(data)
    source, destination, elevation_type, percent_increase, mode = data["source"]["description"], data["destination"]["description"], data["elevation_type"], int(data["percent_increase"]), data["mode"]

    st = time.time()
    error, error_msg = validate_for_errors(source, destination, elevation_type, percent_increase, mode)

    if error:
        print(error_msg)
        # error_msg = {"error": error_msg}
        return jsonify(error_msg)
    else:
        route = Route(source, destination, elevation_type, percent_increase, mode, city, state)

        # shortest_path = nx.shortest_path(route.graph, route.source_node, route.destination_node, weight='length')

        # get shortest path with given conditions using dijkstras and astar
        result_dijkstras = dijkstras_with_elevation(route.graph, route.source_node, route.destination_node, route.elevation_type, route.percent_increase, route.mode)
        result_astar = astar_with_elevation(route.graph, route.source_node, route.destination_node, route.elevation_type, route.percent_increase, route.mode)

        min_dijkstras, max_dijkstras = result_dijkstras['elevation']
        min_astar, max_astar = result_astar['elevation']

        # check which algo gives minimum or maximum elevation variation
        if elevation_type == 'min':
            result = result_astar if (max_astar - min_astar) < (max_dijkstras - min_dijkstras) else result_dijkstras
        else:
            result = result_astar if (max_astar - min_astar) > (max_dijkstras - min_dijkstras) else result_dijkstras

        # route_map = ox.plot_route_folium(route.graph, shortest_path, color='#000000', opacity=0.5)
        # route_map = ox.plot_route_folium(route.graph, result_dijkstras['path'], route_map=route_map, color='#0000ff', opacity=0.5)
        # route_map = ox.plot_route_folium(route.graph, result_astar['path'], route_map=route_map, color='#ff0000', opacity=0.5)
        # route_map.save('route.html')

        # print(result)
        et = time.time()
        print("Time elapsed ", et-st)
        return jsonify(result)
