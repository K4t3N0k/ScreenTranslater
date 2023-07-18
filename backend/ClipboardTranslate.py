#!/usr/bin/python3

from flask import Flask
import argparse
import logging

from Translator import Translator

app = Flask(__name__)
log = logging.Logger()


@app.route("/get_new_text")
def hello():
    log.info('thread front')
    return app.config['translator'].getText()


def getParameters():
    parser = argparse.ArgumentParser(
        prog='Clipboard Transate',
        description='Get screenshot from clipboard and translates it.')
    parser.add_argument('-p', '--tesseract_path',
                        default='C:\\Program Files\\Tesseract-OCR\\tesseract.exe')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', default=5000)
    args = parser.parse_args()
    log.info('running with: tesseract_path={},\nhost={}\nport={}'.format(
        args.tesseract_path, args.host, args.port))
    return args


def main():
    args = getParameters()
    translator = Translator(log, args.tesseract_path)

    app.config['translator'] = translator
    app.run(host=args.host, port=args.port, debug=True, threaded=True)

    translator.stop()


if __name__ == '__main__':
    main()
