import sys
import ctypes
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from gui.main_window import MainWindow

def main():
    if sys.platform == "win32":
        app_id = "mahyadev.unogame.gui.1"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/icons/icon_256.png"))

    window = MainWindow()
    window.setWindowIcon(QIcon("assets/icons/icon_256.png"))
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
