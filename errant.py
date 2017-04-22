import random
import itertools
import bisect
import math
from collections import defaultdict

class Errant:


	def trail_value(self, trail):
		val = 0
		for i in range(len(trail)-1):
			val += 1 / (self.metric(trail[i], trail[i+1]) or 1)
		return val

	def weight(self, x, y):
		length = self.metric(x, y) or 1
		length = 1/length
		ph = self.pheromones[(x, y)]		
		we = ph ** self.A + length ** self.B
		return we

	def solve(self):
		best_trail = []
		best_trail_val = None
		for x in range(0,self.L):
			trails = []

			for ant in range(0,self.N):
				trail = []
				nodes = self.nodes.copy()
				random.shuffle(nodes)
				visited = nodes.pop()
				trail.append(visited)

				while(len(nodes)>0):
					weights = []
					for move in nodes:
						weights.append(self.weight(visited, move))
					total = sum(weights)
					cumdist = list(itertools.accumulate(weights)) + [total]
					index = bisect.bisect(cumdist, random.random() * total)
					visited = nodes.pop(index)
					trail.append(visited)
				trails.append(trail)

			for a in self.nodes:
				for b in self.nodes:
					ph = self.pheromones[(a, b)]
					ph = (1-self.rho)*ph
					self.pheromones[(a,b)]= ph
					self.pheromones[(b,a)]= ph
  
			for trail in trails:
				
				trail_eval = self.trail_value(trail)
				trail_len = 0
				for i in range(len(trail)-1):
					a = trail[i]
					b = trail[i+1]

					ph = self.pheromones[(a, b)]
					ph = ph + trail_eval * self.Q
					self.pheromones[(a,b)]= ph
					self.pheromones[(b,a)]= ph
					trail_len += self.metric(a, b)

				if best_trail_val == None:
					best_trail = trail
					best_trail_val = trail_len
				if best_trail_val > trail_len:
					best_trail = trail
					best_trail_val = trail_len
			if self.show_debug:
				print("Iteration: %d Shortest length: %f" % (x,best_trail_val))

		return best_trail

			


	def __init__(self, nodes, metric, Q=1, rho=0.8, N=10, L=100, A=1, B = 3, show_debug = False):
		# Initializes solver
		#
		random.seed(42)
		self.nodes = nodes
		self.metric = metric
		self.Q = Q
		self.rho = rho
		self.N = N
		self.L = L
		self.A = A
		self.B = B
		self.pheromones = defaultdict(lambda: 0.1)
		self.show_debug = show_debug



