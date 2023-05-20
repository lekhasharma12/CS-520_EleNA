import math
from queue import PriorityQueue


def dijkstras(graph, source_node, dest_node):
    elevations = {node: math.inf for node in graph.nodes}
    paths = {node: "" for node in graph.edges}

    elevations[source_node] = 0
    paths[source_node] = str(source_node)

    visited = set()

    queue = PriorityQueue()
    queue.put((elevations[source_node], source_node))

    while not queue.empty():
        (elevation, node) = queue.get()

        # marking current node as visited
        visited.add(node)

        # check all neighbors of current node
        for neighbor in graph.neighbors(node):

            edge_data = graph.edges[node, neighbor, 0]
            neighbor_elevation = graph.nodes[neighbor]['elevation']
            node_elevation = graph.nodes[node]['elevation']
            elevation_diff = node_elevation - neighbor_elevation
            neighbor_cost = edge_data['length']

            if neighbor not in visited:
                curr_elevation = elevations[neighbor]
                new_elevation = elevation + elevation_diff

                if new_elevation < curr_elevation:
                    elevations[neighbor] = new_elevation
                    paths[neighbor] = paths[node] + " " + str(neighbor)
                    queue.put((new_elevation, neighbor))

    # return total elevation and path taken.
    return {
        "elevation": elevations[dest_node],
        "path": [int(node) for node in paths[dest_node].strip().split(" ")]
    }

