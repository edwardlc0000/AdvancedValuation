

import os
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QFileDialog,
                             QMessageBox)

from widgets.MenuBar import MenuBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle("eVal")

        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.menu_bar.open_action.triggered.connect(self.open_file)
        self.menu_bar.exit_action.triggered.connect(self.close)

    def open_file(self):

        parent_dir: str = os.path.dirname(os.getcwd())
        file_dialog: QFileDialog = QFileDialog()
        file_dialog.setDirectory(parent_dir)

        file_path: str
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Open File",
            "",
            "Excel Files (*.xlsx);;CSV Files (*.csv)"
        )

        if file_path:
            try:
                print(f"Opening file: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()