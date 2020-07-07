import datetime
from math import inf


class Package:

    def __init__(self, id, address="", city="", state="", zip=-1, weight=-1, deadline=-1, notes=-1
                 , current_location=-1, address_number=-1, time=None):
        self.delivered_at = time
        self.pk_id = id
        self.pk_address = address
        self.pk_city = city
        self.pk_state = state
        self.pk_zip = zip
        self.pk_weight = weight
        self.pk_deadline = deadline
        self.pk_notes = notes
        self.pk_status = current_location
        self.address_number = address_number

    def delivered(self, time):
        self.delivered_at = time


class Table:
    # This is a direct access hash table
    def __init__(self, array_of_obj=None):
        self.array = [None]
        if array_of_obj is not None:
            for obj in array_of_obj:
                self.array.append(obj)

    def search(self, id, address="", deadline="", city="", zip="", weight="", status=""):
        search_key = id
        try:
            if self.array[search_key] is None:
                return None
            else:
                return self.array[search_key]
        except IndexError:
            return IndexError

    def insert_new_package(self, id, address, deadline, city, zip, weight, status):
        myPkg = Package(id, address, city, state, zip, weight, deadline, notes, status)
        """Search the table for the specified id. If no id is found check extend the 
        list to the correct length and insert the package.
        None inside the list indicates a blank element and is used as a placeholder"""
        try:
            if self.array[myPkg.pk_id] is None:
                self.array[myPkg.pk_id] = myPkg
                return
            if self.array[myPkg.pk_id] is not None:
                print("ERROR ID IN USE")
                return
        except IndexError:
            # If the bucket is not in the array extend the array to the bucket size then insert the package
            array_size = self.array.__len__()
            n = myPkg.pk_id + 1
            for x in range(array_size, n):
                self.array.insert(x, None)
            self.array[myPkg.pk_id] = myPkg

    def insert_package(self, package):
        myPkg = package
        myPkg.pk_id = int(myPkg.pk_id)
        try:
            if self.array[myPkg.pk_id] is None:
                self.array[myPkg.pk_id] = myPkg
                return
            if self.array[myPkg.pk_id] is not None:
                print("ERROR ID IN USE")
                return
        except IndexError:
            # If the bucket is not in the array extend the array to the bucket size then insert the package
            array_size = self.array.__len__()
            n = myPkg.pk_id + 1
            for x in range(array_size, n):
                self.array.insert(x, None)
            self.array[myPkg.pk_id] = myPkg

    def delete(self, key):
        if self.array[key] is not None:  # set the bucket of key to None
            self.array[key] = None
            print("Package deleted")


class Node:
    def __init__(self, name):
        self.name = name
        self.distance = float(inf)
        self.previous_node = None


class Graph:
    def __init__(self):
        self.adj_nodes = {}
        self.weight = {}

    def add_node(self, node):
        self.adj_nodes[node] = []

    def add_weight(self, node1, node2, weight):
        self.weight[(node1, node2)] = weight
        self.adj_nodes[node1].append(node2)


class Truck:
    def __init__(self, starting_time, current_location=None):
        self.inv = []
        self.time = starting_time
        self.current_location = current_location
