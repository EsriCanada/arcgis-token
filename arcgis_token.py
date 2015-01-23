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
        layout = QtGui.QGridLayout()

        self.clipboard = QtGui.QApplication.clipboard()

        # Variables
        self.main_title = "Token Generator"
        self.url = "https://www.arcgis.com/sharing/rest"
        self.submitUrl = self.url + "/generateToken"
        self.expirations = ['60', '120', '180', 'max']

        # Design widgets
        self.title_lbl = QtGui.QLabel("ArcGIS Online")
        self.username_txt = QtGui.QLineEdit()
        self.password_txt = QtGui.QLineEdit()
        self.expiration_combo = QtGui.QComboBox()
        self.clipboard_chk = QtGui.QCheckBox("Copy token to clipboard ?")
        self.get_token_btn = QtGui.QPushButton("Get Token")
        self.clear_btn = QtGui.QPushButton("X")
        self.message_lbl = QtGui.QLabel()
        self.sub_message_lbl = QtGui.QLabel()
        self.expiration_lbl = QtGui.QLabel()
        self.token_output = QtGui.QTextEdit()

        # Configure
        self.username_txt.setPlaceholderText("Username")
        self.password_txt.setPlaceholderText("Password")
        self.password_txt.setEchoMode(QtGui.QLineEdit.Password)
        self.get_token_btn.clicked.connect(self.get_token)
        self.clear_btn.clicked.connect(self.clear_form)
        self.expiration_combo.addItems(self.expirations)

        # Add widgets
        layout.addWidget(self.title_lbl, 0, 0, 1, 4)
        layout.addWidget(self.username_txt, 1, 0, 1, 4)
        layout.addWidget(self.password_txt, 2, 0, 1, 4)
        layout.addWidget(self.expiration_combo, 3, 0, 1, 1)
        layout.addWidget(self.get_token_btn, 3, 1, 1, 2)
        layout.addWidget(self.clear_btn, 3, 3, 1, 1)
        layout.addWidget(self.clipboard_chk, 4, 0, 1, 4)
        layout.addWidget(self.message_lbl, 5, 0, 1, 4)
        layout.addWidget(self.sub_message_lbl, 6, 0, 1, 4)
        layout.addWidget(self.expiration_lbl, 7, 0, 1, 4)
        layout.addWidget(self.token_output, 8, 0, 5, 4)

        # Formatting
        layout.setAlignment(self.title_lbl, QtCore.Qt.AlignCenter)
        layout.setAlignment(self.clipboard_chk, QtCore.Qt.AlignCenter)
        layout.setAlignment(self.message_lbl, QtCore.Qt.AlignCenter)
        layout.setAlignment(self.sub_message_lbl, QtCore.Qt.AlignCenter)
        layout.setAlignment(self.token_output, QtCore.Qt.AlignCenter)

        self.palette = QtGui.QPalette()

        self.sub_expiration_message_font = QtGui.QFont()
        self.sub_expiration_message_font.setPointSize(7)
        self.sub_message_lbl.setFont(self.sub_expiration_message_font)

        self.expiration_font = QtGui.QFont()
        self.expiration_font.setBold(True)
        self.expiration_lbl.setFont(self.expiration_font)
        layout.setAlignment(self.expiration_lbl, QtCore.Qt.AlignCenter)

        # Hide output widgets initially
        self.message_lbl.hide()
        self.sub_message_lbl.hide()
        self.expiration_lbl.hide()
        self.token_output.hide()

        self.setLayout(layout)
        self.setWindowTitle(self.main_title)
        self.setFocus()

    def get_token(self):

        # Hide previous messages
        self.message_lbl.hide()
        self.sub_message_lbl.hide()
        self.expiration_lbl.hide()
        self.token_output.hide()

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

            # Show messages
            self.message_lbl.show()

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

            # Show messages
            self.message_lbl.show()
            self.sub_message_lbl.show()
            self.expiration_lbl.show()
            self.token_output.show()

    def clear_form(self):

        # Hide previous messages
        self.message_lbl.hide()
        self.sub_message_lbl.hide()
        self.expiration_lbl.hide()
        self.token_output.hide()

        self.username_txt.clear()
        self.password_txt.clear()
        self.expiration_combo.setCurrentIndex(0)


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    # http://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
    app_id = u'esricanada.tokengenerator.arcgis.0.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    dialog = ArcGIS()
    dialog.setFixedWidth(200)
    dialog.setWindowIcon(QtGui.QIcon('images/icon-windowed.ico'))
    app.setWindowIcon(QtGui.QIcon('images/icon-windowed.ico'))

    dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)

    dialog.show()
    sys.exit(app.exec_())
