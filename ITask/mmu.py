import logging

import iptable
import ptable
import const
import shutil


class MemoryManagementUnit:
    def __init__(self):
        self.table = dict()
        self.unused_pages = [i for i in range(const.memory_size)]
        self.unused_paging_pages = [i for i in range(const.paging_size)]
        self.written_in_paging_by_Nf_in_ram = dict()  # RAM, paging

    def is_free_ram(self):
        return len(self.unused_pages) > 0

    def purge_memory(self):
        for it2 in self.table.values():
            for it in it2.table:
                if it.P:
                    to_del = None
                    self.unused_pages.append(it.Nf)
                    if it.D or it.Nf not in self.written_in_paging_by_Nf_in_ram:
                        if len(self.unused_paging_pages) == 0:
                            logging.info("Кончился файл подкачки и ОЗУ")
                            exit(0)
                        shutil.move(const.RAM_files + str(it.Nf), const.paging_files + str(self.unused_paging_pages[0]))
                        it.P = False
                        it.Nf = self.unused_paging_pages[0]
                        to_del = self.unused_paging_pages[0]

                        self.unused_paging_pages.pop(0)
                    else:
                        print('не записалось')
                        self.unused_paging_pages.remove(self.written_in_paging_by_Nf_in_ram[it.Nf])
                        to_del = self.written_in_paging_by_Nf_in_ram[it.Nf]

                    for key, value in self.written_in_paging_by_Nf_in_ram.items():
                        if value == to_del:
                            del self.written_in_paging_by_Nf_in_ram[key]
                            break

                    it.P = False

    def load_page_from_paging(self, inner_pages_table: iptable.InnerPagesTable):
        if not self.is_free_ram():
            self.purge_memory()
        if not self.is_free_ram():
            logging.info("Память кочилась")
            exit(0)

        self.unused_paging_pages.append(inner_pages_table.Nf)

        shutil.copy(const.paging_files + str(inner_pages_table.Nf), const.RAM_files + str(self.unused_pages[0]))

        self.written_in_paging_by_Nf_in_ram[self.unused_pages[0]] = inner_pages_table.Nf
        inner_pages_table.Nf = self.unused_pages[0]
        inner_pages_table.P = True
        self.unused_pages.pop(0)

    def get_new_memory(self, pid):
        if pid not in self.table:
            self.table[pid] = ptable.ProcessTable(pid, self)

        return self.table[pid].add_mem()

    def get_val_in_memory(self, pid, offset: int):
        if pid not in self.table:
            raise Exception

        return self.table[pid].get_val(offset)

    def set_val_in_memory(self, pid, offset: int, val: int):
        if pid not in self.table:
            raise Exception
        if len(str(val)) > const.n_bits:
            raise Exception

        return self.table[pid].set_val(offset, val)
