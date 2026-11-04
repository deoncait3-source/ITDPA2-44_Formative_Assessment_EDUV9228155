import heapq
from itertools import count
import time


# Question 2.1.

class IncidentQueue:
    def __init__(self):
        self.queue = []
        self.counter = count()

    def add_incident(self, incident, priority):
        if priority not in (1, 2):
            print("Error: Priority must be 1 (Critical) or 2 (Routine).")
            return False

        if not isinstance(incident, str) or not incident.strip():
            print("Error: Incident description cannot be empty.")
            return False

        arrival_order = next(self.counter)

        heapq.heappush(
            self.queue,
            (priority, arrival_order, incident.strip())
        )

        print(f"Added: {incident.strip()} (Priority {priority})")
        return True

    def dispatch(self):
        if not self.queue:
            print("No incidents waiting for dispatch.")
            return None

        priority, arrival_order, incident = heapq.heappop(
            self.queue
        )

        print(f"Dispatched: {incident} (Priority {priority})")
        return incident


# Demonstration using four incidents

incidents = IncidentQueue()

incidents.add_incident("Noise complaint", 2)
incidents.add_incident("Cardiac arrest", 1)
incidents.add_incident("Minor road accident", 2)
incidents.add_incident("Building fire with trapped people", 1)

print("\nDispatch order:")

while incidents.queue:
    incidents.dispatch()


# Question 2.2.

# Vehicle records stored in a dictionary (hash table)

vehicles = {
    "ND123456": {
        "type": "Ambulance",
        "status": "Available",
        "crew": "Crew A"
    },
    "ND789012": {
        "type": "Fire Engine",
        "status": "On Call",
        "crew": "Crew B"
    },
    "ND345678": {
        "type": "Rescue Vehicle",
        "status": "Available",
        "crew": "Crew C"
    }
}


def lookup_vehicle(registration):
    if not isinstance(registration, str) or not registration.strip():
        print("Error: Registration number cannot be empty.")
        return None

    registration = registration.strip().upper()
    vehicle = vehicles.get(registration)

    if vehicle is None:
        print(f"Vehicle {registration} was not found.")
        return None

    print(f"\nVehicle Registration: {registration}")
    print(f"Vehicle Type: {vehicle['type']}")
    print(f"Status: {vehicle['status']}")
    print(f"Assigned Crew: {vehicle['crew']}")

    return vehicle


# Demonstrate a successful lookup

lookup_vehicle("ND123456")


# Question 2.3.

print("\nTEST 1: Dispatch from an empty queue")

empty_queue = IncidentQueue()
empty_queue.dispatch()


print("\nTEST 2: Look up a vehicle that does not exist")

lookup_vehicle("UNKNOWN999")


print("\nTEST 3: Add an incident with an invalid priority")

incidents_test = IncidentQueue()
incidents_test.add_incident("Medical emergency", 5)


print("\nTEST 4: Add an incident with a missing description")

incidents_test.add_incident("", 1)


# Question 2.4.

# Test 1: Critical incidents are dispatched first

test_queue = IncidentQueue()
test_queue.add_incident("Routine call", 2)
test_queue.add_incident("Critical call", 1)

result = test_queue.dispatch()

if result == "Critical call":
    print("Test 1 passed: Critical incident dispatched first.")
else:
    print("Test 1 failed.")


# Test 2: Incidents with the same priority keep arrival order

test_queue = IncidentQueue()
test_queue.add_incident("First call", 2)
test_queue.add_incident("Second call", 2)

result = test_queue.dispatch()

if result == "First call":
    print("Test 2 passed: Arrival order maintained.")
else:
    print("Test 2 failed.")


# Test 3: An existing vehicle can be found

result = lookup_vehicle("ND123456")

if result is not None:
    print("Test 3 passed: Vehicle found successfully.")
else:
    print("Test 3 failed.")


# Test 4: A missing vehicle is handled correctly

result = lookup_vehicle("UNKNOWN999")

if result is None:
    print("Test 4 passed: Missing vehicle handled correctly.")
else:
    print("Test 4 failed.")


# Question 2.5.

dataset_sizes = [1000, 10000, 50000]
repeats = 100

