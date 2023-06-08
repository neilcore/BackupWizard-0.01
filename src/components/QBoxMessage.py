from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtGui import QIcon


def display_message(title, content, icon):
    message = QMessageBox()
    message.setWindowTitle(title)

    window_icon = QIcon(icon)
    message.setWindowIcon(window_icon)
    message.setText(content)
    # message.setFixedSize(QSize(1000, 500))
    message.exec()
