import os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication

from sql.requests import *

form_ui_path = os.path.join("qt", "form.ui")
Form, Window = uic.loadUiType(form_ui_path)
app = QApplication([])
window = Window()
form = Form()

def main():
    form.setupUi(window)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()