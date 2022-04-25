import logging
import multiprocessing

import const
import mmu


class Process:
    def __init__(self, memmu: mmu.MemoryManagementUnit, pid, mutex: multiprocessing.Lock):
        self.__mmu = memmu
        self.pid = pid
        self.__logging = logging
        logging.info(f"процесс {pid} создан")
        self.__mutex = mutex
        self.__memory = list()

    def do_something_useless(self):
        import random
        self.__mutex.acquire()
        interaction = random.randint(0, 2)
        if interaction == 0:
            logging.info(f'pid:{self.pid}, выделена пямять')
            self.__memory.append(self.__mmu.get_new_memory(self.pid))

        elif interaction == 1:
            if len(self.__memory) != 0:
                logging.info(
                    f'pid:{self.pid}, получено значение: {self.__mmu.get_val_in_memory(self.pid, self.__memory[random.randint(0, len(self.__memory) - 1)])}')

        elif interaction == 2:
            if len(self.__memory) != 0:
                self.__mmu.set_val_in_memory(self.pid, self.__memory[random.randint(0, len(self.__memory) - 1)],
                                             random.randint(0, 10 ** const.n_bits))
                logging.info(f'pid:{self.pid}, установленно новое значение для переменной')

        self.__mutex.release()

    def getmem(self):
        return self.__memory
