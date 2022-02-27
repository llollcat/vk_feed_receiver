import tkinter as tk

import TOKEN
import informationreceiver
import vknewsiojson


def main():
    ir = informationreceiver.InformationReceiver(TOKEN.vk_token)
    news = ir.get_news()
    io = vknewsiojson.VKNewsIOJSON()
    io.write_news_to_files(news)


window = tk.Tk()

button = tk.Button(text="to json!", width=25, height=5, bg="blue", fg="yellow", command=main)

button.pack()
window.mainloop()