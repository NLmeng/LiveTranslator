import argparse

from src.translation_worker import start_translation_process


def main(print_text):
    if print_text:
        print("Text extraction and translation with console output enabled.")
        start_translation_process(print_text)
    else:
        start_translation_process()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Translate text from screenshots.")
    parser.add_argument('--print', dest='print_text', action='store_true',
                        help='Print extracted texts to the console')
    args = parser.parse_args()
    main(args.print_text)
