# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Call_Dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_sip_callinfo(object):
    def setupUi(self, sip_callinfo):
        sip_callinfo.setObjectName("Call_Dialog")
        sip_callinfo.resize(320, 120)
        sip_callinfo.setFixedSize(sip_callinfo.width(), sip_callinfo.height());
        self.Call_number = QtWidgets.QLabel(sip_callinfo)
        self.Call_number.setGeometry(QtCore.QRect(140, 20, 54, 12))
        self.Call_number.setObjectName("Call_number")
        self.pushButton_cancel = QtWidgets.QPushButton(sip_callinfo)
        self.pushButton_cancel.setGeometry(QtCore.QRect(170, 60, 75, 23))
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.pushButton_Answer = QtWidgets.QPushButton(sip_callinfo)
        self.pushButton_Answer.setGeometry(QtCore.QRect(70, 60, 75, 23))
        self.pushButton_Answer.setObjectName("pushButton_Answer")

        self.retranslateUi(sip_callinfo)
        self.pushButton_cancel.clicked.connect(sip_callinfo.PushButton_Click)
        self.pushButton_Answer.clicked.connect(sip_callinfo.PushButton_Click)
        QtCore.QMetaObject.connectSlotsByName(sip_callinfo)

    def retranslateUi(self, Call_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Call_Dialog.setWindowTitle(_translate("Call_Dialog", "通话"))
        self.Call_number.setText(_translate("Call_Dialog", "0000"))
        self.pushButton_cancel.setText(_translate("Call_Dialog", "取消"))
        self.pushButton_Answer.setText(_translate("Call_Dialog", "接听"))

