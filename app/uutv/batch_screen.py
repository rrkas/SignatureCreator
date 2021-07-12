import csv
import secrets
from datetime import datetime
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar

from app.data import *


class UutvBatchGeneratorScreen:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        configure_bg(self.frame)
        self.load_components()
        self.frame.pack(padx=10, pady=10)

    def load_components(self):
        window_name = Label(
            self.frame,
            text="uutv Batch Signature Generator",
            font=("Arial", 25, "bold"),
        )
        window_name.grid(row=0, column=0, columnspan=6, pady=10)
        configure_bg(window_name)

        font_style = ("Arial", 13)

        label_file_path = Label(self.frame, text="No File Selected", font=font_style)
        label_file_path.grid(row=1, column=1, columnspan=3, sticky=W)

        filepath = None
        names_count = None

        def choose_file():
            global filepath, names_count
            filepath = filedialog.askopenfilename(
                initialdir="/",
                title="Select a File",
                filetypes=(
                    ("Text files", "*.txt"),
                    # ("all files", "*.*"),
                ),
            )
            filepath = os.path.normpath(filepath)
            names_count = count_names(filepath)
            label_file_size.configure(text=pretty_file_size(filepath))
            label_count_names.configure(text=str(names_count) + " names")
            label_file_path.configure(text=filepath.split(os.sep)[-1])
            if names_count > 0:
                btn_generate.grid(row=3, column=0, columnspan=5, pady=15)
                configure_bg(btn_generate)
            else:
                btn_generate.grid_forget()

        btn_choose_file = Button(
            self.frame,
            text="Choose file with names",
            font=("Arial", 13),
            command=lambda: choose_file(),
        )
        btn_choose_file.grid(row=1, column=0)
        configure_bg(label_file_path, btn_choose_file)

        meta_frame = Frame(self.frame)

        label_meta = Label(meta_frame, text="File Details", font=font_style, width=35)
        label_meta.pack(side=LEFT)

        label_file_size = Label(meta_frame, text="0 b", font=font_style)
        label_file_size.pack(side=LEFT, padx=15)

        label_count_names = Label(meta_frame, text="0 names", font=font_style)
        label_count_names.pack(side=LEFT, padx=15)

        meta_frame.grid(row=2, column=0, columnspan=2, pady=10)
        configure_bg(meta_frame, label_meta, label_file_size, label_count_names)

        def generate_signs():
            global filepath, names_count
            if filepath is None:
                return
            batch_id = secrets.token_hex(10)
            batch_path = os.path.join(output_path, batch_id)
            progress_var = DoubleVar()
            progress_bar.grid(row=4, column=0, columnspan=6, padx=10, pady=10)
            progress_bar.configure(
                maximum=names_count,
                # background="white", # unknown option "-background"
                variable=progress_var,
            )
            progress_bar["value"] = 0
            if not os.path.exists(batch_path):
                os.mkdir(batch_path)
            with open(os.path.join(batch_path, "_meta.txt"), "w") as f:
                f.write(f"batch_id: {batch_id}\n")
                f.write(f"number of names: {names_count}\n")
                f.write(
                    f"date of generation: {datetime.now().strftime('%d %B %Y - %H:%M:%S')}"
                )
            with open(os.path.join(batch_path, "_names.csv"), "w", newline="") as of:
                csv_writer = csv.writer(of)
                with open(filepath) as inp:
                    ridx = 1
                    for name in inp.readlines():
                        name = name.strip()
                        font = list(font_map.keys())[floor(random() * len(font_map))]
                        dfile_path = download_image(
                            name, font_name=font, batch_id=batch_id
                        )
                        print(dfile_path)
                        if len(name) == 0:
                            continue
                        csv_writer.writerow(
                            [
                                ridx,
                                name,
                                dfile_path.split(os.sep)[-1],
                            ]
                        )
                        progress_var.set(ridx)
                        self.frame.update_idletasks()
                        ridx += 1

        btn_generate = Button(
            self.frame,
            text="Generate Signatures",
            font=font_style,
            command=generate_signs,
        )
        btn_generate.grid_forget()

        progress_bar = Progressbar(
            self.frame, orient=HORIZONTAL, length=100, mode="determinate"
        )
        progress_bar.grid_forget()
