import osmnx as ox
from heapq import heappush, heappop
import math


class Node:
    def __init__(self, node_id, position, g_cost, h_cost, previous_node):
        self.id = node_id
        self.position = position

        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = self.g_cost + self.h_cost

        self.previous_node = previous_node


def reconstruct_path(node):
    path = []
    current_node = node

    while current_node:
        path.append(current_node.id)

        # reaches nil once current node is starting node
        current_node = current_node.previous_node

    # start -> end
    return path[::-1]


def heuristic(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def find_neighbors(graph, node_id):
    return [(neighbor, graph.nodes[neighbor]) for neighbor in graph.neighbors(node_id)]


def A_STAR_SEARCH(graph, start, goal):
    start_node = Node(
        start["id"],
        start["position"],
        0,
        heuristic(start["position"], goal["position"]),
        None,
    )

    open_list = [(start_node.f_cost, start_node)]
    open_dict = {start["id"]: start_node}
    closed_dict = {}

    while open_list:
        _, current_node = heappop(open_list)

        if current_node.id == goal["id"]:
            return reconstruct_path(current_node)

        for neighbor_id, data in find_neighbors(graph, current_node.id):
            neighbor_position = (data["x"], data["y"])

            edge_data = graph.get_edge_data(current_node.id, neighbor_id)
            edge_length = min([d["length"] for d in edge_data.values()])

            g_cost = current_node.g_cost + edge_length
            h_cost = heuristic(neighbor_position, goal["position"])

            neighbor_node = Node(neighbor_id, neighbor_position, g_cost, h_cost, current_node)

            if neighbor_id in open_dict and open_dict[neighbor_id].f_cost <= neighbor_node.f_cost:
                continue
            if neighbor_id in closed_dict and closed_dict[neighbor_id].f_cost <= neighbor_node.f_cost:
                continue

            heappush(open_list, (neighbor_node.f_cost, neighbor_node))
            open_dict[neighbor_id] = neighbor_node

        closed_dict[current_node.id] = current_node

    return None


G = ox.load_graphml("dc_drive.graphml")

start_address = input("Current location address: ")
destination_address = input("Destination address: ")

start_coordinates = ox.geocode(start_address)
end_coordinates = ox.geocode(destination_address)

start_id = ox.distance.nearest_nodes(G, start_coordinates[1], start_coordinates[0])
end_id = ox.distance.nearest_nodes(G, end_coordinates[1], end_coordinates[0])

start_data = G.nodes[start_id]
end_data = G.nodes[end_id]

path = A_STAR_SEARCH(
    G,
    {"id": start_id, "position": (start_data["x"], start_data["y"])},
    {"id": end_id, "position": (end_data["x"], end_data["y"])},
)

if path:
    street_names = []
    for u, v in zip(path[:-1], path[1:]):
        edge_data = G.get_edge_data(u, v)
        if edge_data:
            best_edge = min(edge_data.values(), key=lambda d: d.get("length", float("inf")))
            name = best_edge.get("name", "Unnamed Road")

            if isinstance(name, list) and len(name) > 1:
                name = name[1]
            
            if not street_names or street_names[-1] != name:
                street_names.append(name)

    print("Directions:")
    for street in street_names:
        print("->", street)

    ox.plot_graph_route(G, path, route_linewidth=4, node_size=0, orig_dest_size=100)
else:

    print("No path found!")

