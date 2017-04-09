from antcolony import AntColony
from antgraph import AntGraph

import pickle
import sys
import traceback


def ant_traverse(num_nodes, cost_mat):

    if num_nodes < len(cost_mat):
        cost_mat = cost_mat[0:num_nodes]
        for i in range(0, num_nodes):
            cost_mat[i] = cost_mat[i][0:num_nodes]

    try:
        print(num_nodes, cost_mat)
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
            print(cities[node] + " ")
        print("\nBest path cost = %s\n" % (best_path_cost,))

    except Exception as e:
        print("exception: " + str(e))
        best_path_cost = sys.maxsize
        traceback.print_exc()

    return best_path_cost


def time_of_trip(path, pace):
    return path/pace


def get_trip():
    cost_mat = stuff[1]
    num_nodes = int(user_trip_time*3)

    path_cost = ant_traverse(num_nodes, cost_mat) / 400
    current_trip_time = time_of_trip(path_cost, slow_walk_pace)

    if current_trip_time != user_trip_time:

        below_time_limit = (current_trip_time < user_trip_time)

        while True:

            if user_trip_time > current_trip_time:
                num_nodes += 1
                if not below_time_limit:
                    return (path_cost, current_trip_time)
                below_time_limit = True
            else:
                num_nodes -= 1
                if below_time_limit:
                    return (prev_path_cost, prev_trip_time)
                below_time_limit = False

            if num_nodes >= 15:
                return (path_cost, current_trip_time)

            prev_path_cost = path_cost
            path_cost = ant_traverse(num_nodes, cost_mat)/400

            prev_trip_time = current_trip_time
            current_trip_time = time_of_trip(path_cost, slow_walk_pace)
            print(current_trip_time)


if __name__ == "__main__":

    user_trip_time = 3.5
    vehicle_pace = 40
    vehicle_waiting_time = 0.1
    slow_walk_pace = 4
    medium_walk_pace = 6
    fast_walk_pace = 8

    num_iterations = 30

    stuff = pickle.load(open("citiesAndDistances.pickled", "rb"), encoding='latin1')
    cities = stuff[0]
    cost_mat = stuff[1]
    print("Path cost and trip time : ", get_trip())

