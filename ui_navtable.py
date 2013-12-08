# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_navtable.ui'
#
# Created: Sun Dec  8 17:03:18 2013
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Navtable(object):
    def setupUi(self, Navtable):
        Navtable.setObjectName(_fromUtf8("Navtable"))
        Navtable.resize(406, 502)
        self.panCB = QtGui.QCheckBox(Navtable)
        self.panCB.setGeometry(QtCore.QRect(40, 10, 61, 22))
        self.panCB.setObjectName(_fromUtf8("panCB"))
        self.zoomCB = QtGui.QCheckBox(Navtable)
        self.zoomCB.setGeometry(QtCore.QRect(300, 10, 81, 22))
        self.zoomCB.setObjectName(_fromUtf8("zoomCB"))
        self.table = QtGui.QTextEdit(Navtable)
        self.table.setEnabled(False)
        self.table.setGeometry(QtCore.QRect(40, 40, 341, 331))
        self.table.setReadOnly(True)
        self.table.setObjectName(_fromUtf8("table"))
        self.lastBT = QtGui.QPushButton(Navtable)
        self.lastBT.setGeometry(QtCore.QRect(310, 390, 31, 27))
        self.lastBT.setObjectName(_fromUtf8("lastBT"))
        self.nextBT = QtGui.QPushButton(Navtable)
        self.nextBT.setGeometry(QtCore.QRect(260, 390, 31, 27))
        self.nextBT.setObjectName(_fromUtf8("nextBT"))
        self.previousBT = QtGui.QPushButton(Navtable)
        self.previousBT.setGeometry(QtCore.QRect(110, 390, 31, 27))
        self.previousBT.setObjectName(_fromUtf8("previousBT"))
        self.firstBT = QtGui.QPushButton(Navtable)
        self.firstBT.setGeometry(QtCore.QRect(60, 390, 31, 27))
        self.firstBT.setObjectName(_fromUtf8("firstBT"))
        self.nFeatLB = QtGui.QLabel(Navtable)
        self.nFeatLB.setGeometry(QtCore.QRect(230, 400, 31, 17))
        self.nFeatLB.setObjectName(_fromUtf8("nFeatLB"))
        self.currentFeatLB = QtGui.QLineEdit(Navtable)
        self.currentFeatLB.setGeometry(QtCore.QRect(160, 400, 41, 27))
        self.currentFeatLB.setObjectName(_fromUtf8("currentFeatLB"))
        self.label = QtGui.QLabel(Navtable)
        self.label.setGeometry(QtCore.QRect(210, 400, 16, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.onlySelectedCB = QtGui.QCheckBox(Navtable)
        self.onlySelectedCB.setEnabled(False)
        self.onlySelectedCB.setGeometry(QtCore.QRect(170, 10, 121, 22))
        self.onlySelectedCB.setObjectName(_fromUtf8("onlySelectedCB"))
        self.selectCB = QtGui.QCheckBox(Navtable)
        self.selectCB.setEnabled(True)
        self.selectCB.setGeometry(QtCore.QRect(100, 10, 71, 22))
        self.selectCB.setChecked(False)
        self.selectCB.setObjectName(_fromUtf8("selectCB"))
        self.pushButton = QtGui.QPushButton(Navtable)
        self.pushButton.setEnabled(False)
        self.pushButton.setGeometry(QtCore.QRect(280, 430, 98, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Navtable)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 430, 101, 27))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Navtable)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 430, 98, 27))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))

        self.retranslateUi(Navtable)
        QtCore.QMetaObject.connectSlotsByName(Navtable)

    def retranslateUi(self, Navtable):
        Navtable.setWindowTitle(_translate("Navtable", "Navtable", None))
        self.panCB.setText(_translate("Navtable", "Pan", None))
        self.zoomCB.setText(_translate("Navtable", "Zoom", None))
        self.lastBT.setText(_translate("Navtable", ">>", None))
        self.nextBT.setText(_translate("Navtable", ">", None))
        self.previousBT.setText(_translate("Navtable", "<", None))
        self.firstBT.setText(_translate("Navtable", "<<", None))
        self.nFeatLB.setText(_translate("Navtable", "0", None))
        self.label.setText(_translate("Navtable", "/", None))
        self.onlySelectedCB.setText(_translate("Navtable", "Only Selected", None))
        self.selectCB.setText(_translate("Navtable", "Select", None))
        self.pushButton.setText(_translate("Navtable", "Save", None))
        self.pushButton_2.setText(_translate("Navtable", "Copy Previous", None))
        self.pushButton_3.setText(_translate("Navtable", "Delete", None))

