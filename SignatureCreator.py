from app.home_screen import *

if __name__ == "__main__":
    root = Tk()
    root.title("Signature Creator")
    root.resizable(False, False)
    configure_bg(root)

    HomeScreen(root)

    root.mainloop()
