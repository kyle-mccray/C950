import csv
import datetime
import time
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
        obj = Package(id, address, city, state, zip, weight, deadline, notes)
        obj.update_status("AT HUB", datetime.time(hour=7))
        pkgs_at_hub.append(obj)

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
    for k in range(0, n):
        for i in range(0, n):
            for j in range(0, n):
                if float(distance[i][j]) > float(distance[i][k]) + float(distance[k][j]):
                    distance[i][j] = float(distance[i][k]) + float(distance[k][j])

    return distance


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
g = fun(g, 27)

DELAYED_ON_FLIGHT = [6, 25, 28, 32]
ONLY_ON_TRUCK_2 = [3, 36, 38, 18]
DELIVERED_WITH_EACH_OTHER = [13, 14, 15, 16, 19, 20]
WRONG_ADDRESS = 9
MPH = 18
TOTAL_DISTANCE = 0
HUB = 0
START_TIME = datetime.datetime(year=2020, month=9, day=12, hour=8, minute=0, second=0)  # use a dummy date here so we
# can use a timedelta in the future
truck_1 = Truck(starting_time=START_TIME, current_location=0, name="Truck 1")
truck_2 = Truck(starting_time=START_TIME, current_location=0, name="Truck 2")


def add_packages(truck, packages_to_add=None):
    for obj in range(len(packages_table.array)):
        # add every package in the list and any other packages going to the same
        # destination
        if packages_to_add is None:
            break
        if truck.inv.__len__() == 16:
            break
        if packages_table.array[obj] is None:
            continue
        if obj in packages_to_add:
            truck.inv.append(packages_table.array[obj])
            for x in range(len(packages_table.array)):
                if packages_table.array[x] is None:
                    continue
                if packages_table.array[obj] != packages_table.array[x] and packages_table.array[obj].address_number == \
                        packages_table.array[x].address_number and x != WRONG_ADDRESS:
                    truck.inv.append(packages_table.array[x])
                    packages_table.array[x] = None
            packages_table.array[obj] = None

    for obj in range(len(packages_table.array)):  # fill up the truck with the rest of packages
        if truck.inv.__len__() == 16:
            break
        if packages_table.array[obj] is None:
            continue
        if obj not in DELAYED_ON_FLIGHT and obj not in ONLY_ON_TRUCK_2 and obj not in DELIVERED_WITH_EACH_OTHER and obj != WRONG_ADDRESS:
            truck.inv.append(packages_table.array[obj])
            temp_obj = packages_table.array[obj]
            packages_table.array[obj] = None
            if truck.inv.__len__() == 16:
                break
            for x in range(len(packages_table.array)):
                if truck.inv.__len__() == 16:
                    break
                if packages_table.array[x] is None:
                    continue
                if temp_obj != packages_table.array[x] and temp_obj.address_number == \
                        packages_table.array[x].address_number and x != WRONG_ADDRESS:
                    truck.inv.append(packages_table.array[x])
                    packages_table.array[x] = None

    for x in truck.inv:
        x.update_status("ON TRUCK", truck.time.time())

    return truck


def deliver(g, truck, delivered_packages, no_more_packages=None):
    global TOTAL_DISTANCE
    # this function requires trucks to be at the hub to work properly
    assert truck.current_location == 0
    start = HUB
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
        # print("The truck is currently at location " + str(start) + " the time is " + str(truck.time.time()))
        for x in truck.inv:
            if x.address_number == current_stop:  # deliver all packages on truck that require this location
                x.delivered(truck.time.time())
                x.update_status("DELIVERED", truck.time.time())
                truck.inv.remove(x)
                delivered_packages.insert_package(x)
                # print("Package Number " + str(x.pk_id) + " was delivered " + " at location " + str(
                #     truck.current_location) + " at " + str(truck.time.time()) + " on " + truck.name)
        final_location = current_stop

    if no_more_packages:
        return
    distance = g[final_location][HUB]
    TOTAL_DISTANCE += distance
    truck_travel_time = (distance / MPH)
    truck.time += datetime.timedelta(hours=truck_travel_time)
    truck.current_location = HUB


def run(truck_1, truck_2):
    global WRONG_ADDRESS
    truck_1 = add_packages(truck_1, DELIVERED_WITH_EACH_OTHER)

    deliver(g, truck_1, delivered_packages)

    truck_2 = add_packages(truck_2, ONLY_ON_TRUCK_2)

    deliver(g, truck_2, delivered_packages, no_more_packages=True)

    truck_1 = add_packages(truck_1, DELAYED_ON_FLIGHT)
    deliver(g, truck_1, delivered_packages)
    # updating the package at 10:28
    packages_table.array[9].pk_address = "410 S State St"
    packages_table.array[9].pk_city = "Salt Lake City"
    packages_table.array[9].pk_state = "UT"
    packages_table.array[9].pk_zip = 84111
    packages_table.array[9].address_number = 18
    WRONG_ADDRESS = None
    truck_1 = add_packages(truck_1, packages_to_add=None)
    deliver(g, truck_1, delivered_packages, no_more_packages=True)


