from errant import Errant
import random
import math

nodes = []
for _ in range(200):
  x = random.uniform(-10, 10)
  y = random.uniform(-10, 10)
  nodes.append((x, y))

def metric(a, b):
    return math.sqrt(pow(a[1] - b[1], 2) + pow(a[0] - b[0], 2))

ant = Errant(nodes, metric, show_debug=True)
ant.solve()