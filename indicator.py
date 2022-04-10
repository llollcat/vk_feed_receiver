import time
from multiprocessing import shared_memory


class Indicator:
    @staticmethod
    def indicate(process_name: str):

        shm = None
        try:
            shm = shared_memory.SharedMemory(name=process_name, create=True, size=1)
        except FileExistsError:
            shm = shared_memory.SharedMemory(name=process_name, create=False)

        shm.buf[0] = 0
        while True:
            shm.buf[0] += 1
            if shm.buf[0] > 100:
                shm.buf[0] = 0
            # print(shm.buf[0])
            time.sleep(0.5)

    def __init__(self):
        self.is_second_process_dead = True
        self.__shm1 = None

    def wait_for_process(self, process_name: str):
        while True:
            try:
                self.__shm1 = shared_memory.SharedMemory(name=process_name, create=False)
                prev = self.__shm1.buf[0]
                time.sleep(0.5)
                if prev != self.__shm1.buf[0]:
                    self.is_second_process_dead = False
                    break
            except FileNotFoundError:
                pass
            print(f'Не запущен {process_name}')
            time.sleep(2)

    def second_process_checker(self, process_name: str, is_need_init=False):
        if (is_need_init):
            self.wait_for_process(process_name)

        prev_value = self.__shm1.buf[0]

        time.sleep(0.5)
        while True:

            if self.__shm1.buf[0] == prev_value:
                self.is_second_process_dead = True
            else:
                self.is_second_process_dead = False

            if self.is_second_process_dead:
                print(f'Не запущен {process_name}')
            time.sleep(1)
