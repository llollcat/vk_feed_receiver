import json
import logging
import os
import threading

import vknews
from pathlib import Path
from threading import Thread

text_filename = '2.json'
photos_filename = '1.json'
href_filename = '3.json'


class VKNewsIOJSON:

    @staticmethod
    def __load_json_part_from_file(name):
        with open(name, 'r', encoding='utf-8') as read_file:
            return json.load(read_file)

    @staticmethod
    def load_vknews():
        out = list()
        try:
            f1 = VKNewsIOJSON.__load_json_part_from_file(text_filename)

            f2 = VKNewsIOJSON.__load_json_part_from_file(photos_filename)
            f3 = VKNewsIOJSON.__load_json_part_from_file(href_filename)

            for i1, i2, i3 in zip(f1, f2, f3):
                t = vknews.VKNews(i1[1], i1[0], i2[1], i3[1])
                out.append(t)
            return out
        except FileNotFoundError:
            return []

    def __init__(self):
        self.first_file_mutex = threading.Lock()
        self.second_file_mutex = threading.Lock()
        self.third_file_mutex = threading.Lock()
        self.mutex_on_calculation = threading.Lock()
        self.loaded_news = self.load_vknews()

    @staticmethod
    def __write_element_to_file(name, keys: list):
        is_new_file = False
        if not Path(name).is_file():
            with open(name, 'w', encoding='utf-8') as write_file:
                write_file.write('[')
            is_new_file = True
        else:
            with open(name, 'rb+') as filehandle:
                filehandle.seek(-1, os.SEEK_END)
                filehandle.truncate()

        with open(name, 'a', encoding='utf-8') as write_file:
            if not is_new_file:
                write_file.write(',')
            json.dump(keys, write_file)
            write_file.write(']')

    def write_any_news_to_files_in_thread(self, news: list):

        def f1():
            self.second_file_mutex.acquire()

            for i in news:
                self.__write_element_to_file(text_filename, [i.news_id, i.text])

            self.second_file_mutex.release()

        thread1 = Thread(target=f1)

        def f2():
            self.first_file_mutex.acquire()
            for i in news:
                self.__write_element_to_file(photos_filename, [i.news_id, i.photos])

            self.first_file_mutex.release()

        thread2 = Thread(target=f2)

        def f3():
            self.third_file_mutex.acquire()

            for i in news:
                self.__write_element_to_file(href_filename, [i.news_id, i.href])
            self.third_file_mutex.release()

        thread3 = Thread(target=f3)

        thread1.start()
        thread2.start()
        thread3.start()
        logging.info("write news in thread  to files started")

    def write_unique_news_to_file_in_thread(self, news: list):
        self.mutex_on_calculation.acquire()
        t = list(set(news).difference(set(self.loaded_news)))
        self.loaded_news += t.copy()
        self.write_any_news_to_files_in_thread(t.copy())
        self.mutex_on_calculation.release()
