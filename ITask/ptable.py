import logging

import iptable
import const


# noinspection PyPep8Naming
class ProcessTable:
    def __init__(self, pid, memmu):
        self.__mmu = memmu
        self.__offset = 0
        self.__size = 0
        self.pid = pid
        self.table = list()

    def add_mem(self):

        if self.__size % const.page_size == 0:
            if not self.__mmu.is_free_ram():
                self.__mmu.purge_memory()

            if not self.__mmu.is_free_ram():
                logging.info("Память кочилась")
                exit(0)
            self.table.append(iptable.InnerPagesTable(self.__mmu.unused_pages[0]))

            with open(const.RAM_files + str(self.__mmu.unused_pages[0]), 'w') as file:
                file.write(('0' * const.n_bits + '\n') * const.page_size)

            self.__mmu.unused_pages.pop(0)

        self.__size += 1
        self.__offset += 1
        return self.__offset - 1

    def get_val(self, offset):
        if not self.table[offset // const.page_size].P:
            self.__mmu.load_page_from_paging(self.table[offset // const.page_size])
            self.table[offset // const.page_size].P = True

            # изменение таблицы
        self.table[offset // const.page_size].A = True

        with open(const.RAM_files + str(self.table[offset // const.page_size].Nf), 'r') as f:
            f.seek((offset % const.page_size) * const.n_bits + 1)
            return f.readline()

    def set_val(self, offset, val: int):
        if not self.table[offset // const.page_size].P:
            self.__mmu.load_page_from_paging(self.table[offset // const.page_size])

        temp = None
        try:
            with open(const.RAM_files + str(self.table[offset // const.page_size].Nf), 'r') as f:
                temp = f.read().split()
        except FileNotFoundError:
            pass

        with open(const.RAM_files + str(self.table[offset // const.page_size].Nf), 'w') as f:
            if temp is None:
                f.write(str(val).rjust(const.n_bits, '0'))
            else:
                c = 0
                for i in temp:
                    if c != offset % const.page_size:
                        f.write(i + '\n')
                    else:
                        f.write(str(val).rjust(const.n_bits, '0') + '\n')
                    c += 1

        # изменение таблицы

        self.table[offset // const.page_size].A = True
        self.table[offset // const.page_size].D = True
