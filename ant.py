import math
from threading import *


class Ant(Thread):
    def __init__(self, ID, start_node, colony, beta, alpha, Q0, Q, rho):
        Thread.__init__(self)
        self.ID = ID
        self.start_node = start_node
        self.colony = colony

        self.curr_node = self.start_node
        self.graph = self.colony.graph
        self.path_vec = []
        self.path_vec.append(self.start_node)
        self.path_cost = 0

        # same meaning as in standard equations
        self.Beta = beta
        self.Alpha = alpha
        #self.Q0 = 1  # Q0 = 1 works just fine for 10 city case (no explore)
        self.Q0 = Q0
        self.Q = Q  # pheromone constant value
        self.Rho = rho

        # store the nodes remaining to be explored here
        self.nodes_to_visit = {}

        for i in range(0, self.graph.num_nodes):
            if i != self.start_node:
                self.nodes_to_visit[i] = i

        # create n X n matrix 0'd out to start
        self.path_mat = []

        for i in range(0, self.graph.num_nodes):
            self.path_mat.append([0]*self.graph.num_nodes)

    # override Thread's run()
    def run(self):
        graph = self.colony.graph
        while not self.end():
            # we need exclusive access to the graph
            graph.lock.acquire()
            new_node = self.state_transition_rule(self.curr_node)
            self.path_cost += graph.delta(self.curr_node, new_node)

            self.path_vec.append(new_node)
            self.path_mat[self.curr_node][new_node] = 1  #adjacency matrix representing path

            self.local_updating_rule(self.curr_node, new_node, self.path_cost)
            graph.lock.release()

            self.curr_node = new_node

        # don't forget to close the tour
        self.path_cost += graph.delta(self.path_vec[-1], self.path_vec[0])

        # send our results to the colony
        self.colony.update(self)

        # allows thread to be restarted (calls Thread.__init__)
        self.__init__(self.ID, self.start_node, self.colony, self.Beta, self.Alpha, self.Q0, self.Q, self.Rho)

    def end(self):
        return not self.nodes_to_visit 

    def key_with_max_val(self, d):
        v = list(d.values())
        k = list(d.keys())
        return k[v.index(max(v))]

    # determines next node to visit after curr_node
    def state_transition_rule(self, curr_node):
        graph = self.colony.graph
        max_node = -1

        max_val = -1
        nominator = {}

        for node in self.nodes_to_visit.values():
            if graph.tau(curr_node, node) == 0:
                raise Exception("tau = 0")

            nominator[node] = math.pow(graph.tau(curr_node, node), self.Alpha) *\
                math.pow(graph.etha(curr_node, node), self.Beta)
        sum = 0
        node = -1

        for node in self.nodes_to_visit.values():
            if graph.tau(curr_node, node) == 0:
                raise Exception("tau = 0")
            sum += math.pow(graph.tau(curr_node, node), self.Alpha) * math.pow(graph.etha(curr_node, node), self.Beta)
        if sum == 0:
            raise Exception("sum = 0")

        p = {}

        for node in self.nodes_to_visit.values():
            p[node] = nominator[node] / sum
        max_node = self.key_with_max_val(p)

        if max_node == -1:
            max_node = node

        if max_node < 0:
            raise Exception("max_node < 0")

        del self.nodes_to_visit[max_node]
        del p[max_node]
        del nominator[max_node]

        return max_node

    # pheromone update rule for indiv ants
    def local_updating_rule(self, curr_node, next_node, path_cost):
        graph = self.colony.graph
        val = self.Rho * graph.tau(curr_node, next_node) + (self.Q / path_cost)
        graph.update_tau(curr_node, next_node, val)
