import osmnx as ox
import networkx as nx
from model.route import Route

from controller.route_finder import dijkstras, astar


def distance(graph, path):
    dist = 0
    for i in range(len(path)-1):
        edge_data = graph.edges[path[i], path[i+1], 0]
        dist += edge_data['length']
    return dist

def get_shortest_path(source, destination, elevation_type, percent_increase, mode):

    source_location = ox.geocode(source)
    destination_location = ox.geocode(destination)

    route = Route(source_location, destination_location, elevation_type, percent_increase, mode)

    source_node = ox.nearest_nodes(route.graph, source_location[1], source_location[0])
    destination_node = ox.nearest_nodes(route.graph, destination_location[1], destination_location[0])

    route1 = nx.shortest_path(route.graph, source_node, destination_node, weight='length')
    result = dijkstras(route.graph, source_node, destination_node)
    result_astar = astar(route.graph, source_node, destination_node)
    dist = distance(route.graph, route1)
    print(route1)
    print(result['path'])
    # print("astar path", result_astar['path'])
    print(result['elevation'])
    print(result['distance'])
    print(dist)

    route_map = ox.plot_route_folium(route.graph, route1, color='#ff0000', opacity=0.5)
    route_map_dijsktra = ox.plot_route_folium(route.graph, result['path'], route_map=route_map, color='#0000ff', opacity=0.5)
    route_map_dijsktra.save('route.html')
    route_map_astar = ox.plot_route_folium(route.graph, result_astar['path'], route_map=route_map, color='#000000', opacity=0.5)
    route_map_astar.save('route_astar.html')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    src = "147, Brittany Manor Drive, The Boulders, Mill Valley, Amherst, Hampshire County, Massachusetts, 01002"
    #dest = "University of Massachusetts Amherst, Mullins Way, Hadley, Hampshire County, Massachusetts, 01003"
    dest = "Puffers Pond, Amherst"
    get_shortest_path(src, dest, 'min', 25, 'walk')
