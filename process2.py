import json
import time

import NAMES
import vknewsiojson
import threading

from multiprocessing import shared_memory

f1, f2, f3 = (list() for i in range(3))

internal_mem_f1 = shared_memory.SharedMemory(NAMES.process2_rf1, create=True, size=1)
internal_mem_f1.buf[0] =1

internal_mem_f2 = shared_memory.SharedMemory(NAMES.process2_rf2, create=True, size=1)
internal_mem_f2.buf[0] =1

internal_mem_f3 = shared_memory.SharedMemory(NAMES.process2_rf3, create=True, size=1)
internal_mem_f3.buf[0] =1


def read_file1():
    global f1, internal_mem_f1

    while(internal_mem_f1.buf[0] != 1):
        pass
    internal_mem_f1.buf[0] = 0

    name = vknewsiojson.photos_filename
    with open(name, 'r', encoding='utf-8') as read_file:
        f1 = read_file.read()

    internal_mem_f1.buf[0] = 1

def read_file2():
    global f2, internal_mem_f2

    while(internal_mem_f2.buf[0] != 1):
        pass
    internal_mem_f2.buf[0] = 0


    name = vknewsiojson.text_filename
    with open(name, 'r', encoding='utf-8') as read_file:
        f2= json.load(read_file)


    internal_mem_f2.buf[0] = 1

def read_file3():
    global f3,  internal_mem_f3

    while(internal_mem_f3.buf[0] != 1):
        pass
    internal_mem_f3.buf[0] = 0

    name = vknewsiojson.href_filename
    with open(name, 'r', encoding='utf-8') as read_file:
        f3= json.load(read_file)

    internal_mem_f3.buf[0] = 1

def main():

    
    while(True):

        try:
            t1 = threading.Thread(read_file1())
            t1.start()
            t2 = threading.Thread(read_file1())
            t2.start()
            t3 = threading.Thread(read_file1())
            t3.start()

            t1.join()
            t2.join()
            t3.join()
        except FileNotFoundError:
            pass

        time.sleep(0.1)






main()
