from __future__ import absolute_import

import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6 import uic
import subprocess
import psycopg2
from PyQt6.QtGui import QIcon

# components
from src.components.QBoxMessage import display_message


class MyGui(QMainWindow):
    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi("database-backup-ui.ui", self)
        self.show()

        # placeholders
        self.hostLineEdit.setPlaceholderText("Host name")
        self.databaseLineEdit.setPlaceholderText("Database name")
        self.userLineEdit.setPlaceholderText("User name")
        self.passwordLineEdit.setPlaceholderText("Password")
        self.portLineEdit.setPlaceholderText("Port Number")

        # font sizes
        self.hostLineEdit.setStyleSheet("font-size: 16px;")
        self.databaseLineEdit.setStyleSheet("font-size: 16px;")
        self.userLineEdit.setStyleSheet("font-size: 16px;")
        self.passwordLineEdit.setStyleSheet("font-size: 16px;")
        self.portLineEdit.setStyleSheet("font-size: 16px;")

        self.backupButton.clicked.connect(self.backup_database)

        # Set window icon
        icon = QIcon("src/images/window icon/wizard-hat.png")  # Replace with the path to your icon file
        self.setWindowIcon(icon)

    def check_fields(self):
        if self.databaseLineEdit.text() and self.hostLineEdit.text() and self.userLineEdit.text() and self.passwordLineEdit.text() and self.portLineEdit.text():
            return True
        return False

    def backup_database(self):

        if self.check_fields():

            try:
                con = psycopg2.connect(database=self.databaseLineEdit.text(), user=self.userLineEdit.text(),
                                       password=self.passwordLineEdit.text(), host=self.hostLineEdit.text(),
                                       port=self.portLineEdit.text())
                con.close()
            except psycopg2.Error as e:
                title = "Error connecting to the database"
                content = str(e)  # str() is important
                window_icon = "src/images/window icon/warning.png"
                display_message(title, content, window_icon)

            else:
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                backup_file = f'{desktop_path}\{self.databaseLineEdit.text()}_backup_db.sql'
                # backup_file = f"{self.databaseLineEdit.text()}_backup_db.sql"

                # Construct the pg_dump command
                command = [
                    "pg_dump",
                    f"--dbname=postgresql://{self.userLineEdit.text()}:{self.passwordLineEdit.text()}@{self.hostLineEdit.text()}:{self.portLineEdit.text()}/{self.databaseLineEdit.text()}",
                    f"--file={backup_file}",
                ]

                try:
                    subprocess.run(command, check=True)

                    title = "Success"
                    content = f'Backup created successfully!\n{backup_file}'
                    window_icon = "src/images/window icon/check.png"
                    display_message(title, content, window_icon)

                    self.databaseLineEdit.setText("")
                    self.userLineEdit.setText("")
                    self.passwordLineEdit.setText("")
                except subprocess.CalledProcessError as e:
                    title = "Failed"
                    content = f"Backup creation failed: {str(e)}"
                    window_icon = "src/images/window icon/delete-button.png"
                    display_message(title, content, window_icon)
        else:
            title = "Error"
            content = 'Incomplete Fields!'
            window_icon = "src/images/window icon/warning.png"
            display_message(title, content, window_icon)


def MainWindow():
    app = QApplication([])
    window = MyGui()
    app.exec()


if __name__ == '__main__':
    MainWindow()
