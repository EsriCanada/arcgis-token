import sys
import json
import urllib
import time
import ctypes

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ArcGIS(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        layout = QVBoxLayout()

        self.clipboard = QApplication.clipboard()

        # Variables
        self.main_title = "ArcGIS Online Token Generator"
        self.url = "https://www.arcgis.com/sharing/rest"
        self.submitUrl = self.url + "/generateToken"
        self.expirations = ['60', '120', '180', 'max']

        # Design widgets
        self.title_lbl = QLabel(self.main_title)
        self.username_txt = QLineEdit()
        self.password_txt = QLineEdit()
        self.expiration_combo = QComboBox()
        self.clipboard_chk = QCheckBox("Copy token to clipboard ?")
        self.get_token_btn = QPushButton("Get Token")
        self.message_lbl = QLabel()
        self.sub_message_lbl = QLabel()
        self.expiration_lbl = QLabel()
        self.token_output = QTextEdit()

        # Configure
        self.username_txt.setPlaceholderText("Username")
        self.password_txt.setPlaceholderText("Password")
        self.password_txt.setEchoMode(QLineEdit.Password)
        self.get_token_btn.clicked.connect(self.get_token)
        self.expiration_combo.addItems(self.expirations)

        # Add widgets
        layout.addWidget(self.title_lbl)
        layout.addWidget(self.username_txt)
        layout.addWidget(self.password_txt)
        layout.addWidget(self.expiration_combo)
        layout.addWidget(self.get_token_btn)
        layout.addWidget(self.clipboard_chk)
        layout.addWidget(self.message_lbl)
        layout.addWidget(self.sub_message_lbl)
        layout.addWidget(self.expiration_lbl)
        layout.addWidget(self.token_output)

        # Formatting
        layout.setAlignment(self.title_lbl, Qt.AlignCenter)
        layout.setAlignment(self.username_txt, Qt.AlignCenter)
        layout.setAlignment(self.password_txt, Qt.AlignCenter)
        layout.setAlignment(self.expiration_combo, Qt.AlignCenter)
        layout.setAlignment(self.get_token_btn, Qt.AlignCenter)
        layout.setAlignment(self.clipboard_chk, Qt.AlignCenter)
        layout.setAlignment(self.message_lbl, Qt.AlignCenter)
        layout.setAlignment(self.sub_message_lbl, Qt.AlignCenter)

        self.palette = QPalette()

        self.sub_expiration_message_font = QFont()
        self.sub_expiration_message_font.setPointSize(7)
        self.sub_message_lbl.setFont(self.sub_expiration_message_font)

        self.expiration_font = QFont()
        self.expiration_font.setBold(True)
        self.expiration_lbl.setFont(self.expiration_font)
        layout.setAlignment(self.expiration_lbl, Qt.AlignCenter)

        self.setLayout(layout)
        self.setWindowTitle(self.main_title)
        self.setFocus()


    def get_token(self):
        # The maximum expiration period is 15 days or 21600 minutes
        data = dict(username=self.username_txt.text(),
                    password=self.password_txt.text(),
                    expiration='21600' if self.expiration_combo.currentText() == 'max' else self.expiration_combo.currentText(),
                    client='referer',
                    referer='https://www.arcgis.com',
                    f='json')

        submitResponse = urllib.urlopen(self.submitUrl, urllib.urlencode(data))
        submitJson = json.loads(submitResponse.read())

        if 'error' in submitJson:
            self.palette.setColor(QPalette.Foreground, Qt.red)
            self.message_lbl.setPalette(self.palette)
            self.message_lbl.setText(str(submitJson['error']['details'][0]))
        else:
            if self.clipboard_chk.isChecked():
                self.clipboard.clear()
                self.clipboard.setText(str(submitJson['token']), mode=self.clipboard.Clipboard)
            self.palette.setColor(QPalette.Foreground, Qt.blue)
            self.message_lbl.setPalette(self.palette)
            self.message_lbl.setText("Token Granted")
            self.sub_message_lbl.setText("Your token expires:")
            self.expiration_lbl.setText(time.ctime(int(submitJson["expires"]) / 1000))
            self.token_output.clear()
            self.token_output.insertPlainText(str(submitJson['token']))


app = QApplication(sys.argv)

myappid = u'esricanada.tokengenerator.arcgis.1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

dialog = ArcGIS()
dialog.setFixedSize(200, 325)
dialog.setWindowIcon(QIcon('icon.ico'))
app.setWindowIcon(QIcon('icon.ico'))

dialog.show()
app.exec_()