print("\nVEHICLE LOOKUP PERFORMANCE COMPARISON")
print("-" * 75)
print(f"{'Vehicles':<12}{'List Search (ms)':<22}{'Hash Table (ms)':<22}")
print("-" * 75)

for size in dataset_sizes:

    # Create the vehicle dataset

    vehicle_list = [
        {"registration": f"REG{i:06d}", "status": "Available"}
        for i in range(size)
    ]

    # Create a dictionary using registration numbers as keys

    vehicle_hash = {
        vehicle["registration"]: vehicle
        for vehicle in vehicle_list
    }

    # Search for the last vehicle in the dataset

    target = f"REG{size - 1:06d}"

    def list_search():
        for vehicle in vehicle_list:
            if vehicle["registration"] == target:
                return vehicle
        return None

    def hash_search():
        return vehicle_hash.get(target)

    # Check that both methods find the same vehicle

    assert list_search() == hash_search()

    # Measure list search time

    start = time.perf_counter()

    for _ in range(repeats):
        list_search()

    list_time = (time.perf_counter() - start) * 1000 / repeats

    # Measure hash table lookup time

    start = time.perf_counter()

    for _ in range(repeats):
        hash_search()

    hash_time = (time.perf_counter() - start) * 1000 / repeats

    print(f"{size:<12}{list_time:<22.6f}{hash_time:<22.6f}")

print("-" * 75)
print("Comparison completed successfully.")


# Question 4.1.

# Hash Table
hash_table = {
    "Berea": True,
    "Durban North": True,
    "Glenwood": True,
    "Morningside": True,
    "Pinetown": True,
    "Umbilo": True,
    "Westville": True,
    "Umhlanga": True
}

def add_to_hash(suburb):
    hash_table[suburb] = True

def find_in_hash(suburb):
    return suburb in hash_table


# Binary Search Tree
class Node:
    def __init__(self, suburb):
        self.suburb = suburb
        self.left = None
        self.right = None


def insert(root, suburb):
    if root is None:
        return Node(suburb)

    if suburb < root.suburb:
        root.left = insert(root.left, suburb)
    elif suburb > root.suburb:
        root.right = insert(root.right, suburb)

    return root


def find_in_bst(root, suburb):
    if root is None:
        return False

    if root.suburb == suburb:
        return True

    if suburb < root.suburb:
        return find_in_bst(root.left, suburb)

    return find_in_bst(root.right, suburb)


# Add the eight suburbs to the BST
root = None

for suburb in hash_table:
    root = insert(root, suburb)


# Test Both Structures
print("Number of suburbs:", len(hash_table))

print("Hash table - find Berea:", find_in_hash("Berea"))
print("BST - find Berea:", find_in_bst(root, "Berea"))

print("Hash table - find Unknown:", find_in_hash("Unknown"))
print("BST - find Unknown:", find_in_bst(root, "Unknown"))

add_to_hash("Hillcrest")
root = insert(root, "Hillcrest")

print("Add new suburb to hash table:", find_in_hash("Hillcrest"))
print("Add new suburb to BST:", find_in_bst(root, "Hillcrest"))



# QUESTION 4.2.

# Display suburbs from the hash table in alphabetical order
print("Hash table (sorted):")
print(sorted(hash_table.keys()))


# Display suburbs from the BST in alphabetical order
def alphabetical_listing(root):
    if root is not None:
        alphabetical_listing(root.left)
        print(root.suburb)
        alphabetical_listing(root.right)


print("BST (sorted):")
alphabetical_listing(root)



#Question 4.3.

# Store the number of incidents for each suburb
incident_counts = {
    "Berea": 3,
    "Durban North": 5,
    "Glenwood": 2,
    "Morningside": 4,
    "Pinetown": 6,
    "Umbilo": 1,
    "Westville": 3,
    "Umhlanga": 7
}

# Add an incident to a suburb
def add_incident(suburb):
    if suburb in incident_counts:
        incident_counts[suburb] += 1
    else:
        incident_counts[suburb] = 1

# Display incident counts
print("Incident counts before update:")
print(incident_counts)

add_incident("Berea")
add_incident("Hillcrest")

print("Incident counts after update:")
print(incident_counts)

