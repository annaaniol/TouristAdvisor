import sys
import traceback
import numpy

from antcolony import AntColony
from antgraph import AntGraph
from cluster import Cluster
from geopy import *

def ant_traverse(num_nodes, cost_mat):

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

        ant_colony.start()

        if ant_colony.best_path_cost < best_path_cost:
            best_path_vec = ant_colony.best_path_vec
            best_path_cost = ant_colony.best_path_cost

        print("\n------------------------------------------------------------")
        print("                     Results                                ")
        print("------------------------------------------------------------")
        print("\nBest path = %s" % (best_path_vec,))
        for node in best_path_vec:
            print(cities[node])
            geolocator = Nominatim()
            location = geolocator.reverse("{0}, {1}".format(cities[node][0], cities[node][1]))
            print(location.address)

        edges_len.clear()
        for i in range(len(best_path_vec)-1):
            edges_len.append(cost_mat[best_path_vec[i]][best_path_vec[i+1]])
        last_edge_len = cost_mat[best_path_vec[0]][best_path_vec[-1]]
        edges_len.append(last_edge_len)

        print("\nBest path cost = %s\n" % (best_path_cost,))

    except Exception as e:
        print("exception: " + str(e))
        best_path_cost = sys.maxsize
        traceback.print_exc()

    return best_path_cost


def time_of_trip(walk_pace):

    paths_to_go_by_vehicle = sum([dist for dist in edges_len if dist > 3.0])
    paths_to_walk = sum([dist for dist in edges_len if dist <= 3.0])

    walk_time = paths_to_walk/walk_pace
    ride_time = paths_to_go_by_vehicle/vehicle_pace + vehicle_waiting_time*paths_to_go_by_vehicle
    attractions_time = len(edges_len) * single_attraction_time

    return walk_time + ride_time + attractions_time


def get_trip(walk_pace):
    cost_mat = cost_mat_copy
    num_nodes = int(user_trip_time*3)

    path_cost = ant_traverse(num_nodes, cost_mat)
    current_trip_time = time_of_trip(walk_pace)

    if current_trip_time != user_trip_time:

        below_time_limit = (current_trip_time < user_trip_time)

        while True:

            if user_trip_time > current_trip_time:
                num_nodes += 1
                if not below_time_limit:
                    return path_cost, current_trip_time, num_nodes
                below_time_limit = True
            else:
                num_nodes -= 1
                if below_time_limit:
                    return prev_path_cost, prev_trip_time, num_nodes
                below_time_limit = False

            if num_nodes >= len(cost_mat) or num_nodes < 2:
                return path_cost, current_trip_time, num_nodes

            prev_path_cost = path_cost
            path_cost = ant_traverse(num_nodes, cost_mat)

            prev_trip_time = current_trip_time
            current_trip_time = time_of_trip(walk_pace)

if __name__ == "__main__":

    user_trip_time = 4
    vehicle_pace = 40
    vehicle_waiting_time = 0.1
    slow_walk_pace = 3
    medium_walk_pace = 4.5
    fast_walk_pace = 6
    single_attraction_time = 0.08
    walk_pace = slow_walk_pace

    num_iterations = 100
    edges_len = []

    cluster = Cluster()
    cost_mat = cluster.get_calculate_distance_matrix()
    cost_mat_copy = cost_mat.copy()
    cities = cluster.get_center_coordinate_list()
    print("Path cost, trip time and number of nodes : ", get_trip(walk_pace))
