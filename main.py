import osmnx as ox
import networkx as nx
from model.evelation_graph import get_elevation_data, get_elevation_graph
from controller.route_finder import *


def get_shortest_path(source, destination):    

    source_location = ox.geocode(source)
    destination_location = ox.geocode(destination)

    graph = ox.graph_from_point(source_location, dist=1000, dist_type='bbox', network_type='all')

    source_node = ox.nearest_nodes(graph, source_location[1], source_location[0])
    destination_node = ox.nearest_nodes(graph, destination_location[1], destination_location[0])

    elevation_data = get_elevation_data(graph)
    elevation_graph = get_elevation_graph(graph, elevation_data)

    route1 = nx.shortest_path(elevation_graph, source_node, destination_node, weight='length')
    result = dijkstras(elevation_graph, source_node, destination_node)
    result_astar = astar(elevation_graph, source_node, destination_node)
    print(route1)
    print(result['path'])
    print("astar path", result_astar['path'])

    route_map = ox.plot_route_folium(graph, route1, color='#ff0000', opacity=0.5)
    route_map_dijsktra = ox.plot_route_folium(graph, result['path'], route_map=route_map, color='#0000ff', opacity=0.5)
    route_map_dijsktra.save('route.html')
    route_map_astar = ox.plot_route_folium(graph, result_astar['path'], route_map=route_map, color='#000000', opacity=0.5)
    route_map_astar.save('route_astar.html')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    src = "147, Brittany Manor Drive, The Boulders, Mill Valley, Amherst, Hampshire County, Massachusetts, 01002"
    #dest = "University of Massachusetts Amherst, Mullins Way, Hadley, Hampshire County, Massachusetts, 01003"
    dest = "Puffers Pond, Amherst"
    get_shortest_path(src, dest)
