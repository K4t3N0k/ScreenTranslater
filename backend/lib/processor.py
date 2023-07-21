#!/usr/bin/python3
# -*- coding: utf-8 -*-

from time import sleep
from threading import Thread, Lock
import logging

log = logging.getLogger(__name__)


class Processor(object):
    def __init__(self, config, data_getter, data_processor):
        self._inputData = []
        self._outputData = []
        self._is_running = True
        self._data_getter = data_getter
        self._data_processor = data_processor
        self._max_buffer_length = config.max_buffer_length
        self._dataLock = Lock()
        self._reader = Thread(target=self.input_routine)
        self._writer = Thread(target=self.processing_routine)
        self._reader.start()
        self._writer.start()
        print('logger handlers={}'.format(log.hasHandlers()))

    def stop(self):
        self._is_running = False
        self._reader.join()
        self._writer.join()

    def processing_routine(self):
        self._counter = 0
        while self._is_running:
            data = None
            with self._dataLock:
                if len(self._inputData) != 0:
                    data = self._inputData.pop(0)
                    log.info('New data getted in processing_routine')
            if data is not None:
                text = self._data_processor.process_data(data)
                if text:
                    if len(self._outputData) >= self._max_buffer_length:
                        self._outputData.pop(0)
                    self._outputData.append(text)
                self._counter += 1
            sleep(0.1)

    def input_routine(self):
        while self._is_running:
            data = None
            try:
                data = self._data_getter.get_data()
            except Exception as e:
                log.exception('Accured exception: {}'.format(e))
            if data is not None:
                if len(self._inputData) >= self._max_buffer_length:
                    self._inputData.pop(0)
                self._inputData.append(data)
                log.info('New data getted from data getter')
                log.debug(f'InputQueue size = {len(self._inputData)}')
            sleep(0.1)

    def get_processed_data(self):
        if len(self._outputData) == 0:
            return ""
        return self._outputData.pop(0)

    def push_data(self, data):
        # test purpuses only
        with self._dataLock:
            self._inputData.append(data)

    def get_counter(self):
        return self._counter
