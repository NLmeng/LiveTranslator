import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import pairwise_distances
from sklearn.neighbors import NearestNeighbors


def plot_k_distance(points, k=3, plot=True):
    """
    Plots the k-distance graph for a set of points to use to determine the optimal epsilon (eps) value for DBSCAN.
    """
    neigh = NearestNeighbors(n_neighbors=k)
    neigh.fit(points)
    distances, indices = neigh.kneighbors(points)
    sorted_distances = np.sort(distances[:, k-1], axis=0)[::-1]
    # plt.plot(sorted_distances)
    # plt.title("K-Distance Graph")
    # plt.xlabel("Points")
    # plt.ylabel(f"Distance to {k}-th Nearest Neighbor")
    # plt.show()
    return sorted_distances


def find_optimal_eps(sorted_distances):
    """
    Determines the optimal eps by finding the elbow point in the sorted k-distance graph.
    First and Second Differences:
    - First difference of the sorted distances measures how much the distance increases from one point to the next.
    - Second difference of the first difference helps to identify (inflection point) where the rate of increase in distance changes significantly.
    Finding the Elbow:
    - The index of the maximum value in the second difference array is identified. This is the point after which the increase in distance becomes not useful.
    """
    diff = np.diff(sorted_distances, n=1)
    second_diff = np.diff(diff, n=1)
    elbow_index = np.argmax(second_diff) + 1
    optimal_eps = sorted_distances[elbow_index]
    return optimal_eps


def get_optimal_eps(points, k=3):
    sorted_distances = plot_k_distance(points, k=k, plot=False)
    optimal_eps = find_optimal_eps(sorted_distances)
    print(f"Optimal eps suggested: {optimal_eps}")
    return optimal_eps


def cluster_text_boxes(text_box_pairs, algorithm='dbscan', print_text=False, plot_cluster=False, min_samples=2, n_clusters=3):
    points = np.array([(x + w / 2, y + h / 2)
                      for _, (x, y, w, h) in text_box_pairs])

    eps = get_optimal_eps(points)
    labels = None
    if algorithm == 'dbscan':
        clustering = DBSCAN(eps=eps,
                            min_samples=min_samples).fit(points)
        labels = clustering.labels_
    elif algorithm == 'kmeans':
        clustering = KMeans(n_clusters=n_clusters, random_state=0).fit(points)
        labels = clustering.labels_
    else:
        raise ValueError("Unsupported clustering algorithm specified")

    clustered_texts = {}
    for label, (text, (x, y, w, h)) in zip(labels, text_box_pairs):
        if label != -1:
            if label not in clustered_texts:
                clustered_texts[label] = {
                    'text': text, 'box': [x, y, x+w, y+h]}
            else:
                existing = clustered_texts[label]
                existing['text'] += " " + text
                existing['box'][0] = min(existing['box'][0], x)
                existing['box'][1] = min(existing['box'][1], y)
                existing['box'][2] = max(existing['box'][2], x + w)
                existing['box'][3] = max(existing['box'][3], y + h)

    if print_text:
        for cluster_id, items in clustered_texts.items():
            box = items['box']
            items['box'] = [box[0], box[1], box[2] - box[0], box[3] - box[1]]
            print(f"Cluster {cluster_id}: {items['text']}, {items['box']}")

    if plot_cluster:
        plt.scatter(points[:, 0], points[:, 1], c=labels, cmap='rainbow')
        plt.title(f"{algorithm.title()} Clustering of Text Boxes")
        plt.xlabel("X coordinate")
        plt.ylabel("Y coordinate")
        plt.gca().invert_yaxis()
        plt.show()

    return [(items['text'], tuple(items['box'])) for _, items in clustered_texts.items()]
