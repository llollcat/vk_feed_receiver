import time
from multiprocessing import shared_memory

import NAMES


class SecondProcessWatcher:
    def __init__(self):
        while True:
            try:
                self.shm1 = shared_memory.SharedMemory(NAMES.process2_rf1, create=False)
                self.shm2 = shared_memory.SharedMemory(NAMES.process2_rf2, create=False)
                self.shm3 = shared_memory.SharedMemory(NAMES.process2_rf3, create=False)
            except FileNotFoundError:
                time.sleep(0.5)
                print('Не запущен второй процесс')
                continue
            break

