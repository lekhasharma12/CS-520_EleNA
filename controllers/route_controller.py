import osmnx as ox
from models.route import Route
from utils.utils import validate_for_errors

from services.route_finder import dijkstras, astar


def index():
    return "Hello, this is EleNA"

def shortest_path(source, destination, elevation_type, percent_increase, mode, city, state):

    source_coordinates = ox.geocode(source)
    destination_coordinates = ox.geocode(destination)

    error, error_msg = validate_for_errors(elevation_type, percent_increase, mode)

    if error:
        return error_msg
    else:
        route = Route(source_coordinates, destination_coordinates, elevation_type, percent_increase, mode, city, state)

        # route1 = nx.shortest_path(route.graph, route.source_node, route.destination_node, weight='length')
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

        route_map = ox.plot_route_folium(route.graph, result_dijkstras['path'], color='#0000ff', opacity=0.5)
        route_map = ox.plot_route_folium(route.graph, result_astar['path'], route_map=route_map, color='#ff0000', opacity=0.5)
        route_map.save('route.html')

        return result['elevation'], result['distance'], result['distance']
