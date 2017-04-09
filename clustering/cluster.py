import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from geopy.distance import vincenty
from collections import defaultdict

data = np.loadtxt(fname="../downloader/new_data.txt", delimiter=",")

db = DBSCAN(eps = 0.001, min_samples=5).fit(data)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
labels = db.labels_
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'

    class_member_mask = (labels == k)

    xy = data[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)

    xy = data[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
points = zip(data, labels)

points = zip(data, labels)
grouped = defaultdict(list)
for value, key in points:
    grouped[key].append(value)

centers = dict()
for label in grouped:
    values = (grouped.get(label))
    sum_x = 0
    sum_y = 0
    for point in values:
        sum_x = sum_x + point[0]
        sum_y = sum_y + point[1]
    centers[label] = ((sum_x / len(values), sum_y / len(values)), len(values))

centers.pop(-1)
distances = np.zeros((len(unique_labels)-1, len(unique_labels)-1))

for first in range(len(distances)):
    for second in range(len(distances)):
        distances[first, second] = vincenty(centers.get(first)[0], centers.get(second)[0]).meters

print(distances)