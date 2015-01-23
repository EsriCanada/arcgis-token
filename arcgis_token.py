#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import urllib
import time
import ctypes

import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui


class ArcGIS(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        layout = QtGui.QVBoxLayout()

        self.clipboard = QtGui.QApplication.clipboard()

        # Variables
        self.main_title = "Token Generator"
        self.url = "https://www.arcgis.com/sharing/rest"
        self.submitUrl = self.url + "/generateToken"
        self.expirations = ['60', '120', '180', 'max']

        # Design widgets
        self.title_lbl = QtGui.QLabel(self.main_title)
        self.username_txt = QtGui.QLineEdit()
        self.password_txt = QtGui.QLineEdit()
        self.expiration_combo = QtGui.QComboBox()
        self.clipboard_chk = QtGui.QCheckBox("Copy token to clipboard ?")
        self.get_token_btn = QtGui.QPushButton("Get Token")
        self.message_lbl = QtGui.QLabel()
        self.sub_message_lbl = QtGui.QLabel()
        self.expiration_lbl = QtGui.QLabel()
        self.token_output = QtGui.QTextEdit()

        # Configure
        self.username_txt.setPlaceholderText("Username")
        self.password_txt.setPlaceholderText("Password")
        self.password_txt.setEchoMode(QtGui.QLineEdit.Password)
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
        layout.setAlignment(self.title_lbl, QtCore.Qt.AlignCenter)
        layout.setAlignment(self.username_txt, QtCore.Qt.AlignCenter)
        layout.setAlignment(self.password_txt, QtCore.Qt.AlignCenter)
        layout.setAlignment(self.expiration_combo, QtCore.Qt.AlignCenter)
        layout.setAlignment(self.get_token_btn, QtCore.Qt.AlignCenter)
        layout.setAlignment(self.clipboard_chk, QtCore.Qt.AlignCenter)
        layout.setAlignment(self.message_lbl, QtCore.Qt.AlignCenter)
        layout.setAlignment(self.sub_message_lbl, QtCore.Qt.AlignCenter)

        self.palette = QtGui.QPalette()

        self.sub_expiration_message_font = QtGui.QFont()
        self.sub_expiration_message_font.setPointSize(7)
        self.sub_message_lbl.setFont(self.sub_expiration_message_font)

        self.expiration_font = QtGui.QFont()
        self.expiration_font.setBold(True)
        self.expiration_lbl.setFont(self.expiration_font)
        layout.setAlignment(self.expiration_lbl, QtCore.Qt.AlignCenter)

        self.setLayout(layout)
        self.setWindowTitle(self.main_title)
        self.setFocus()

    def get_token(self):
        # The maximum expiration period is 15 days or 21600 minutes
        expire_select = self.expiration_combo.currentText()
        data = dict(username=self.username_txt.text(),
                    password=self.password_txt.text(),
                    expiration='21600' if expire_select == 'max' else expire_select,
                    client='referer',
                    referer='https://www.arcgis.com',
                    f='json')

        submit_response = urllib.urlopen(self.submitUrl, urllib.urlencode(data))
        submit_json = json.loads(submit_response.read())

        if 'error' in submit_json:
            self.palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)
            self.message_lbl.setPalette(self.palette)
            self.message_lbl.setText(str(submit_json['error']['details'][0]))
        else:
            if self.clipboard_chk.isChecked():
                self.clipboard.clear()
                self.clipboard.setText(str(submit_json['token']), mode=self.clipboard.Clipboard)
            self.palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.blue)
            self.message_lbl.setPalette(self.palette)
            self.message_lbl.setText("Token Granted")
            self.sub_message_lbl.setText("Your token expires:")
            self.expiration_lbl.setText(time.ctime(int(submit_json["expires"]) / 1000))
            self.token_output.clear()
            self.token_output.insertPlainText(str(submit_json['token']))


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    # http://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
    app_id = u'esricanada.tokengenerator.arcgis.0.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    dialog = ArcGIS()
    dialog.setFixedSize(200, 325)
    dialog.setWindowIcon(QtGui.QIcon('images/icon-windowed.ico'))
    app.setWindowIcon(QtGui.QIcon('images/icon-windowed.ico'))

    dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)

    dialog.show()
    sys.exit(app.exec_())
