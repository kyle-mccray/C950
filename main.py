import csv
from math import inf
from datetime import time
from Packages import Package, Table, Node


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
        node_list.append(x)

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


def shortest_route_no_restrictions(graph):
    unvisited_nodes = []
    for x in range(len(graph)):
        unvisited_nodes.append(x)
    current_node = 0
    visited_distance = {}
    while len(unvisited_nodes) > 1:  # if only one location remains in the unvisited list we are done
        unvisited_nodes.remove(current_node)
        min_num = float(inf)
        min_num_pos = -1
        print("The current array row is " + str(current_node))
        for i in graph[current_node]:
            if i <= min_num and i != float(0.0) and unvisited_nodes.__contains__(graph[current_node].index(i)):
                min_num = i
                min_num_pos = graph[current_node].index(i)
        # print(min_num)
        # print(min_num_pos)
        visited_distance[current_node] = min_num

        current_node = min_num_pos
    visited_distance[unvisited_nodes[0]] = float(0.0)  # this gets us the last location into are dict
    return visited_distance


def route(graph, nodes):
    unvisited_nodes = [0]
    for x in nodes:
        unvisited_nodes.append(x)
    current_node = 0
    visited_distance = {}
    while len(unvisited_nodes) > 1:  # if only one location remains in the unvisited list we are done
        unvisited_nodes.remove(current_node)
        min_num = float(inf)
        min_num_pos = -1
        print("The current array row is " + str(current_node))
        for i in graph[current_node]:
            if i <= min_num and i != float(0.0) and unvisited_nodes.__contains__(graph[current_node].index(i)):
                min_num = i
                min_num_pos = graph[current_node].index(i)
        visited_distance[current_node] = min_num
        current_node = min_num_pos
    visited_distance[unvisited_nodes[0]] = float(0.0)  # this gets us the last location into are dict
    return route


packages_list = import_packages()
rows_dict = import_addresses()
locations = make_nodes(rows_dict)
hashTable = Table(packages_list)
g = make_graph(rows_dict)
g, adj_array = fun(g, 27)
v = shortest_route_no_restrictions(g)

DELAYED_ON_FLIGHT = [6, 25, 28, 32]
ONLY_ON_TRUCK_2 = [3, 36, 38, 18]
DELIVERED_WITH_EACH_OTHER = [13, 14, 15, 16, 19, 20]
WRONG_ADDRESS = 9
START_TIME = time(hour=8, minute=0, second=0).isoformat()
current_time = START_TIME
truck_1 = []
truck_2 = []

for x in ONLY_ON_TRUCK_2:
    truck_2.append(x)

for x in DELIVERED_WITH_EACH_OTHER:
    truck_1.append(x)

for x in range(len(hashTable.array)):
    if x in truck_1:
        hashTable.array[x].pk_status = "On Truck1"

for x in range(len(hashTable.array)):
    if x in truck_2:
        hashTable.array[x].pk_status = "On Truck2"

# def deliver
for x in truck_2:
    address = hashTable.array[x].pk_address
    address_

# def check_req(id, current_time):
#     s = time(hour=9, minute=5, second=0).isoformat()
#     if current_time >= s and id in DELAYED_ON_FLIGHT:
#         return True  # package can be added
#
#
# for x in v.keys():
#     address = nodes[x].name
#     if x == 0:  # we do not have to worry about dropping packages off at the hub
#         continue
#
#     for element in range(len(hashTable.array)):
#         if hashTable.array[element] is not None:
#             if hashTable.array[element].pk_address in address:  # if the address to deliver the package is current
#                 # next in route add the package to truck 1
#                 id = hashTable.array[element].pk_id
#                 check_req(id, current_time)
#                 hashTable.array[element].current_location = "On Truck"
#                 truck_1[x] = id
#
# for x in truck_1:
#     print(x)
