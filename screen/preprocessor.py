import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN


def group_text_boxes(text_box_pairs, print_text=False, plot_cluster=False):
    # Extracting the center points of each text box for clustering
    points = np.array([(x + w / 2, y + h / 2)
                      for _, (x, y, w, h) in text_box_pairs])

    # Applying DBSCAN to find clusters
    clustering = DBSCAN(eps=50, min_samples=2).fit(points)
    labels = clustering.labels_

    # Group text and merge bounding boxes within each cluster
    clustered_texts = {}
    for label, (text, (x, y, w, h)) in zip(labels, text_box_pairs):
        if label not in clustered_texts:
            clustered_texts[label] = {'text': text, 'box': [x, y, x+w, y+h]}
        else:
            existing = clustered_texts[label]
            existing['text'] += " " + text
            # Calculate new bounding box dimensions
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
        plt.title("DBSCAN Clustering of Text Boxes")
        plt.xlabel("X coordinate")
        plt.ylabel("Y coordinate")
        plt.gca().invert_yaxis()
        plt.show()

    return [(items['text'], tuple(items['box'])) for _, items in clustered_texts.items()]