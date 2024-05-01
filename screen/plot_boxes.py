import matplotlib.pyplot as plt


def plot_text_boxes(text_box_pairs):
    """ Plot bounding boxes of detected text on a scatter plot. """
    x_coords = [box[0] for _, box in text_box_pairs]
    y_coords = [box[1] for _, box in text_box_pairs]

    plt.figure(figsize=(10, 6))
    plt.scatter(x_coords, y_coords, color='red', marker='o')
    plt.title('Text Box Positions')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.show()
