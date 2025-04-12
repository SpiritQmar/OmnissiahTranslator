import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QCheckBox, QTabWidget
)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt


class PerevodApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Omnissiah")
        self.setGeometry(200, 200, 800, 600)
        self.setWindowIcon(QIcon("ikonka.webp"))
        self.tema_temnaya = False
        self.format = None
        self.init_ui()

    def init_ui(self):
        glav_layout = QVBoxLayout()

        self.tema_box = QCheckBox("🌙 Темная тема")
        self.tema_box.stateChanged.connect(self.perekl_temi)
        glav_layout.addWidget(self.tema_box)

        self.vkladki = QTabWidget()
        self.vkladki.addTab(self.tab_kod(), "В текст → Код")
        self.vkladki.addTab(self.tab_raskod(), "Из кода → Текст")
        glav_layout.addWidget(self.vkladki)

        self.iconka = QLabel(self)
        self.iconka.setPixmap(QPixmap("ikonka.webp").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        self.iconka.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.iconka.setStyleSheet("background: transparent;")
        glav_layout.addWidget(self.iconka)

        self.setLayout(glav_layout)

    def tab_kod(self):
        w = QWidget()
        l = QVBoxLayout()

        l_format = QHBoxLayout()

        self.btn_bin = QPushButton()
        self.btn_bin.setIcon(QIcon("ikonka.webp"))
        self.btn_bin.setText("Binary")
        self.btn_bin.clicked.connect(self.set_bin)

        self.btn_ascii = QPushButton()
        self.btn_ascii.setIcon(QIcon("ikonka.webp"))
        self.btn_ascii.setText("ASCII")
        self.btn_ascii.clicked.connect(self.set_ascii)

        self.btn_hex = QPushButton()
        self.btn_hex.setIcon(QIcon("ikonka.webp"))
        self.btn_hex.setText("HEX")
        self.btn_hex.clicked.connect(self.set_hex)

        l_format.addWidget(self.btn_bin)
        l_format.addWidget(self.btn_ascii)
        l_format.addWidget(self.btn_hex)

        l.addLayout(l_format)

        self.vvod_kod = QTextEdit()
        self.vvod_kod.setPlaceholderText("Text here / текст")
        self.vvod_kod.setFont(QFont("Consolas", 16))
        self.vvod_kod.setStyleSheet("background: transparent; color: white; border: 1px solid #555; padding: 5px;")
        l.addWidget(self.vvod_kod)

        self.btn_kod = QPushButton("Translate / Перевод")
        self.btn_kod.setFixedHeight(50)
        self.btn_kod.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.btn_kod.clicked.connect(self.kodirovat)
        l.addWidget(self.btn_kod)

        self.rez_kod = QTextEdit()
        self.rez_kod.setReadOnly(True)
        self.rez_kod.setStyleSheet("background: transparent; color: white; border: 1px solid #555; padding: 5px;")
        l.addWidget(self.rez_kod)

        self.info_kod = QLabel()
        self.info_kod.setWordWrap(True)
        self.info_kod.setStyleSheet("color: gray; padding: 5px;")
        l.addWidget(self.info_kod)

        w.setLayout(l)
        return w

    def tab_raskod(self):
        w = QWidget()
        l = QVBoxLayout()

        self.vvod_raskod = QTextEdit()
        self.vvod_raskod.setPlaceholderText("Text here / Текст")
        self.vvod_raskod.setFont(QFont("Consolas", 12))
        self.vvod_raskod.setStyleSheet("background: transparent; color: white; border: 1px solid #555; padding: 5px;")
        l.addWidget(self.vvod_raskod)

        self.btn_raskod = QPushButton("Decode / Раскодировать")
        self.btn_raskod.setFixedHeight(50)
        self.btn_raskod.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.btn_raskod.clicked.connect(self.raskodirovat)
        l.addWidget(self.btn_raskod)

        self.rez_raskod = QTextEdit()
        self.rez_raskod.setReadOnly(True)
        self.rez_raskod.setStyleSheet("background: transparent; color: white; border: 1px solid #555; padding: 5px;")
        l.addWidget(self.rez_raskod)

        w.setLayout(l)
        return w

    def kodirovat(self):
        if self.format is None:
            self.rez_kod.setText("⚠ Set encode style(Binary/ASCII/HEX) or Type")
            return

        txt = self.vvod_kod.toPlainText()
        rez = ""
        inf = ""

        for ch in txt:
            if self.format == "Binary":
                rez += format(ord(ch), '08b') + " "
            elif self.format == "ASCII":
                rez += str(ord(ch)) + " "
            elif self.format == "HEX":
                rez += hex(ord(ch))[2:].upper() + " "

        self.rez_kod.setText(rez.strip())

        if txt and ord(txt[0]) > 127 and self.format in ["ASCII", "HEX"]:
            ch = txt[0]
            code = ord(ch)
            if self.format == "ASCII":
                inf = f"'{ch}' не входит в стандарт ASCII.\nWindows-1251: {code}, UTF-8: {ch.encode('utf-8').hex().upper()}"
            elif self.format == "HEX":
                hexval = hex(code)[2:].upper()
                utf8 = ' '.join([f"0x{b:02X}" for b in ch.encode('utf-8')])
                inf = f"'{ch}': HEX = {hexval}, Unicode = {code}\nWindows-1251 = {code}, UTF-8 = {utf8}"

        self.info_kod.setText(f"Доп. информация:\n{inf}" if inf else "")

    def raskodirovat(self):
        if self.format is None:
            self.rez_raskod.setText("⚠ Set encode style(Binary/ASCII/HEX) or Type")
            return

        txt = self.vvod_raskod.toPlainText().strip()
        try:
            rez = ""
            for p in txt.split():
                if self.format == "Binary":
                    rez += chr(int(p, 2))
                elif self.format == "ASCII":
                    rez += chr(int(p))
                elif self.format == "HEX":
                    rez += chr(int(p, 16))
            self.rez_raskod.setText(rez)
        except:
            self.rez_raskod.setText("⚠ ERROR You need to type ASCII/HEX/Binary")

    def set_bin(self):
        self.format = "Binary"
        self.update_btns()

    def set_ascii(self):
        self.format = "ASCII"
        self.update_btns()

    def set_hex(self):
        self.format = "HEX"
        self.update_btns()

    def update_btns(self):
        self.btn_bin.setStyleSheet("background-color: none;")
        self.btn_ascii.setStyleSheet("background-color: none;")
        self.btn_hex.setStyleSheet("background-color: none;")

        if self.format == "Binary":
            self.btn_bin.setStyleSheet("background-color: #007BFF; color: white;")
        elif self.format == "ASCII":
            self.btn_ascii.setStyleSheet("background-color: #007BFF; color: white;")
        elif self.format == "HEX":
            self.btn_hex.setStyleSheet("background-color: #007BFF; color: white;")

    def perekl_temi(self):
        if self.tema_box.isChecked():
            self.setStyleSheet("background-color: #1e1e1e; color: white;")
            self.tema_temnaya = True
        else:
            self.setStyleSheet("")
            self.tema_temnaya = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = PerevodApp()
    okno.show()
    sys.exit(app.exec())
