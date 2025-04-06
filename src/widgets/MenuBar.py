#

from PyQt6.QtWidgets import QWidget, QMenuBar
from PyQt6.QtGui import QAction

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        file_menu = self.addMenu('&File')
        edit_menu = self.addMenu('&Edit')
        help_menu = self.addMenu('&Help')

        new_action = QAction("&New", self)
        new_action.setShortcut("Ctrl+N")
        file_menu.addAction(new_action)

        open_action = QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)

        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        file_menu.addAction(exit_action)

        # Edit menu actions
        cut_action = QAction("&Cut", self)
        cut_action.setShortcut("Ctrl+X")
        edit_menu.addAction(cut_action)

        copy_action = QAction("&Copy", self)
        copy_action.setShortcut("Ctrl+C")
        edit_menu.addAction(copy_action)

        paste_action = QAction("&Paste", self)
        paste_action.setShortcut("Ctrl+V")
        edit_menu.addAction(paste_action)

        # Help menu actions
        about_action = QAction("&About", self)
        help_menu.addAction(about_action)

        # Store actions as instance variables to access them later
        self.new_action = new_action
        self.open_action = open_action
        self.save_action = save_action
        self.exit_action = exit_action
        self.about_action = about_action
