from ant import Ant
from threading import Lock, Condition
import numpy as np

import random
import sys

class AntColony:
    def __init__(self, graph, num_ants, num_iterations):
        self.graph = graph
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.Alpha = 0.1

        # condition var
        self.cv = Condition()

        self.reset()

    def reset(self):
        self.best_path_cost = sys.maxsize
        self.best_path_vec = None
        self.best_path_mat  = None
        self.last_best_path_iteration = 0

    def start(self):
        self.ants = self.distribute_ants()
        self.iter_counter = 0

        while self.iter_counter < self.num_iterations:
            self.iteration()

            self.cv.acquire()
            # wait until update calls notify()
            self.cv.wait(0.005)

            lock = self.graph.lock
            lock.acquire()
            self.global_updating_rule()
            lock.release()

            self.cv.release()

    # one iteration involves spawning a number of ant threads
    def iteration(self):
        self.avg_path_cost = 0
        self.ant_counter = 0
        self.iter_counter += 1
        for ant in self.ants:
            ant.start()

    # called by individual ants
    def update(self, ant):
        lock = Lock()
        lock.acquire()

        self.ant_counter += 1

        self.avg_path_cost += ant.path_cost

        # book-keeping
        if ant.path_cost < self.best_path_cost:
            self.best_path_cost = ant.path_cost
            self.best_path_mat = ant.path_mat
            self.best_path_vec = ant.path_vec
            self.last_best_path_iteration = self.iter_counter

        if self.ant_counter == len(self.ants):
            self.avg_path_cost /= len(self.ants)
            self.cv.acquire()
            self.cv.notify()
            self.cv.release()
        lock.release()

    def done(self):
        return self.iter_counter == self.num_iterations

    # assign each ant a random start-node
    def distribute_ants(self):
        self.reset()
        permitted_nodes = np.random.permutation(self.graph.num_nodes).tolist()
        ants = []
        for i in range(0, self.num_ants):
            ant = Ant(i, permitted_nodes.pop(), self)
            ants.append(ant)
        
        return ants

    # changes the tau matrix based on evaporation/deposition 
    def global_updating_rule(self):
        evaporation = 0
        deposition = 0

        for r in range(0, self.graph.num_nodes):
            for s in range(0, self.graph.num_nodes):
                if r != s:
                    delt_tau = self.best_path_mat[r][s] / self.best_path_cost
                    evaporation = (1 - self.Alpha) * self.graph.tau(r, s)
                    deposition = self.Alpha * delt_tau

                    self.graph.update_tau(r, s, evaporation + deposition)
