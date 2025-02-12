from app.gui.main_gui import MainGUI
from tkinter import filedialog

if __name__ == '__main__':
    path = filedialog.askopenfilename()
    main = MainGUI(path)
    main.run()

