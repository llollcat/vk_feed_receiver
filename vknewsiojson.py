import json
import multiprocessing
import os
import threading
import time
from multiprocessing import shared_memory

import NAMES
import vknews
from pathlib import Path
from threading import Thread

photos_filename = '1.json'
text_filename = '2.json'
href_filename = '3.json'


class VKNewsIOJSON:

    def __init__(self):


        self.first_file_mutex = threading.Lock()
        self.second_file_mutex = threading.Lock()
        self.third_file_mutex = threading.Lock()

        self.mutex_on_calculation = threading.Lock()

        self.loaded_news = self.load_vknews()

    def __create_file(self, name: str):
        with open(name, 'w', encoding='utf-8') as write_file:
            write_file.write('[')

    def __write_element_to_file(self, name, keys: list):
        is_new_file = False
        if not Path(name).is_file():
            self.__create_file(name)
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

    def write_any_news_to_files(self, news: list):
        for i in news:
            self.__write_element_to_file(photos_filename, [i.news_id, i.photos])
            self.__write_element_to_file(text_filename, [i.news_id, i.text])
            self.__write_element_to_file(href_filename, [i.news_id, i.href])

    def write_any_news_to_files_in_thread(self, news: list):
        def f1():

            while self.shm1.buf != 1:
                pass
            self.shm1.buf[0] = 0

            self.first_file_mutex.acquire()
            for i in news:
                self.__write_element_to_file(photos_filename, [i.news_id, i.photos])

            self.first_file_mutex.release()
            self.shm1.buf[0] = 1

        variable1 = Thread(target=f1)

        def f2():

            while self.shm2.buf != 1:
                pass
            self.shm2.buf[0] = 0


            self.second_file_mutex.acquire()

            for i in news:
                self.__write_element_to_file(text_filename, [i.news_id, i.text])

            self.second_file_mutex.release()
            self.shm2.buf[0] = 1



        variable2 = Thread(target=f2)

        def f3():
            while self.shm3.buf != 1:
                pass
            self.shm3.buf[0] = 0


            self.third_file_mutex.acquire()

            for i in news:
                self.__write_element_to_file(href_filename, [i.news_id, i.href])
            self.third_file_mutex.release()
            self.shm3.buf[0] = 1

        variable3 = Thread(target=f3)

        variable1.start()
        variable2.start()
        variable3.start()
        self.mutex_on_calculation.release()

    def __load_json_part_from_file(self, name):
        with open(name, 'r', encoding='utf-8') as read_file:
            return json.load(read_file)

    def load_vknews(self):
        out = list()
        try:
            f1 = self.__load_json_part_from_file(text_filename)

            f2 = self.__load_json_part_from_file(photos_filename)
            f3 = self.__load_json_part_from_file(href_filename)

            for i1, i2, i3 in zip(f1, f2, f3):
                t = vknews.VKNews(i1[1], i1[0], i2[1], i3[1])
                out.append(t)
            return out
        except FileNotFoundError:
            return []

    def write_unique_news_to_file(self, news: list):
        t = list(set(news).difference(set(self.loaded_news)))
        self.write_any_news_to_files(t.copy())
        self.loaded_news += t.copy()

    def write_unique_news_to_file_in_thread(self, news: list):
        self.mutex_on_calculation.acquire()
        t = list(set(news).difference(set(self.loaded_news)))
        self.write_any_news_to_files_in_thread(t.copy())
        self.loaded_news += t.copy()
