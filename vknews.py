from __future__ import print_function

import builtins


class VKNews:
    def __init__(self, text: str,id: str,photos: list, href: list):

        self.text = text
        self.id = id
        self.photos = photos
        self.href = href



    def print(*args, **kwargs):
        builtins.print('New print function')
        return builtins.print(*args, **kwargs)

    def __str__(self):
        return "text: {0}\nid: {1}\nphotos: {2}\nhref: {3}".format(self.text, self.id, str(self.photos), str(self.href) )