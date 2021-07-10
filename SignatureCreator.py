import os
from tkinter import *
from tkinter import messagebox

import requests
from PIL import ImageTk


def download_pic(name):
    startUrl = "http://www.uustv.com/"
    if name == "":
        messagebox.showinfo('ERROR', 'please enter your name!')
    else:
        dict_paras = {
            'word': name,
            'sizes': '30',
            'fonts': 'zql.ttf',
            'frontcolor': '#000000'
        }
        result = requests.post(startUrl, data=dict_paras)
        result.encoding = 'utf-8'
        html = result.text
        # print(html)
        # reg = '<div class="tu"><img src="(.*)"/></div>'
        # imagePath = re.findall(reg, html)
        # if len(imagePath)==0:
        #     messagebox.showinfo('ERROR','no signature generated!')
        #     return
        imagePath = html.split('<div class="tu">')[1].split('</div>')[0].split('="')[1].split('"')[0]
        imageUrl = startUrl + imagePath
        # print(imageUrl)
        # return
        response = requests.get(imageUrl).content
        if not os.path.exists('imgs'):
            os.mkdir('imgs')
        with open('imgs/{}.gif'.format(name), 'wb') as f:
            f.write(response)
        bm = ImageTk.PhotoImage(file='imgs/{}.gif'.format(name))
        label2 = Label(frame, image=bm)
        label2.bm = bm
        label2.grid(row=2, columnspan=2)


if __name__ == '__main__':
    root = Tk()
    root.title("Signature Creator")
    root.geometry("700x350")

    frame = Frame(root)
    label = Label(frame, text="Enter your name", font=('arial', 15), fg='green')
    label.grid(row=0, column=0)
    entry = Entry(frame, font=('Arial', 20), fg='green')
    entry.grid(row=0, column=1)
    button = Button(frame, text="Generate", font=('arial', 15), command=lambda: download_pic(entry.get()))
    button.grid(row=0, column=2, padx=5)
    frame.pack(padx=10, pady=10)

    root.mainloop()
