import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN, KMeans


def cluster_text_boxes(text_box_pairs, algorithm='dbscan', print_text=False, plot_cluster=False, eps=50, min_samples=2, n_clusters=3):
    points = np.array([(x + w / 2, y + h / 2)
                      for _, (x, y, w, h) in text_box_pairs])

    labels = None
    if algorithm == 'dbscan':
        clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(points)
        labels = clustering.labels_
    elif algorithm == 'kmeans':
        clustering = KMeans(n_clusters=n_clusters, random_state=0).fit(points)
        labels = clustering.labels_
    else:
        raise ValueError("Unsupported clustering algorithm specified")

    clustered_texts = {}
    for label, (text, (x, y, w, h)) in zip(labels, text_box_pairs):
        if label not in clustered_texts:
            clustered_texts[label] = {'text': text, 'box': [x, y, x+w, y+h]}
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
