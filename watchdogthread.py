import logging
import threading

import vknewsiojson


class WatchdogThread(threading.Thread):

    def __init__(self, vioj: vknewsiojson.VKNewsIOJSON):
        super().__init__()
        self.__vioj = vioj

    def run(self):
        self.__vioj.first_file_mutex.acquire()
        with open(vknewsiojson.photos_filename, 'r', encoding='utf-8') as write_file:
            print(write_file.read())
        self.__vioj.first_file_mutex.release()

        self.__vioj.second_file_mutex.acquire()
        with open(vknewsiojson.text_filename, 'r', encoding='utf-8') as write_file:
            print(write_file.read())
        self.__vioj.second_file_mutex.release()

        self.__vioj.third_file_mutex.acquire()
        with open(vknewsiojson.href_filename, 'r', encoding='utf-8') as write_file:
            print(write_file.read())
        self.__vioj.third_file_mutex.release()
        logging.info("watchdog thread ended")
