class Package:

    def __init__(self, id, address="", city="", state="", zip=-1, weight=-1, deadline=-1, notes=-1
                 , address_number=-1, time=None):
        self.delivered_at = time
        self.pk_id = id
        self.pk_address = address
        self.pk_city = city
        self.pk_state = state
        self.pk_zip = zip
        self.pk_weight = weight
        self.pk_deadline = deadline
        self.pk_notes = notes
        self.pk_status = []
        self.address_number = address_number

    def delivered(self, time):
        self.delivered_at = time

    def update_status(self, status, time):
        self.pk_status.append([status, time])


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
                print("Package id: " + str(self.array[search_key].pk_id))
                print("Package address: " + str(self.array[search_key].pk_address))
                print("Package deadline: " + str(self.array[search_key].pk_deadline))
                print("Package city: " + str(self.array[search_key].pk_city))
                print("Package zip: " + str(self.array[search_key].pk_zip))
                print("Package weight: " + str(self.array[search_key].pk_weight))
                print("Package status: " + str(self.array[search_key].pk_status))

        except IndexError:
            return IndexError

    def insert_new_package(self, id, address, deadline, city, zip, weight, status):
        my_pkg = Package(id, address, deadline, city, zip, weight, status)
        """
        Search the table for the specified id. If no id is found check extend the 
        list to the correct length and insert the package.
        None inside the list indicates a blank element and is used as a placeholder
        """
        try:
            if self.array[my_pkg.pk_id] is None:
                self.array[my_pkg.pk_id] = my_pkg
                return
            if self.array[my_pkg.pk_id] is not None:
                print("ERROR ID IN USE")
                return
        except IndexError:
            # If the bucket is not in the array extend the array to the bucket size then insert the package
            array_size = self.array.__len__()
            n = my_pkg.pk_id + 1
            for x in range(array_size, n):
                self.array.insert(x, None)
            self.array[my_pkg.pk_id] = my_pkg

    def insert_package(self, package):
        my_pkg = package
        my_pkg.pk_id = int(my_pkg.pk_id)
        try:
            if self.array[my_pkg.pk_id] is None:
                self.array[my_pkg.pk_id] = my_pkg
                return
            if self.array[my_pkg.pk_id] is not None:
                print(str(my_pkg.pk_id) + " ERROR ID IN USE")
                return
        except IndexError:
            # If the bucket is not in the array extend the array to the bucket size then insert the package
            array_size = self.array.__len__()
            n = my_pkg.pk_id + 1
            for x in range(array_size, n):
                self.array.insert(x, None)
            self.array[my_pkg.pk_id] = my_pkg

    def delete(self, key):
        if self.array[key] is not None:  # set the bucket of key to None
            self.array[key] = None
            print("Package deleted")


class Truck:
    def __init__(self, starting_time, current_location=None, name=None):
        self.inv = []
        self.time = starting_time
        self.current_location = current_location
        self.name = name
