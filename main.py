import argparse

from src.translation_worker import start_translation_process


def main(print_text, print_boxes, plot_clusters, source_lang, target_lang):
    if print_text:
        print("Console output enabled.")
    if print_boxes:
        print("Bounding box output enabled.")
    if plot_clusters:
        print("Cluster plotting enabled.")

    start_translation_process(print_text, print_boxes, plot_clusters, source_lang, target_lang)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Translate text from screenshots.")
    
    parser.add_argument('--print', dest='print_text', action='store_true',
                        help='Print extracted texts to the console')
    parser.add_argument('--print-boxes', dest='print_boxes', action='store_true',
                        help='Print bounding boxes of extracted texts')
    parser.add_argument('--plot', dest='plot_clusters', action='store_true',
                        help='Print clusters of extracted texts')
    
    parser.add_argument('--from', dest='source_lang', type=str, default='eng',
                        help='Specify OCR source language (default: "eng")')
    parser.add_argument('--to', dest='target_lang', type=str, default='eng',
                        help='Specify target translation language (default: "eng")')

    args = parser.parse_args()
    main(args.print_text, args.print_boxes, args.plot_clusters, args.source_lang, args.target_lang)
