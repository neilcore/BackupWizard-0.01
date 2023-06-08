import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6 import uic
import subprocess
import psycopg2
from PyQt6.QtGui import QIcon


class MyGui(QMainWindow):
    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi("database-backup-ui.ui", self)
        self.show()

        self.hostLineEdit.setPlaceholderText("Host name")
        self.databaseLineEdit.setPlaceholderText("Database name")
        self.userLineEdit.setPlaceholderText("User name")
        self.passwordLineEdit.setPlaceholderText("Password")
        self.portLineEdit.setPlaceholderText("Port Number")

        self.backupButton.clicked.connect(self.the_button_was_clicked)

        # Set window icon
        icon = QIcon("src/images/window icon/wizard-hat.png")  # Replace with the path to your icon file
        self.setWindowIcon(icon)

    def the_button_was_clicked(self):

        if self.databaseLineEdit.text() and self.hostLineEdit.text() and self.userLineEdit.text() and self.passwordLineEdit.text() and self.portLineEdit.text():

            try:
                con = psycopg2.connect(database=self.databaseLineEdit.text(), user=self.userLineEdit.text(),
                                       password=self.passwordLineEdit.text(), host=self.hostLineEdit.text(),
                                       port=self.portLineEdit.text())
                con.close()
            except psycopg2.Error as e:
                message = QMessageBox()
                message.setWindowTitle("Error connecting to the database")
                message.setText(str(e))
                # message.setFixedSize(QSize(1000, 500))
                message.exec()
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
                    self.resultLabel.setText("Backup created successfully!")
                    self.databaseLineEdit.setText("")
                    self.userLineEdit.setText("")
                    self.passwordLineEdit.setText("")
                except subprocess.CalledProcessError as e:
                    self.resultLabel.setText(f"Backup creation failed: {e}")
        else:
            self.resultLabel.setText('Missing Fields!')


def MainWindow():
    app = QApplication([])
    window = MyGui()
    app.exec()


if __name__ == '__main__':
    MainWindow()
