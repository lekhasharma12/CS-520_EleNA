import math
from queue import PriorityQueue


def dijkstras(graph, source_node, dest_node):
    elevations = {node: math.inf for node in graph.nodes}
    distances = {node: 0 for node in graph.nodes}
    paths = {node: "" for node in graph.nodes}

    elevations[source_node] = 0
    paths[source_node] = str(source_node)

    visited = set()

    queue = PriorityQueue()
    queue.put((elevations[source_node], source_node))

    while not queue.empty():
        (elevation, node) = queue.get()
        distance = distances[node]

        # marking current node as visited
        visited.add(node)

        # check all neighbors of current node
        for neighbor in graph.neighbors(node):

            edge_data = graph.edges[node, neighbor, 0]
            neighbor_elevation = graph.nodes[neighbor]['elevation']
            node_elevation = graph.nodes[node]['elevation']
            elevation_diff = node_elevation - neighbor_elevation
            neighbor_distance = edge_data['length']

            if neighbor not in visited:
                curr_elevation = elevations[neighbor]
                new_elevation = elevation + elevation_diff

                if new_elevation < curr_elevation:
                    elevations[neighbor] = new_elevation
                    distances[neighbor] = distance + neighbor_distance
                    paths[neighbor] = paths[node] + " " + str(neighbor)
                    queue.put((new_elevation, neighbor))

    # return total elevation and path taken.
    return {
        "elevation": elevations[dest_node],
        "distance": distances[dest_node],
        "path": [int(node) for node in paths[dest_node].strip().split(" ")]
    }


# def dijkstras(graph, source_node, dest_node, opt_type, pct_increase):
#     distances = elevations = {node: math.inf for node in graph.nodes}
#     distances_paths = elevations_paths = {node: "" for node in graph.nodes}
#
#     distances[source_node] = elevations[source_node] = 0
#     distances_paths[source_node] = distances_paths[source_node] = str(source_node)
#
#     visited = set()
#     queue = PriorityQueue()
#     queue.put((distances[source_node], source_node))
#
#     while not queue.empty():
#         (elevation, node) = queue.get()
#
#         # marking current node as visited
#         visited.add(node)
#
#         # check all neighbors of current node
#         for neighbor in graph.neighbors(node):
#
#             edge_data = graph.edges[node, neighbor, 0]
#             neighbor_distance = edge_data['length']
#
#             if neighbor not in visited:
#                 curr_distance = distances[neighbor]
#                 new_distance = neighbor_distance
#
#                 if new_distance < curr_distance:
#                     distances[neighbor] = neighbor_distance
#                     distances_paths[neighbor] = distances_paths[node] + " " + str(neighbor)
#                     queue.put((new_distance, neighbor))
#
#     visited.clear()
#     queue.put((elevations[source_node], source_node))
#
#     while not queue.empty():
#         (elevation, node) = queue.get()
#
#         # marking current node as visited
#         visited.add(node)
#
#         # check all neighbors of current node
#         for neighbor in graph.neighbors(node):
#
#             neighbor_elevation = graph.nodes[neighbor]['elevation']
#             node_elevation = graph.nodes[node]['elevation']
#             elevation_diff = node_elevation - neighbor_elevation
#
#             if neighbor not in visited:
#                 curr_elevation = elevations[neighbor]
#                 new_elevation = elevation + elevation_diff
#
#                 if new_elevation < curr_elevation:
#                     elevations[neighbor] = new_elevation
#                     elevations_paths[neighbor] = elevations_paths[node] + " " + str(neighbor)
#                     queue.put((new_elevation, neighbor))
#
#
#     # return total elevation and path taken.
#     return {
#         "elevation": elevations[dest_node],
#         "path": [int(node) for node in elevations_paths[dest_node].strip().split(" ")]
#     }

def astar(graph, source_node, dest_node):
    elevations = {node: math.inf for node in graph.nodes}
    paths = {node: "" for node in graph.nodes}

    elevations[source_node] = 0
    paths[source_node] = str(source_node)

    visited = set()

    queue = PriorityQueue()
    queue.put((elevations[source_node], source_node))

    while not queue.empty():
        (elevation, node) = queue.get()

        if node == dest_node:
            break

        visited.add(node)

        for neighbor in graph.neighbors(node):
            edge_data = graph.edges[node, neighbor, 0]
            neighbor_elevation = graph.nodes[neighbor]['elevation']
            node_elevation = graph.nodes[node]['elevation']
            elevation_diff = node_elevation - neighbor_elevation
            neighbor_cost = edge_data['length']

            if neighbor not in visited:
                curr_elevation = elevations[neighbor]
                new_elevation = elevation + elevation_diff
                f_cost = new_elevation + neighbor_cost

                if f_cost < curr_elevation:
                    elevations[neighbor] = f_cost
                    paths[neighbor] = paths[node] + " " + str(neighbor)
                    queue.put((f_cost, neighbor))

    return {
        "elevation": elevations[dest_node],
        "path": [int(node) for node in paths[dest_node].strip().split(" ")]
    }


