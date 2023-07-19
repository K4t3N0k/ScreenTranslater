#!/usr/bin/python3
# -*- coding: utf-8 -*-

from Translator import Translator
import os
import argparse
import logging
from PIL import Image

log = logging.Logger('main')


def getParameters():
    parser = argparse.ArgumentParser(
        prog='Translate single image')
    parser.add_argument('input')
    parser.add_argument('-p', '--tesseract_path', default='C:\\Program Files\\Tesseract-OCR\\tesseract.exe')
    parser.add_argument('--x1', default=250)
    parser.add_argument('--y1', default=770)
    parser.add_argument('--x2', default=1600)
    parser.add_argument('--y2', default=1000)
    args = parser.parse_args()
    log.info('running with: args={}'.format(
        args))
    return args


def main():
    args = getParameters()
    translator = Translator(log, args)

    image = Image.open(args.input)
    translator.push_image(image)
    log.info(translator.getText())

    translator.stop()


if __name__ == '__main__':
    main()
