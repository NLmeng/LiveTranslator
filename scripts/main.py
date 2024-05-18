import argparse
import os
import sys
import pygetwindow as gw
import Quartz

scripts_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(scripts_dir, '..'))
sys.path.append(project_root)

from screen.FrameTranslator import FrameTranslator
from ui.App import start_gui

def list_window_titles():
    """ for windows OS"""
    windows = gw.getAllWindows()
    return [win.title for win in windows if win.isVisible]

def get_window_list():
    """ for macOS"""
    window_list = []
    window_info_list = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
    for window_info in window_info_list:
        window_list.append(window_info.get('kCGWindowName', 'Unknown'))
    return window_list

def translate_text_from_image(img_src, source_lang, target_lang, print_text=False, print_boxes=False, show=False):
    """Translate text from an image."""
    translator = FrameTranslator(
        img_path=img_src, source_lang=source_lang, target_lang=target_lang, print_text=print_text, print_boxes=print_boxes)
    translator.start_translation_process()
    if show:
        translator.show_translated_frame()

def process_translate(args):
    translate_text_from_image(
        args.img_src, args.source_lang, args.target_lang, args.print_text, args.print_boxes, args.show)
    
def use_app(_):
    start_gui()

def parse_args():
    parser = argparse.ArgumentParser(description="Translate text from images.")
    subparsers = parser.add_subparsers(dest='command', required=True)

    translate_parser = subparsers.add_parser('translate', help="Translate text from an image")
    translate_parser.add_argument('--src', dest='img_src', type=str, default='',
                                  help='Specify path to image (default: "")')
    translate_parser.add_argument('--print', dest='print_text', action='store_true',
                                  help='Print extracted texts to the console')
    translate_parser.add_argument('--print-boxes', dest='print_boxes', action='store_true',
                                  help='Print bounding boxes of extracted texts')
    translate_parser.add_argument('--from', dest='source_lang', type=str, default='',
                                  help='Specify OCR source language (default: "")')
    translate_parser.add_argument('--to', dest='target_lang', type=str, default='eng',
                                  help='Specify target translation language (default: "eng")')
    translate_parser.add_argument('--show', dest='show', action='store_true',
                                  help='Show the final translated image')
    translate_parser.set_defaults(func=process_translate)

    gui_parser = subparsers.add_parser('gui', help="Start the GUI for window capture and translation")
    gui_parser.set_defaults(func=use_app)

    return parser.parse_args()

def main():
    args = parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
