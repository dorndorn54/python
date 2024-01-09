###########################
# 6.0002 Problem Set 1a: Space Cows
# Name:
# Collaborators:
# Time:

import time
from ps1_partition import get_partitions


# ================================
# Part A: Transporting Space Cows
# ================================


# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cow_dict = dict()
    # open the file
    f = open(filename, "r")
    for line in f:
        name, weight = line.split(",")
        cow_dict[name] = int(weight)
    f.close()
    print(cow_dict)

    return cow_dict


# Problem 2
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    sorted_cows = sorted(cows.items(), key=lambda x: x[1], reverse=True)
    result = []   # creating list where results will be appended.
    trip = 0   # increasing with each trip.
    while len(sorted_cows) > 0:  # after there is no cow left, the job is done.
        trip_limit = limit   # sets the initial limit for the trip.
        result.append([])   # initiating trip sub-list.
        removed_cows = []  # creating a list with indexes of cows that were already assigned to the trip.
        for cow in sorted_cows:
            if cow[1] <= trip_limit:   # checking if weight of cow meets current constraint.
                result[trip].append(cow[0])
                removed_cows.append(sorted_cows.index(cow))
                trip_limit -= cow[1]   # updating the limit for current trip.
        trip += 1
        for cow_index in sorted(removed_cows, reverse=True):
            sorted_cows.pop(cow_index)
    return result


# Problem 3
def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    total_trips = list()
    # a list of tuples
    cow_list = sorted(cows.items(), key=lambda x: x[1], reverse=True)
    # prepare total number of possible iterations
    for partition in get_partitions(cow_list):
        total_trips.append(partition)
    # total_trips is a list of a list of a list of tuples
    for trip in total_trips.copy():
        # trip is one possible trip all permutations
        temp_limit = limit
        for journey in trip:
            # check if sum of that partition exceed
            journey_weight = sum(map(lambda x: int(x[1]), journey))
        # if so delete
        if temp_limit < journey_weight:
            total_trips.remove(trip)
    # now total_trips is a list of all possible partitions
    # need to convert it to a lists of lists with just names
    export_list = list()
    # iterate over the count of total partitions left
    for count, element in enumerate(total_trips):
        # give empty list for the map function to append to later
        export_list.append([])
        # element represents the list of tuples at position count of total_trips
        for j in map(lambda x: x[0], element):
            # add each name to a new list
            export_list[count].append(j)

    return export_list


# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """

    # run the brute force algorithm first
    """_summary of brute force algorithm_
    plain and simple it works but takes fking long time to do so
    """
    filename = "ps1_cow_data.txt"
    cows = load_cows(filename)
    start = time.time()
    brute_force_cow_transport(cows, limit=10)
    end = time.time()
    print(end - start)
    """the much better way to complete it even as the size of the file increases
    """
    # run the greedy algorithm next
    filename = "ps1_cow_data.txt"
    cows = load_cows(filename)
    start = time.time()
    greedy_cow_transport(cows, limit=10)
    end = time.time()
    print(end - start)

compare_cow_transport_algorithms()
