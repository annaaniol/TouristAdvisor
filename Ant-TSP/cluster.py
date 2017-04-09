import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from geopy.distance import vincenty
from collections import defaultdict

class Cluster:

    def __init__(self):
        self.data_source = "../downloader/new_data.txt"
        self.data = self.load_data()
        self.eps = 0.001
        self.min_samples = 5
        self.labels = ""
        self.grouped = defaultdict(list)
        self.points = []
        self.centers = dict()
        self.unique_labels = set()
        self.distances = []
        self.center_coordinates = []

    def load_data(self):
        return np.loadtxt(self.data_source, delimiter=',')

    def cluster_and_plot(self):
        db = DBSCAN(self.eps, self.min_samples).fit(self.data)
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        self.labels = db.labels_
        n_clusters_ = len(set(self.labels)) - (1 if -1 in self.labels else 0)
        self.unique_labels = set(self.labels)
        colors = plt.cm.Spectral(np.linspace(0, 1, len(self.unique_labels)))
        for k, col in zip(self.unique_labels, colors):
            if k == -1:
        # Black used for noise.
                col = 'k'
        class_member_mask = (self.labels == k)
        xy = self.data[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)

        xy = self.data[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=6)
        plt.title('Estimated number of clusters: %d' % n_clusters_)
        plt.show()

    def group_data(self):
        self.points = zip(self.data, self.labels)
        for value, key in self.points:
            self.grouped[key].append(value)


    def calculate_centers(self):
        for label in self.grouped:
            values = (self.grouped.get(label))
            sum_x = 0
            sum_y = 0
            for point in values:
                sum_x = sum_x + point[0]
                sum_y = sum_y + point[1]
                self.centers[label] = ((sum_x / len(values), sum_y / len(values)), len(values))

    def remove_unclustered_points(self):
        self.centers.pop(-1)

    def calculate_distance_matrix(self):
        self.distances = np.zeros((len(self.unique_labels)-1, len(self.unique_labels)-1))
        for first in range(len(self.distances)):
            for second in range(len(self.distances)):
                self.distances[first, second] = vincenty(self.centers.get(first)[0],
                                                 self.centers.get(second)[0]).kilometers

    def prepare_center_coordinates_list(self):
        self.center_coordinates = (sorted(cluster.centers.values(), key=lambda x: x[1]))
        self.center_coordinates.reverse()
        self.center_coordinates = [x[0] for x in self.center_coordinates]

    def get_calculate_distance_matrix(self):
        self.load_data()
        self.cluster_and_plot()
        self.group_data()
        self.calculate_centers()
        self.remove_unclustered_points()
        self.calculate_distance_matrix()
        self.prepare_center_coordinates_list()
        return self.distances.tolist()

    def get_center_coordinate_list(self):
        return self.center_coordinates

cluster = Cluster()

print(type(cluster.get_calculate_distance_matrix()))