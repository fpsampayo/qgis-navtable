# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_navtable.ui'
#
# Created: Tue Apr 01 14:22:31 2014
#      by: PyQt4 UI code generator 4.10.2
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
        Navtable.resize(400, 550)
        Navtable.setMinimumSize(QtCore.QSize(400, 550))
        Navtable.setMaximumSize(QtCore.QSize(400, 550))
        self.panCB = QtGui.QCheckBox(Navtable)
        self.panCB.setGeometry(QtCore.QRect(40, 10, 61, 22))
        self.panCB.setObjectName(_fromUtf8("panCB"))
        self.zoomCB = QtGui.QCheckBox(Navtable)
        self.zoomCB.setGeometry(QtCore.QRect(300, 10, 81, 22))
        self.zoomCB.setObjectName(_fromUtf8("zoomCB"))
        self.lastBT = QtGui.QPushButton(Navtable)
        self.lastBT.setGeometry(QtCore.QRect(325, 470, 30, 27))
        self.lastBT.setObjectName(_fromUtf8("lastBT"))
        self.nextBT = QtGui.QPushButton(Navtable)
        self.nextBT.setEnabled(True)
        self.nextBT.setGeometry(QtCore.QRect(275, 470, 30, 27))
        self.nextBT.setCheckable(False)
        self.nextBT.setObjectName(_fromUtf8("nextBT"))
        self.previousBT = QtGui.QPushButton(Navtable)
        self.previousBT.setGeometry(QtCore.QRect(95, 470, 30, 27))
        self.previousBT.setObjectName(_fromUtf8("previousBT"))
        self.firstBT = QtGui.QPushButton(Navtable)
        self.firstBT.setGeometry(QtCore.QRect(45, 470, 30, 27))
        self.firstBT.setObjectName(_fromUtf8("firstBT"))
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
        self.pushButton.setGeometry(QtCore.QRect(275, 510, 100, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(Navtable)
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 510, 100, 27))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(Navtable)
        self.pushButton_3.setEnabled(False)
        self.pushButton_3.setGeometry(QtCore.QRect(25, 510, 100, 27))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayoutWidget = QtGui.QWidget(Navtable)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(160, 470, 81, 31))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.nFeatLB = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.nFeatLB.setFont(font)
        self.nFeatLB.setObjectName(_fromUtf8("nFeatLB"))
        self.gridLayout.addWidget(self.nFeatLB, 0, 2, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.currentFeatLB = QtGui.QLineEdit(self.gridLayoutWidget)
        self.currentFeatLB.setObjectName(_fromUtf8("currentFeatLB"))
        self.gridLayout.addWidget(self.currentFeatLB, 0, 0, 1, 1)
        self.attrsTable = QtGui.QTableWidget(Navtable)
        self.attrsTable.setGeometry(QtCore.QRect(10, 40, 381, 421))
        self.attrsTable.setAlternatingRowColors(True)
        self.attrsTable.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.attrsTable.setObjectName(_fromUtf8("attrsTable"))
        self.attrsTable.setColumnCount(2)
        self.attrsTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.attrsTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.attrsTable.setHorizontalHeaderItem(1, item)
        self.attrsTable.horizontalHeader().setVisible(True)
        self.attrsTable.horizontalHeader().setCascadingSectionResizes(False)
        self.attrsTable.horizontalHeader().setSortIndicatorShown(True)
        self.attrsTable.horizontalHeader().setStretchLastSection(True)
        self.attrsTable.verticalHeader().setStretchLastSection(False)

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
        self.onlySelectedCB.setText(_translate("Navtable", "Only Selected", None))
        self.selectCB.setText(_translate("Navtable", "Select", None))
        self.pushButton.setText(_translate("Navtable", "Save", None))
        self.pushButton_2.setText(_translate("Navtable", "Copy Previous", None))
        self.pushButton_3.setText(_translate("Navtable", "Delete", None))
        self.nFeatLB.setText(_translate("Navtable", "0", None))
        self.label.setText(_translate("Navtable", "/", None))
        self.attrsTable.setSortingEnabled(False)
        item = self.attrsTable.horizontalHeaderItem(0)
        item.setText(_translate("Navtable", "campo", None))
        item = self.attrsTable.horizontalHeaderItem(1)
        item.setText(_translate("Navtable", "valor", None))

