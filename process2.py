import json
import time
from multiprocessing import shared_memory

import NAMES
import indicator
import vknews
import vknewsiojson
import threading

import logging

logging.basicConfig(filename=NAMES.process2_logfile.format(time.time()), level=logging.INFO)

f1, f2, f3 = (None for i in range(3))
shm_lock = None
try:
    shm_lock = shared_memory.SharedMemory(NAMES.process_shm_name, create=True, size=1)
    shm_lock.buf[0] = 1
except FileExistsError:
    shm_lock = shared_memory.SharedMemory(NAMES.process_shm_name, create=False)

ind = indicator.Indicator()





def read_file(filename, var):
    try:
        with open(filename, 'r', encoding='utf-8') as read_file:
            globals()[var] = json.load(read_file)
    except FileNotFoundError:
        pass


def do_cycle():
    global f1, f2, f3
    threading.Thread(target=ind.indicate, args=[NAMES.process2_alive_indicator]).start()
    threading.Thread(target=ind.second_process_checker, args=[NAMES.process1_alive_indicator, True]).start()
    while True:
        while shm_lock.buf[0] != 1 and not ind.is_second_process_dead:
            pass

        shm_lock.buf[0] = 0
        try:
            t1 = threading.Thread(target=read_file, args=[vknewsiojson.text_filename, 'f1'])
            t1.start()
            t2 = threading.Thread(target=read_file, args=[vknewsiojson.photos_filename, 'f2'])
            t2.start()
            t3 = threading.Thread(target=read_file, args=[vknewsiojson.href_filename, 'f3'])
            t3.start()

            t1.join()
            t2.join()
            t3.join()

        except FileNotFoundError:
            pass
        import sqlite3 as sql

        con = sql.connect('DB.sqlite')
        with con:
            cur = con.cursor()
            con.commit()
            cur.execute("CREATE TABLE IF NOT EXISTS `table1` (`id` STRING, `photo` STRING, PRIMARY KEY(`id`, `photo`))")
            cur.execute("CREATE TABLE IF NOT EXISTS `table2` (`id` STRING, `text` STRING, PRIMARY KEY(`id`, `text`))")
            cur.execute("CREATE TABLE IF NOT EXISTS `table3` (`id` STRING, `href` STRING, PRIMARY KEY(`id`, `href`))")

            if f1 == None or f2 == None or f3 == None:
                continue

            news = list()
            for i1, i2, i3 in zip(f1, f2, f3):
                t = vknews.VKNews(i1[1], i1[0], i2[1], i3[1])
                news.append(t)
            print(news[-1])
            for i in news:
                for photo in i.photos:
                    cur.execute(f"INSERT OR IGNORE INTO `table1` VALUES (?, ?)", [i.news_id, photo])

                cur.execute(f"INSERT OR IGNORE INTO `table2` VALUES (?, ?)", [i.news_id, i.text])

                for href in i.href:
                    cur.execute(f"INSERT OR IGNORE INTO `table3` VALUES (?, ?)", [i.news_id, href])

        shm_lock.buf[0] = 1
        time.sleep(1)


do_cycle()
