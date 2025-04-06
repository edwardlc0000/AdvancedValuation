#

from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        file_menu: QMenu = self.addMenu('&File')
        edit_menu: QMenu = self.addMenu('&Edit')
        help_menu: QMenu = self.addMenu('&Help')

        # File menu actions
        new_action: QAction = QAction("&New", self)
        new_action.setShortcut("Ctrl+N")
        file_menu.addAction(new_action)

        open_action: QAction = QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)

        save_action: QAction = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action: QAction = QAction("&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        file_menu.addAction(exit_action)

        # Edit menu actions
        cut_action: QAction = QAction("&Cut", self)
        cut_action.setShortcut("Ctrl+X")
        edit_menu.addAction(cut_action)

        copy_action: QAction = QAction("&Copy", self)
        copy_action.setShortcut("Ctrl+C")
        edit_menu.addAction(copy_action)

        paste_action: QAction = QAction("&Paste", self)
        paste_action.setShortcut("Ctrl+V")
        edit_menu.addAction(paste_action)

        # Help menu actions
        about_action: QAction = QAction("&About", self)
        help_menu.addAction(about_action)

        self.new_action: QAction = new_action
        self.open_action: QAction = open_action
        self.save_action: QAction = save_action
        self.exit_action: QAction = exit_action
        self.about_action: QAction = about_action
