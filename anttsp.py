import sys
import traceback
import numpy

from antcolony import AntColony
from antgraph import AntGraph
from cluster import Cluster
from geopy import *


def ant_traverse(num_nodes, cost_mat, num_iterations, cities, beta, alpha, Q0, Q, rho):

    if num_nodes < len(cost_mat):
        cost_mat = cost_mat[0:num_nodes]
        for i in range(0, num_nodes):
            cost_mat[i] = cost_mat[i][0:num_nodes]

    try:
        graph = AntGraph(num_nodes, cost_mat)
        best_path_vec = None
        best_path_cost = sys.maxsize

        graph.reset_tau()
        ant_colony = AntColony(graph, num_nodes, num_iterations)

        ant_colony.start(beta, alpha, Q0, Q, rho)

        if ant_colony.best_path_cost < best_path_cost:
            best_path_vec = ant_colony.best_path_vec
            best_path_cost = ant_colony.best_path_cost

        print("\n------------------------------------------------------------")
        print("                     Results                                ")
        print("------------------------------------------------------------")
        print("\nBest path = %s" % (best_path_vec,))
        coordinates = [cities[node] for node in best_path_vec]
        coordinates_as_tuples = list(zip(coordinates, range(len(coordinates))))
        # for node in best_path_vec:
        #     print(cities[node])
        #     geolocator = Nominatim()
        #     location = geolocator.reverse("{0}, {1}".format(cities[node][0], cities[node][1]))
        #     print(location.address)

        edges_len = []
        for i in range(len(best_path_vec)-1):
            edges_len.append(cost_mat[best_path_vec[i]][best_path_vec[i+1]])
        last_edge_len = cost_mat[best_path_vec[0]][best_path_vec[-1]]
        edges_len.append(last_edge_len)

    except Exception as e:
        print("exception: " + str(e))
        best_path_cost = sys.maxsize
        edges_len = []
        coordinates = []
        traceback.print_exc()

    return best_path_cost, coordinates_as_tuples, edges_len


def time_of_trip(walk_pace, public_transport_pace, transport_waiting_time, single_attraction_time, edges_len):

    paths_by_public_transport = sum([dist for dist in edges_len if dist > 3.0])
    paths_to_walk = sum([dist for dist in edges_len if dist <= 3.0])

    walk_time = paths_to_walk/walk_pace
    ride_time = paths_by_public_transport / public_transport_pace + transport_waiting_time * paths_by_public_transport
    attractions_time = len(edges_len) * single_attraction_time

    return walk_time + ride_time + attractions_time


def get_trip(walk_pace, public_transport_pace, user_trip_time, transport_waiting_time, single_attraction_time,
             num_iterations, beta, alpha, Q, rho, epsilon, minimal_samples):

#   TODO: Remove
    Q0 = 0.5 

    cluster = Cluster(epsilon, minimal_samples)
    cost_mat = cluster.get_calculate_distance_matrix().copy()
    cities = cluster.get_center_coordinate_list()

    num_nodes = int(user_trip_time*3)

    path_cost, coordinates, edges_len = ant_traverse(num_nodes, cost_mat, num_iterations, cities, beta, alpha, Q0, Q, rho)

    current_trip_time = time_of_trip(walk_pace, public_transport_pace, transport_waiting_time, single_attraction_time, edges_len)

    if current_trip_time != user_trip_time:

        below_time_limit = (current_trip_time < user_trip_time)

        while True:

            if user_trip_time > current_trip_time:
                num_nodes += 1
                if not below_time_limit:
                    print("Path cost, trip time and number of nodes ", path_cost, current_trip_time, num_nodes)
                    return coordinates
                below_time_limit = True
            else:
                num_nodes -= 1
                if below_time_limit:
                    print("Path cost, trip time and number of nodes ", prev_path_cost, prev_trip_time, num_nodes)
                    return prev_coordinates
                below_time_limit = False

            if num_nodes >= len(cost_mat) or num_nodes < 2:
                print("Path cost, trip time and number of nodes ", path_cost, current_trip_time, num_nodes)
                return coordinates

            prev_path_cost, prev_coordinates = path_cost, coordinates
            path_cost, coordinates, edges_len = ant_traverse(num_nodes, cost_mat, num_iterations, cities, beta, alpha,
                                                             Q0, Q, rho)

            prev_trip_time = current_trip_time
            current_trip_time = time_of_trip(walk_pace, public_transport_pace, transport_waiting_time,
                                             single_attraction_time, edges_len)

if __name__ == "__main__":

    # user specifiable parameters :
    SLOW_WALK_PACE = 3
    MEDIUM_WALK_PACE = 4.5
    FAST_WALK_PACE = 6
    public_transport_pace = 40
    user_trip_time = 8
    transport_waiting_time = 0.1
    single_attraction_time = 0.08
    walk_pace = SLOW_WALK_PACE
    num_iterations = 100
    beta = 1
    alpha = 1
    Q0 = 0.5
    Q = 0.9
    rho = 0.1
    epsilon = 0.001
    minimal_samples = 5

    print("List of coordinates : ", get_trip(walk_pace, public_transport_pace, user_trip_time, transport_waiting_time,
                                             single_attraction_time, num_iterations, beta, alpha, Q0, Q, rho, epsilon,
                                             minimal_samples))