def test():
    for x in range(len(delivered_packages.array)):
        if delivered_packages.array[x] is None:
            continue
        if delivered_packages.array[x].pk_deadline == "EOD":
            continue

        if delivered_packages.array[x].pk_deadline == "10:30 AM":
            pkg = delivered_packages.array[x]
            time = delivered_packages.array[x].delivered_at
            time_string = str(time).split(":")
            hours = time_string[0]
            x = time_string[1].split()
            min = x[0]
            assert datetime.timedelta(hours=int(hours), minutes=int(min)) <= datetime.timedelta(hours=10,
                                                                                                minutes=30), str(
                pkg.pk_id)
        elif delivered_packages.array[x].pk_deadline == "9:00 AM":
            pkg = delivered_packages.array[x]
            time = delivered_packages.array[x].delivered_at
            time_string = str(time).split(":")
            hours = time_string[0]
            x = time_string[1].split()
            min = x[0]
            assert datetime.timedelta(hours=int(hours), minutes=int(min)) <= datetime.timedelta(hours=9,
                                                                                                minutes=0), str(
                pkg.pk_id)
        elif x in DELAYED_ON_FLIGHT:
            pkg = delivered_packages.array[x]
            time = delivered_packages.array[x].delivered_at
            time_string = str(time).split(":")
            hours = time_string[0]
            x = time_string[1].split()
            min = x[0]
            assert datetime.timedelta(hours=int(hours), minutes=int(min)) >= datetime.timedelta(hours=9,
                                                                                                minutes=5), str(
                pkg.pk_id)

    pkg = delivered_packages.array[9]
    time = delivered_packages.array[9].delivered_at
    time_string = str(time).split(":")
    hours = time_string[0]
    x = time_string[1].split()
    min = x[0]
    assert datetime.timedelta(hours=int(hours), minutes=int(min)) >= datetime.timedelta(hours=10, minutes=20), str(
        pkg.pk_id)


run(truck_1, truck_2)
test()


def main():
    print("Welcome to the package delivery system")
    print("The last simulation finished in {0:.1f} miles".format(TOTAL_DISTANCE))
    print("Please review the following options. Type exit to end.")
    answer = -1
    while answer != "exit".lower():
        print("")
        print("1. View the package status for all packages at 9:00 a.m.")
        print("2. View the package status for all packages at 10:00 a.m.")
        print("3. View the package status for all packages at 12:05 p.m.")
        print("4. View a single package status at the time of your choosing")
        answer = input()

        if answer == "1":
            status_lookup(datetime.time(hour=9, minute=0))
        elif answer == "2":
            status_lookup(datetime.time(hour=10, minute=0))
        elif answer == "3":
            status_lookup(datetime.time(hour=12, minute=5))
        elif answer == "4":
            try:
                pkg_id = input("Please enter the package number you would like to look up. E.g. 23" "\n")
                str_time = input("Please enter in a time in 24Hr standard. E.g. 12:09" "\n")
                split_time = str_time.split(":")
                status_lookup(datetime.time(hour=int(split_time[0]), minute=int(split_time[1])),
                              package_number=int(pkg_id))
            except Exception:
                print("An error has occurred please check your input")


def status_lookup(start_time, package_number=None):
    start_time = start_time

    if package_number is not None:
        if delivered_packages.array[package_number].delivered_at == start_time or delivered_packages.array[
            package_number].delivered_at < start_time:
            print("Package #" + str(delivered_packages.array[package_number].pk_id) + " current status at " + str(
                start_time) + " is " + delivered_packages.array[package_number].pk_status[2][0])
        # if the delivery time is between the two times the package was delivered already
        elif delivered_packages.array[package_number].pk_status[1][1] <= start_time:
            print("Package #" + str(delivered_packages.array[package_number].pk_id) + " current status at " + str(
                start_time) + " is " + delivered_packages.array[package_number].pk_status[1][0])
        # if the package was not delivered we check to see if the package on truck time is between the
        else:
            print("Package #" + str(delivered_packages.array[package_number].pk_id) + " current status at " + str(
                start_time) + " is " + delivered_packages.array[package_number].pk_status[0][0])
        # if the package is not delivered yet nor on the truck then it can only be at the HUB
    elif package_number is None:
        for x in range(len(delivered_packages.array)):
            if delivered_packages.array[x] is None:
                continue
            if delivered_packages.array[x].delivered_at == start_time or delivered_packages.array[
                x].delivered_at < start_time:
                print("Package #" + str(delivered_packages.array[x].pk_id) + " current status at " + str(
                    start_time) + " is " + delivered_packages.array[x].pk_status[2][0])
                # if the delivery time is between the two times the package was delivered already
            elif delivered_packages.array[x].pk_status[1][1] <= start_time:
                print("Package #" + str(delivered_packages.array[x].pk_id) + " current status at " + str(
                    start_time) + " is " + delivered_packages.array[x].pk_status[1][0])
                # if the package was not delivered we check to see if the package on truck time is between the
            else:
                print("Package #" + str(delivered_packages.array[x].pk_id) + " current status at " + str(
                    start_time) + " is " + delivered_packages.array[x].pk_status[0][0])
                # if the package is not delivered yet nor on the truck then it can only be at the HUB


main()
