import datetime
import threading
import time
import tkinter as tk
from multiprocessing import shared_memory

import NAMES
import TOKEN
import indicator
import informationreceiver
import vknewsiojson
import watchdogthread

import logging

logging.basicConfig(filename=NAMES.logfile.format(time.time()),
                    level=logging.INFO)

io = vknewsiojson.VKNewsIOJSON()


def to_json():
    ir = informationreceiver.InformationReceiver(TOKEN.vk_token)

    # Из-за вычисления разницы set нужно запускать поток чтобы не зависал GUI
    threading.Thread(target=io.write_unique_news_to_file_in_thread(ir.get_news())).start()


def do_cycle():
    ind = indicator.Indicator()
    threading.Thread(target=ind.indicate, args=[NAMES.process1_alive_indicator]).start()

    # ожидание второго процесса
    t = threading.Thread(target=ind.wait_for_process, args=[NAMES.process2_alive_indicator])
    t.start()
    t.join()

    threading.Thread(target=ind.second_process_checker, args=[NAMES.process2_alive_indicator]).start()

    shm_lock = None
    try:
        shm_lock = shared_memory.SharedMemory(NAMES.process_shm_name, create=True, size=1)
        shm_lock.buf[0] = 1
    except FileExistsError:
        shm_lock = shared_memory.SharedMemory(NAMES.process_shm_name, create=False)

    while True:
        to_json()
        while shm_lock.buf[0] != 1 and not ind.is_second_process_dead:
            pass
        shm_lock.buf[0] = 0
        wd_thread = watchdogthread.WatchdogThread(io)
        wd_thread.start()
        wd_thread.join()
        shm_lock.buf[0] = 1
        time.sleep(1)


logging.info("do_cycle started")
do_cycle()

# GUI
# window = tk.Tk()
# tk.Button(text="json", width=25, height=5, bg="pink", fg="yellow", command=to_json).pack()
# window.mainloop()
