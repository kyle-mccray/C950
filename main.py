import csv
import datetime
from math import inf
from Packages import Package, Table, Node, Truck


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
        pkgs_at_hub.append(Package(id, address, city, state, zip, weight, deadline, notes, "At_Hub"))

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
locations_list = make_nodes(rows_dict)
delivered_packages = Table(None)
packages_table = Table(packages_list)

# assign each package the location number
for x in range(len(locations_list)):
    for y in range(len(packages_table.array)):
        if packages_table.array[y] is None:
            continue
        if packages_table.array[y].pk_address in locations_list[x]:
            packages_table.array[y].address_number = x


g = make_graph(rows_dict)
g, adj_array = fun(g, 27)
v = shortest_route_no_restrictions(g)

DELAYED_ON_FLIGHT = [6, 25, 28, 32]
ONLY_ON_TRUCK_2 = [3, 36, 38, 18]
DELIVERED_WITH_EACH_OTHER = [13, 14, 15, 16, 19, 20]
WRONG_ADDRESS = 9
MPH = 18
TOTAL_DISTANCE = 0
START_TIME = datetime.datetime(year=2020, month=9, day=12, hour=8, minute=0, second=0)  # use a dummy date here so we
# can use a timedelta in the future
truck_1 = Truck(starting_time=START_TIME)
truck_2 = Truck(starting_time=START_TIME)


def add_packages(truck, list_of_packages):
    for i in range(len(packages_table.array)):
        if truck.inv.__len__() == 16:
            return truck
        if packages_table.array[i] is None:
            continue
        if i in list_of_packages and i != WRONG_ADDRESS:
            packages_table.array[i].pk_status = "ON TRUCK"
            truck.inv.append(packages_table.array[i])
            for x in range(len(packages_table.array)):
                if packages_table.array[x] is None:
                    continue
                if packages_table.array[x].pk_address == packages_table.array[i].pk_address and packages_table.array[x].pk_id != packages_table.array[i].pk_id:
                    packages_table.array[i].pk_status = "ON TRUCK"
                    truck.inv.append(packages_table.array[x])
                    packages_table.array[x] = None  # remove object from table since its on a truck now
            packages_table.array[i] = None  # remove object from table since its on a truck now

    return truck


truck_2 = add_packages(truck_2, ONLY_ON_TRUCK_2)
truck_1 = add_packages(truck_1, DELIVERED_WITH_EACH_OTHER)


def deliver(g, truck, delivered_packages):
    global TOTAL_DISTANCE
    HUB = 0
    # this function requires trucks to be at the hub to work properly
    truck.inv.insert(0, 0)
    start = truck.inv.pop(0)
    final_location = -1
    while truck.inv.__len__() > 0:
        distance = float(inf)
        current_stop = -1
        for x in truck.inv:
            z = x.address_number
            if g[start][z] < distance:
                distance = g[start][z]
                current_stop = z
        start = current_stop
        # Time = D/S
        # 18 Mph is how fast the truck goes
        TOTAL_DISTANCE += distance
        truck_travel_time = (distance / MPH)
        truck.time += datetime.timedelta(hours=truck_travel_time)
        truck.current_location = current_stop
        print("The truck is currently at location " + str(start) + " the time is " + str(truck.time.time()))
        for x in truck.inv:
            if x.address_number == current_stop:  # deliver all packages on truck that require this location
                x.delivered(truck.time.time())
                x.pk_status = "DELIVERED"
                truck.inv.remove(x)
                delivered_packages.insert_package(x)
                print("Package Number " + str(x.pk_id) + " was delivered ")
        final_location = current_stop

    distance = g[final_location][HUB]
    truck_travel_time = (distance / MPH)
    truck.time += datetime.timedelta(hours=truck_travel_time)
    truck.current_location = HUB


deliver(g, truck_2, delivered_packages)
deliver(g, truck_1, delivered_packages)
print(TOTAL_DISTANCE)
print(truck_1.time)
print("   ")
print(truck_2.time)



