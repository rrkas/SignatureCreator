from app.uutv.batch_screen import *
from app.uutv.single_screen import *


# Home screen: show menu for single and batch generation
class HomeScreen:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
        configure_bg(self.frame)
        self.load_components()
        self.frame.pack(pady=10)

    def load_components(self):
        label = Label(
            self.frame,
            text="Signature Generator",
            font=("Arial", 25, "bold"),
        )
        label.pack(padx=15, pady=5)
        configure_bg(label)

        button_width = 20
        btn_font = ("Arial", 13)

        single_btn = Button(
            self.frame,
            text="Single Signature",
            font=btn_font,
            width=button_width,
            command=lambda: self._uutv_single_generate(),
        )
        single_btn.pack(pady=5)

        batch_btn = Button(
            self.frame,
            text="Batch Signatures",
            font=btn_font,
            width=button_width,
            command=lambda: self._uutv_batch_generate(),
        )
        batch_btn.pack(pady=5)

        configure_bg(single_btn, batch_btn)

    def _uutv_single_generate(self):
        UustvSingleGeneratorScreen(self.master)
        self.frame.destroy()

    def _uutv_batch_generate(self):
        UustvBatchGeneratorScreen(self.master)
        self.frame.destroy()
