from datetime import datetime
from PyQt5.QtWidgets import QFileDialog

from rsa import RSA, Encrypter, Decrypter
from rsa import FILES_FOLDER, KEYS_FOLDER, DEC_FOLDER, ENC_FOLDER
from ui import Ui_MainWindow
from PyQt5 import QtWidgets
import sys


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.rsa = RSA()
        self.enc, self.dec = self.rsa.enc_dec_factory()
        self.regen_keys()
        self.cur_files = []
        self.setWindowTitle("RSA")
        self.loadFilesButton.clicked.connect(self.set_input_files)
        self.encryptFilesButton.clicked.connect(self.encrypt_files)
        self.decryptFilesButton.clicked.connect(self.decrypt_files)
        self.saveKeysButton.clicked.connect(self.save_keys)
        self.loadKeysButton.clicked.connect(self.load_keys)
        self.regenKeysButton.clicked.connect(self.regen_keys)

    def upd_enc_dec(self):
        self.enc, self.dec = self.rsa.enc_dec_factory()

    def set_input_files(self):
        options = QFileDialog.Options()

        file_dialog = QFileDialog()
        file_dialog.setFileMode(
            QFileDialog.ExistingFiles)
        file_dialog.setOptions(options)
        file_dialog.setDirectory(FILES_FOLDER)

        file_names, _ = file_dialog.getOpenFileNames(self, "Выберите файлы", "",
                                                     "Все файлы (*)")
        if file_names:
            self.cur_files = list(zip(
                file_names, list(map(lambda x: x.split("/")[-1], file_names))
            ))

    def encrypt_files(self):
        if not self.cur_files:
            self.logTextBrowser.append("Файлы не выбраны")
        for filepath, filename in self.cur_files:
            with open(filepath, "rb") as file:
                file_bytes = file.read()
            enc_bytes = self.enc.encrypt(file_bytes)
            enc_filepath = ENC_FOLDER + filename + ".enc"
            with open(enc_filepath, "wb") as file:
                file.write(enc_bytes)
            self.logTextBrowser.append(f"{filename} сохранен в {enc_filepath}")

    def decrypt_files(self):
        if not self.cur_files:
            self.logTextBrowser.append("Файлы не выбраны")
        for filepath, filename in self.cur_files:
            if not filename.endswith(".enc"):
                self.logTextBrowser.append(
                    f"Файл не является зашифрованным {filename}")
                continue
            with open(filepath, "rb") as file:
                file_bytes = file.read()
            try:

                dec_bytes = self.dec.decrypt(file_bytes)
            except OverflowError:
                self.logTextBrowser.append(
                    f"Произошла ошибка при расшифровке {filename}")
                continue

            dec_filepath = DEC_FOLDER + filename.replace(
                ".enc", ""
            )
            with open(dec_filepath, "wb") as file:
                file.write(dec_bytes)
            self.logTextBrowser.append(f"{filename} сохранен в {dec_filepath}")

    def regen_keys(self):
        self.rsa = RSA()
        self.upd_enc_dec()
        self.logTextBrowser.append(f"Ключи сгенерированы:\n"
                                   f"N={self.rsa.N}\n"
                                   f"s={self.rsa.s}\n"
                                   f"e={self.rsa.e}")

    def save_keys(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name: str
        file_name, _ = QFileDialog.getSaveFileName(self,
                                                   'Выбрать файл и папку',
                                                   KEYS_FOLDER,
                                                   "JSON Files (*.json)",
                                                   options=options)
        if not file_name:
            return
        if not file_name.endswith(".json"):
            file_name += ".json"

        self.rsa.save_keys(file_name)
        self.logTextBrowser.append(f"Ключи сохранены в файл {file_name}")

    def load_keys(self):
        options = QFileDialog.Options()

        file_dialog = QFileDialog()
        file_dialog.setFileMode(
            QFileDialog.ExistingFiles)
        file_dialog.setOptions(options)
        file_dialog.setDirectory(KEYS_FOLDER)

        file_name, _ = file_dialog.getOpenFileName(self, "Выберите файл", "",
                                                   "JSON Files (*.json)")
        if file_name:
            self.rsa.load_keys(file_name)
            self.logTextBrowser.append(
                f"Ключи загружены из файла {file_name}"
            )
        self.upd_enc_dec()


def main():
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
