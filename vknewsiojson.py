import json
import vknews


class VKNewsIOJSON:
    @staticmethod
    def __photo_to_file_writer(news: vknews.VKNews):
        with open("1.json", 'a', encoding='utf-8') as write_file:
            json.dump([news.id, news.photos], write_file)

    @staticmethod
    def __text_to_file_writer(news: vknews.VKNews):
        with open("2.json", 'a', encoding='utf-8') as write_file:
            json.dump([news.id, news.text], write_file)

    @staticmethod
    def __href_to_file_writer(news: vknews.VKNews):
        with open("3.json", 'a', encoding='utf-8') as write_file:
            json.dump([news.id, news.href], write_file)

    def write_news_to_files(self, news: list):
        for i in news:
            self.__photo_to_file_writer(i)
            self.__text_to_file_writer(i)
            self.__href_to_file_writer(i)
