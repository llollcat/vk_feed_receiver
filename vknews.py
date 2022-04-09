from __future__ import print_function


class VKNews:
    def __init__(self, text: str, news_id: str, photos: list, href: list):
        self.text = text
        self.news_id = news_id
        self.photos = photos
        self.href = href

    def __str__(self):
        return "text: {0}\nnews_id: {1}\nphotos: {2}\nhref: {3}".format(self.text, self.news_id, str(self.photos),
                                                                        str(self.href))

    def __hash__(self):
        return hash(self.news_id)

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.news_id == other.news_id
