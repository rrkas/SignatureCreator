import os
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

import requests
from PIL import ImageTk, Image

output_path = "output"


def configure_bg(*components):
    for c in components:
        c["bg"] = "white"


font_map = {
    "Art Lottery": "1.ttf",
    "Even Signed": "zql.ttf",
    "Business Visa": "8.ttf",
    "Bookmarks": "6.ttf",
    "Cheesy Sign": "bzcs.ttf",
    "Cursive": "lfc.ttf",
    "Row Bookmarks": "2.ttf",
    "Individuality Check": "3.ttf",
    "Cute Sign": "yqk.ttf",
}


class HomeScreen:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        configure_bg(self.frame)
        self.load_components()
        self.frame.pack(pady=10)

    def load_components(self):
        label = Label(
            self.frame, text="Signature Generator", font=("Arial", 30, "bold")
        )
        label.pack(padx=15, pady=5)
        configure_bg(label)

        button_width = 20

        single_btn = Button(
            self.frame,
            text="Single Signature",
            font=("Arial", 15),
            width=button_width,
            command=lambda: self._single_generate(),
        )
        single_btn.pack(pady=5)

        batch_btn = Button(
            self.frame,
            text="Batch Signatures",
            font=("Arial", 15),
            width=button_width,
            command=lambda: self._batch_generate(),
        )
        batch_btn.pack(pady=5)

        configure_bg(single_btn, batch_btn)

    def _single_generate(self):
        SingleGeneratorScreen(self.master)
        self.frame.destroy()

    def _batch_generate(self):
        BatchGeneratorScreen(self.master)
        self.frame.destroy()


class SingleGeneratorScreen:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        configure_bg(self.frame)
        self.load_components()
        self.frame.pack(pady=10, padx=15)

    def load_components(self):
        blank_img_path = os.path.join(os.path.dirname(__file__), "blank.jpg")

        label = Label(
            self.frame, text="Enter your name", font=("arial", 15), fg="green"
        )
        label.grid(row=0, column=0)
        entry = Entry(self.frame, font=("Arial", 12), fg="green")
        entry.grid(row=0, column=1)
        configure_bg(label, entry)

        font_frame = Frame(self.frame)

        font_label = Label(font_frame, text="Font", font=("Arial", 15))
        font_label.pack(side=LEFT, padx=15)

        def load_image(img_path=blank_img_path):
            image = Image.open(img_path)
            image = image.resize((500, 200))
            image = ImageTk.PhotoImage(image)
            img_label = Label(self.frame, image=image)
            img_label.image = image
            img_label.grid(row=3, column=0, columnspan=3, pady=10)
            configure_bg(img_label)

        def download_pic(name, font_combobox=None, size=30):
            font = (
                font_map[font_combobox.get() or "zql.ttf"]
                if font_combobox
                else (font_map.values())[1]
            )
            print(name, font, size)
            startUrl = "http://www.uustv.com/"
            if name == "":
                messagebox.showinfo("ERROR", "please enter your name!")
            else:
                dict_paras = {
                    "word": name,
                    "sizes": str(size),
                    "fonts": font,
                    "frontcolor": "#000000",
                }
                result = requests.post(startUrl, data=dict_paras)
                result.encoding = "utf-8"
                html = result.text
                imagePath = (
                    html.split('<div class="tu">')[1]
                    .split("</div>")[0]
                    .split('="')[1]
                    .split('"')[0]
                )
                imageUrl = startUrl + imagePath
                response = requests.get(imageUrl).content
                if not os.path.exists(output_path):
                    os.mkdir(output_path)
                out_file_path = os.path.join(
                    os.path.dirname(__file__), output_path, "{}.gif".format(name)
                )
                with open(out_file_path, "wb") as f:
                    f.write(response)
                load_image(out_file_path)

        font_val = "Even Signed"
        font_combobox = Combobox(font_frame, background="white")
        font_combobox["values"] = list(font_map.keys())
        font_combobox.pack(side=LEFT, padx=5)
        font_combobox.current(1)

        def update_selected(_):
            global font_val
            font_val = font_combobox.get()
            print(
                font_combobox.current(),
                font_combobox.get(),
                font_val,
                font_map[font_val],
            )

        font_combobox.bind("<<ComboboxSelected>>", update_selected)

        font_frame.grid(row=1, column=0, columnspan=3)

        configure_bg(font_frame, font_label)

        load_image()
        button = Button(
            self.frame,
            text="Generate",
            font=("arial", 15),
            command=lambda: download_pic(entry.get(), font_combobox),
        )
        button.grid(row=0, column=2, padx=5)
        configure_bg(button)


class BatchGeneratorScreen:
    def __init__(self, master):
        pass


if __name__ == "__main__":
    root = Tk()
    root.title("Signature Creator")
    root.resizable(False, False)
    configure_bg(root)

    HomeScreen(root)

    root.mainloop()
