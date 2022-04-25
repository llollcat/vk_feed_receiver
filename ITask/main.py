import multiprocessing
import threading
import time

import const
import mmu
import logging
import process

logging.basicConfig(filename=const.logging_file, level=logging.INFO, filemode='w')

mem = mmu.MemoryManagementUnit()

l = multiprocessing.Lock()


def proc(pid):
    it_in_thread = 100
    p = process.Process(mem, pid, l)
    for i in range(it_in_thread):
        p.do_something_useless()
        time.sleep(0.01)


threading.Thread(target=proc, args=[1]).start()
threading.Thread(target=proc, args=[2]).start()
threading.Thread(target=proc, args=[3]).start()
threading.Thread(target=proc, args=[4]).start()
