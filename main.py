import threading
import tkinter as tk

import TOKEN
import informationreceiver
import vknewsiojson
import watchdogthread

io = vknewsiojson.VKNewsIOJSON()

#todo исправить дедлок, отключить менеджер ресурсов на проверку shared memory
#todo сыметировать стратегию замещения из виртуальной
def out():
    wd_thread = watchdogthread.WatchdogThread(io)
    wd_thread.start()


def main():
    ir = informationreceiver.InformationReceiver(TOKEN.vk_token)

    # Из-за вычисления разницы set нужно запускать поток чтобы не зависал GUI
    threading.Thread(target=io.write_unique_news_to_file_in_thread(ir.get_news())).start()


def write_to_DB():
    import sqlite3 as sql

    con = sql.connect('DB.db')
    with con:
        cur = con.cursor()
        con.commit()
        cur.execute("CREATE TABLE IF NOT EXISTS `table1` (`id` STRING, `photo` STRING)")
        cur.execute("CREATE TABLE IF NOT EXISTS `table2` (`id` STRING, `text` STRING)")
        cur.execute("CREATE TABLE IF NOT EXISTS `table3` (`id` STRING, `href` STRING)")

        for i in io.loaded_news:


            for k in i.photos:
                cur.execute(f"INSERT INTO `table1` VALUES ('{i.news_id}', '{k}')")
            cur.execute(f"INSERT INTO `table2` VALUES ('{i.news_id}', '{i.text}')")
            for k in i.href:
                cur.execute(f"INSERT INTO `table3` VALUES ('{i.news_id}', '{k}')")


# GUI
window = tk.Tk()

button = tk.Button(text="json", width=25, height=5, bg="pink", fg="yellow", command=main)

button.pack()
button1 = tk.Button(text="Вывести", width=25, height=5, bg="#FFFFFF", fg="yellow", command=out)

button.pack()
button1.pack()

button2 = tk.Button(text="запись бд", width=25, height=5, bg="#FFFFFF", fg="green", command=write_to_DB)
button2.pack()

window.mainloop()
