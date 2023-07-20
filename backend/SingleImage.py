#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import argparse
from time import sleep

from PIL import Image

from lib.config import Config
from lib.image_getter import ImageGetter
from lib.image_translater import ImageTranslater
from lib.processor import Processor
from lib.utils import make_logger

log = None


def getParameters():
    parser = argparse.ArgumentParser(prog='Translate single image')

    parser.add_argument('input')
    parser.add_argument('-c', '--config-path', default='config.ini')

    args = parser.parse_args()
    config = Config(os.path.dirname(__file__), args.config_path)

    return (config, args.input)


def main():
    (config, input_image) = getParameters()
    log = make_logger(config)
    log.info('==========Started==========\ninput_image={}, config={}'.format(
        input_image, config.to_dict()))

    translator = Processor(log, config, ImageGetter(),
                           ImageTranslater(log, config))

    image = Image.open(input_image)
    translator.push_data(image)
    while translator.get_counter() == 0:
        sleep(0.1)
    log.info('result={}'.format(translator.get_processed_data()))

    translator.stop()


if __name__ == '__main__':
    main()
