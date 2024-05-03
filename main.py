import argparse

from src.FrameTranslator import FrameTranslator


def main(args):
    translator = FrameTranslator(
        args.img_src, args.source_lang, args.target_lang, args.print_text, args.print_boxes)
    translator.start_translation_process()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate text from images.")
    parser.add_argument('--src', dest='img_src', type=str,
                        default='', help='Specify path to image (default: "")')
    parser.add_argument('--print', dest='print_text', action='store_true',
                        help='Print extracted texts to the console')
    parser.add_argument('--print-boxes', dest='print_boxes',
                        action='store_true', help='Print bounding boxes of extracted texts')
    parser.add_argument('--from', dest='source_lang', type=str,
                        default='', help='Specify OCR source language (default: "")')
    parser.add_argument('--to', dest='target_lang', type=str, default='eng',
                        help='Specify target translation language (default: "eng")')

    args = parser.parse_args()
    main(args)
