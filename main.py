import csv
import operator
from math import inf

from Packages import Package, Table, Node, Graph


def import_packages():
    fields = []
    rows = []
    pkgs_at_hub = []

    with open('pckgFiles.csv', newline='') as csvfile:
        row = csv.reader(csvfile, delimiter=",")
        fields = next(row)
        for row in row:
            rows.append(row)

    for row in rows:
        id = row[0]
        address = row[1]
        city = row[2]
        state = row[3]
        zip = row[4]
        deadline = row[5]
        weight = row[6]
        notes = row[7]
        pkgs_at_hub.append(Package(id, address, city, state, zip, deadline, weight, notes, "At_Hub"))

    return pkgs_at_hub


def import_addresses():
    rows = []
    with open('distanceTablesExtd.csv', newline='') as csvfile:
        row = csv.reader(csvfile, delimiter=",")
        field = next(row)
        for row in row:
            rows.append(row)

    rows[0] = None
    rows[1] = None
    rows[2] = None
    rows[3] = None
    rows[4] = None
    rows[5] = None
    rows[6] = None

    col = []
    for x in rows:
        if x is None:
            continue
        else:
            string = x[1:]
            col.append(string)

    rows = {}
    for i in range(len(col)):
        rows[i] = []

    for i in rows.keys():
        x = col[i]
        y = x
        for z in y:
            rows[i].append(z)

    return rows


def make_nodes(rows):
    node_list = []
    for x in rows:
        address = rows[x][0]
        x = address.replace('\n', ' ')
        node_list.append(Node(x))

    return node_list


def make_graph(rows_dict, nodes):
    address_rows = nodes
    address_cols = nodes
    graph = Graph()

    # create the dict key for each node
    for node in nodes:
        graph.add_node(node)

    for i in rows_dict.keys():
        row = rows_dict[i]  # get a single row
        numbers = row[1:]  # numbers start after the second element
        node1 = address_rows[i]
        z = 0  # used to iterate through the col array
        for distance in numbers:
            node2 = address_cols[z]
            if distance == str(0.0):  # if the distance is 0.0 the node1 is = node2
                z += 1
                continue
            else:
                graph.add_directed_edge(node1, node2, float(distance))
                z += 1

    return graph


def shortest_path(graph, starting_node):
    unvisited_list = []

    for node in graph.adj_nodes:
        unvisited_list.append(node)

    current_node = starting_node
    current_node.distance = 0

    while len(unvisited_list) > 0:  # while we have not visited every node
        print("THE CURRENT NODE IS " + current_node.name)
        smallest_index = 0

        for i in range(1, len(unvisited_list)):
            if unvisited_list[i].distance < unvisited_list[smallest_index].distance:
                smallest_index = i
        current_node = unvisited_list.pop(smallest_index)

        for adj_node in graph.adj_nodes[current_node]:  # for each key in the graph print its adjacent node
            d1 = adj_node.distance
            d2 = current_node.distance + graph.edge_distance[(current_node, adj_node)]
            if d2 < d1:
                print("Adj Node distance was " + str(d1))
                print("Adj Node with current " + str(d2))
                adj_node.distance = d2
                adj_node.predecessor = current_node
    return graph



def get_shortest_path(start_vertex, end_vertex):
    # Start from end_vertex and build the path backwards.
    path = ""
    current_vertex = end_vertex
    while current_vertex is not start_vertex:
        path = " -> " + str(current_vertex.name) + path
        current_vertex = current_vertex.predecessor
    path = start_vertex.name + path
    return path


packages_list = import_packages()
rows_dict = import_addresses()
nodes = make_nodes(rows_dict)
hashTable = Table(packages_list)
g = make_graph(rows_dict, nodes)
g = shortest_path(g, nodes[0])
sum_num = 0
for node in g.adj_nodes:
    if node.predecessor is None and node is not nodes[0]:
        print("Hub to %s: no path exists" % node.name)
    else:
        print("Hub to %s: %s (total weight: %g)" % (node.name, get_shortest_path(nodes[0], node), node.distance))

