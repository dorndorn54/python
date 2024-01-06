###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

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
def greedy_cow_transport(cows,limit=10):
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
    final_list = list()
    # sort the cows into a list of tuples
    cow_list = sorted(cows.items(), key=lambda x: x[1], reverse=True)
    trip_count = 0
    while len(cow_list) > 0:
        trip_limit = limit
        # append empty list to add to later
        final_list.append([])
        cows_to_remove = list()
        for cow in cow_list:
            # add the biggest value possible
            if cow[1] <= trip_limit:
                # add the cow name
                final_list[trip_count].append(cow[0])
                # add the positon of the cow tuple to remove later
                cows_to_remove.append(cow_list.index(cow))
                # update the trip limit
                trip_limit -= cow[1]
        trip_count += 1
    # remove the cows from the list by the position of the cow
    for cow_index in cows_to_remove:
        cow_list.pop(cow_index)
    # return the list back
    return final_list


# Problem 3
def brute_force_cow_transport(cows,limit=10):
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
    # make a copy of the trip so does not intefere with iteration
    for trip in total_trips.copy():
        # iterate through each partition
        temp_limit = limit
        for i in map(lambda x: x[1], trip):
            # check if sum of that partition exceed
            temp_limit -= i
        # if so delete
        if temp_limit < 0:
            total_trips.remove(trip)
    # now total_trips is a list of all possible partitions
    # need to convert it to a lists of lists with just names
    export_list = list()
    # iterate over the count of total partitions left
    for count, element in enumerate(total_trips):
        # give empty list for the map function to append to later
        export_list.append([])
        # total_trips[i] represents the partition
        # map function accesses each element in the tuple of the partition
        for j in map(lambda x: x[0], total_trips[count]):
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
    # TODO: Your code here
    pass
