import json
import os

import vknews
from pathlib import Path


class VKNewsIOJSON:

    def __init__(self):
        self.photos_filename = '1.json'
        self.text_filename = '2.json'
        self.href_filename = '3.json'

        self.__loaded_news = self.load_vknews()

    def __create_file(self, name: str):
        with open(name, 'w', encoding='utf-8') as write_file:
            write_file.write('[')

    def __write_elemnt_to_file(self, name, keys: list):
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
            self.__write_elemnt_to_file(self.photos_filename, [i.news_id, i.photos])
            self.__write_elemnt_to_file(self.text_filename, [i.news_id, i.text])
            self.__write_elemnt_to_file(self.href_filename, [i.news_id, i.href])

    def __load_json_part_from_file(self, name):
        with open(name, 'r', encoding='utf-8') as read_file:
            return json.load(read_file)

    def load_vknews(self):
        out = list()
        try:
            f1 = self.__load_json_part_from_file(self.text_filename)

            f2 = self.__load_json_part_from_file(self.photos_filename)
            f3 = self.__load_json_part_from_file(self.href_filename)

            for i1, i2, i3 in zip(f1, f2, f3):
                t = vknews.VKNews(i1[1], i1[0], i2[1], i3[1])
                out.append(t)
            return out
        except FileNotFoundError:
            return []

    def write_unique_news_to_file(self, news: list):
        self.write_any_news_to_files(list(set(news).difference(set(self.__loaded_news))))
        self.__loaded_news += news.copy()
