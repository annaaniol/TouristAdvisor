import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

data = np.loadtxt(fname="data.txt", delimiter=",")
print(data.shape)
# X = data[:, :1]
# Y = data[:, 1:2]
# print(X, Y)
# plt.scatter(X, Y)
# plt.show()

db = DBSCAN(eps = 0.01, min_samples=10).fit(data)
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

