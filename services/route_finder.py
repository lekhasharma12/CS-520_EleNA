import math
from queue import PriorityQueue
from utils.utils import distance_till_dest, elevation_diff_with_dest, get_coordinates_from_node, get_max_elevation, get_min_elevation, get_path_distance, get_time_for_mode


def dijkstras(graph, source_node, dest_node):
    elevations = {node: 0 for node in graph.nodes}
    distances = {node: math.inf for node in graph.nodes}
    paths = {node: [] for node in graph.nodes}
    node_count = 0

    distances[source_node] = 0
    paths[source_node] = [source_node]

    visited = set()

    queue = PriorityQueue()
    queue.put((distances[source_node], source_node))

    while not queue.empty():
        (distance, node) = queue.get()

        if node == dest_node:
            break

        elevation = elevations[node]
        visited.add(node)
        node_count += 1

        # check all neighbors of current node
        for neighbor in graph.neighbors(node):

            edge_data = graph.edges[node, neighbor, 0]
            neighbor_distance = edge_data['length']

            neighbor_elevation = graph.nodes[neighbor]['elevation']
            node_elevation = graph.nodes[node]['elevation']
            elevation_diff = node_elevation - neighbor_elevation

            if neighbor not in visited:
                curr_distance = distances[neighbor]
                new_distance = distance + neighbor_distance

                if new_distance < curr_distance:
                    distances[neighbor] = new_distance
                    elevations[neighbor] = elevation + elevation_diff
                    paths[neighbor] = paths[node] + [neighbor]
                    queue.put((new_distance, neighbor))

    print("D node count ", node_count)

    # return total elevation and path taken.
    return {
        "elevation": elevations,
        "distance": distances,
        # "path": [get_coordinates_from_node(graph, node) for node in paths[dest_node]]
        "path": paths[dest_node]
    }


def dijkstras_with_elevation(graph, source_node, dest_node, elevation_type, pct_increase, mode):
    elevations = {node: math.inf for node in graph.nodes}
    distances = {node: 0 for node in graph.nodes}
    paths = {node: [] for node in graph.nodes}

    dijkstras_res = dijkstras(graph, source_node, dest_node)

    elevations[source_node] = 0
    paths[source_node] = [source_node]

    visited = set()

    queue = PriorityQueue()
    queue.put((elevations[source_node], source_node))

    node_count = 0
    increment_factor = (1 + (pct_increase / 100))
    while not queue.empty():
        (elevation, node) = queue.get()

        if node == dest_node:
            break

        distance = distances[node]
        node_elevation = graph.nodes[node]['elevation']

        # marking current node as visited
        visited.add(node)
        node_count += 1
        # check all neighbors of current node
        for neighbor in graph.neighbors(node):

            edge_data = graph.edges[node, neighbor, 0]
            neighbor_distance = edge_data['length']

            neighbor_elevation = graph.nodes[neighbor]['elevation']
            elevation_diff = node_elevation - neighbor_elevation

            # making the elevation negative so that priority queue is popped in descending order
            if elevation_type == 'min':
                elevation_diff = elevation_diff*(-1)

            if neighbor not in visited:
                curr_elevation = elevations[neighbor]
                new_elevation = elevation + elevation_diff
                new_distance = distance + neighbor_distance

                if new_distance > dijkstras_res["distance"][neighbor] * increment_factor:
                    continue
                if new_elevation < curr_elevation:
                    distances[neighbor] = new_distance
                    elevations[neighbor] = new_elevation
                    paths[neighbor] = paths[node] + [neighbor]
                    queue.put((new_elevation, neighbor))

    print("D node count ", node_count)
    if distances[dest_node] != 0 and distances[dest_node] < dijkstras_res['distance'][dest_node] * increment_factor:
        print("route exists")
        final_path = paths[dest_node]
    else:
        final_path = dijkstras_res['path']
    # return total elevation and path taken.
    final_distance = get_path_distance(graph, final_path)
    return {
        "elevation": (get_min_elevation(graph, final_path), get_max_elevation(graph, final_path)),
        "distance": final_distance,
        "time": get_time_for_mode(final_distance, mode),
        "path": [get_coordinates_from_node(graph, node) for node in final_path]
        # "path": path
    }


