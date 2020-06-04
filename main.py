import csv
import operator
from math import inf

from Packages import Package, Table, Node, Graph


# Kyle McCray 000931226

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


def make_graph(rows_dict):
    graph = []
    for i in rows_dict.keys():
        row = rows_dict[i]  # get a single row
        numbers = row[1:]  # numbers start after the second element
        graph.append([])

        for distance in numbers:
            graph[i].append(float(distance))

    return graph


def fun(graph, n):
    distance = graph
    previous_node = [[None for i in range(27)] for x in range(27)]
    counter = 1
    for x in range(len(distance)):
        for y in range(len(distance[x])):
            if distance[x][y] != float(0.0):
                previous_node[x][y] = x
        counter += 1
    for k in range(0, n):
        for i in range(0, n):
            for j in range(0, n):
                if float(distance[i][j]) > float(distance[i][k]) + float(distance[k][j]):
                    distance[i][j] = float(distance[i][k]) + float(distance[k][j])
                    previous_node[i][j] = previous_node[k][j]
    return distance, previous_node


def print_path(path, source, destination):
    s = []
    s.append(destination)
    while path[source][destination] is not source:
        s.insert(0, path[source][destination])
        destination = path[source][destination]
    print(source)
    while len(s) > 0:
        print(s.pop(0))


packages_list = import_packages()
rows_dict = import_addresses()
nodes = make_nodes(rows_dict)
hashTable = Table(packages_list)
g = make_graph(rows_dict)
g, adj_array = fun(g, 27)

def route(graph, adj_array):
    unvisited_nodes = []
    for x in range(len(graph)):
        unvisited_nodes.append(x)
    current_node = 0
    while len(unvisited_nodes) > 0:
        unvisited_nodes[current_node] = -1
        min_num = float(inf)
        min_num_pos = -1
        print("The current array row is " + str(current_node))
        for i in graph[current_node]:
            if i <= min_num and i != float(0.0) and unvisited_nodes.index(graph[current_node].index(i)) != -1:
                min_num = i
                min_num_pos = graph[current_node].index(i)
        print(min_num)
        print(min_num_pos)
        current_node = min_num_pos

route(g, adj_array)

