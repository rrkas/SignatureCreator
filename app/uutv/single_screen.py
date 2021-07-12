from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

from PIL import ImageTk, Image

from app.data import *


class UutvSingleGeneratorScreen:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        configure_bg(self.frame)
        self.load_components()
        self.frame.pack(pady=10, padx=15)

    def load_components(self):
        window_name = Label(
            self.frame,
            text="uutv Single Signature Generator",
            font=("Arial", 25, "bold"),
        )
        window_name.grid(row=0, column=0, columnspan=3, pady=10)
        label = Label(
            self.frame, text="Enter your name", font=("arial", 15), fg="green"
        )
        label.grid(row=1, column=0)
        entry = Entry(self.frame, font=("Arial", 12), fg="green")
        entry.grid(row=1, column=1)
        configure_bg(window_name, label, entry)

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

        def download_and_load_image(name, font):
            path = download_image(name, font)
            if path is None:
                messagebox.showerror("Name Required", "No name entered!")
                return
            load_image(path)

        font_val = "Even Signed"
        font_combobox = Combobox(font_frame, background="white")
        font_combobox["values"] = list(font_map.keys())
        font_combobox.pack(side=LEFT, padx=5)
        font_combobox.current(1)

        def update_selected(_):
            global font_val
            font_val = font_combobox.get()
            # print(
            #     font_combobox.current(),
            #     font_combobox.get(),
            #     font_val,
            #     font_map[font_val],
            # )

        font_combobox.bind("<<ComboboxSelected>>", update_selected)

        font_frame.grid(row=2, column=0, columnspan=3)

        configure_bg(font_frame, font_label)

        load_image()
        button = Button(
            self.frame,
            text="Generate",
            font=("arial", 15),
            command=lambda: download_and_load_image(entry.get(), font_combobox.get()),
        )
        button.grid(row=1, column=2, padx=5)
        configure_bg(button)
