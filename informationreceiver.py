from vknews import *
import vk_api


class InformationReceiver:
    @staticmethod
    def __auth_handler():
        key = input("Enter authentication code: ")
        remember_device = True

        return key, remember_device

    @staticmethod
    def __captcha_handler(captcha):
        key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
        return captcha.try_again(key)

    def __init__(self, token: str):
        vk_session = vk_api.VkApi(token=token, auth_handler=self.__auth_handler,
                                  captcha_handler=self.__captcha_handler)

        self.vk = vk_session.get_api()

    def get_news(self) -> list:
        response = self.vk.newsfeed.get(filters='post')

        news = list()
        if 'items' in response:
            for i in response['items']:

                photos = list()
                urls = list()
                if 'attachments' in i:
                    for i2 in i['attachments']:
                        if 'photo' in i2:
                            photos.append(i2['photo']['sizes'][-1]['url'])  # берём фото лучшего качества
                        if 'link' in i2:
                            urls.append(i2['link']['url'])  # добавляем ссылку

                    element = VKNews(i['text'], i['post_id'], photos, urls)  # 4 арг, ссылки.
                    news.append(element)
        return news
