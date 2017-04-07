import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

data = np.fromfile("../downloader/data.txt")
print(data)
data_reshaped = data.reshape(data, (-1, 2))
print(data_reshaped)
print(data_reshaped.shape)