def astar(graph, source_node, dest_node):
    elevations = {node: 0 for node in graph.nodes}
    distances = {node: math.inf for node in graph.nodes}
    paths = {node: [] for node in graph.nodes}
    node_count = 0

    f_distances = {node: math.inf for node in graph.nodes}

    distances[source_node] = 0
    f_distances[source_node] = f_distances[source_node] + distance_till_dest(graph, source_node, dest_node)
    paths[source_node] = [source_node]

    visited = set()

    queue = PriorityQueue()
    queue.put((f_distances[source_node], source_node))

    while not queue.empty():
        (f_distance, node) = queue.get()

        if node == dest_node:
            break

        elevation = elevations[node]
        distance = distances[node]

        # marking current node as visited
        visited.add(node)
        node_count += 1

        # check all neighbors of current node
        for neighbor in graph.neighbors(node):

            edge_data = graph.edges[node, neighbor, 0]
            neighbor_distance = edge_data['length']

            neighbor_elevation = graph.nodes[neighbor]['elevation']
            node_elevation = graph.nodes[node]['elevation']
            elevation_diff = node_elevation - neighbor_elevation

            if neighbor not in visited:
                curr_distance = distances[neighbor]
                new_distance = distance + neighbor_distance

                if new_distance < curr_distance:
                    distances[neighbor] = new_distance
                    f_distances[neighbor] = distances[neighbor] + distance_till_dest(graph, neighbor, dest_node)
                    elevations[neighbor] = elevation + elevation_diff
                    paths[neighbor] = paths[node] + [neighbor]
                    queue.put((f_distances[neighbor], neighbor))

    print("A node count ", node_count)
    # return total elevation and path taken.
    return {
        "elevation": elevations,
        "distance": distances,
        # "path": [get_coordinates_from_node(graph, node) for node in paths[dest_node]]
        "path": paths[dest_node]
    }


def astar_with_elevation(graph, source_node, dest_node, elevation_type, pct_increase, mode):
    elevations = {node: math.inf for node in graph.nodes}
    distances = {node: 0 for node in graph.nodes}
    paths = {node: [] for node in graph.nodes}

    f_elevations = {node: math.inf for node in graph.nodes}

    elevations[source_node] = 0
    f_elevations[source_node] = f_elevations[source_node] + elevation_diff_with_dest(graph, source_node, dest_node)
    paths[source_node] = [source_node]

    astar_res = astar(graph, source_node, dest_node)

    visited = set()

    queue = PriorityQueue()
    queue.put((f_elevations[source_node], source_node))

    node_count = 0
    increment_factor = (1 + (pct_increase / 100))

    while not queue.empty():
        (f_elevation, node) = queue.get()


        if node == dest_node:
            break

        elevation = elevations[node]
        distance = distances[node]
        node_elevation = graph.nodes[node]['elevation']

        # marking current node as visited
        visited.add(node)
        node_count += 1
        # check all neighbors of current node
        for neighbor in graph.neighbors(node):

            edge_data = graph.edges[node, neighbor, 0]
            neighbor_distance = edge_data['length']

            neighbor_elevation = graph.nodes[neighbor]['elevation']
            elevation_diff = node_elevation - neighbor_elevation

            # making the elevation negative so that priority queue is popped in descending order
            if elevation_type == 'min':
                elevation_diff = elevation_diff*(-1)

            if neighbor not in visited:
                curr_elevation = elevations[neighbor]
                new_elevation = elevation + elevation_diff
                new_distance = distance + neighbor_distance

                if new_distance > astar_res["distance"][neighbor] * increment_factor:
                    continue
                if new_elevation < curr_elevation:
                    distances[neighbor] = new_distance
                    elevations[neighbor] = new_elevation
                    f_elevations[neighbor] = f_elevations[neighbor] + elevation_diff_with_dest(graph, neighbor, dest_node)
                    paths[neighbor] = paths[node] + [neighbor]
                    queue.put((f_elevations[neighbor], neighbor))

    print("A node count ", node_count)
    if distances[dest_node] != 0 and distances[dest_node] < astar_res['distance'][dest_node] * increment_factor:
        print("route exists")
        final_path = paths[dest_node]
    else:
        final_path = astar_res['path']
    # return total elevation and path taken.
    final_distance = get_path_distance(graph, final_path)
    return {
        "elevation": (get_min_elevation(graph, final_path), get_max_elevation(graph, final_path)),
        "distance": final_distance,
        "time": get_time_for_mode(final_distance, mode),
        "path": [get_coordinates_from_node(graph, node) for node in final_path]
        # "path": path
    }
