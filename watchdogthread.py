import threading


class WatchdogThread(threading.Thread):

    def __init__(self):
        super().__init__()

    def run(self):


        import shutil
        import os
        src = '1.json'
        dst = '11.json'
        shutil.copyfile(src, dst)
        with open(dst, 'r', encoding='utf-8') as write_file:
            print(write_file.read())
        os.remove(dst)
        src = '2.json'
        dst = '22.json'
        shutil.copyfile(src, dst)
        with open(dst, 'r', encoding='utf-8') as write_file:
            print(write_file.read())
        os.remove(dst)

        src = '3.json'
        dst = '33.json'
        shutil.copyfile(src, dst)
        with open(dst, 'r', encoding='utf-8') as write_file:
            print(write_file.read())
        os.remove(dst)



