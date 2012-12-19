# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/matchsubs.ui'
#
# Created: Thu Nov 29 12:05:57 2012
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

try:
    from PyQt4 import QtCore,QtGui
except ImportError as error:
    from PySide import QtCore,QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.dirlineedit = QtGui.QLineEdit(self.centralwidget)
        self.dirlineedit.setMinimumSize(QtCore.QSize(100, 10))
        self.dirlineedit.setReadOnly(True)
        self.dirlineedit.setObjectName("dirlineedit")
        self.horizontalLayout.addWidget(self.dirlineedit)
        self.dirselbutton = QtGui.QPushButton(self.centralwidget)
        self.dirselbutton.setObjectName("dirselbutton")
        self.horizontalLayout.addWidget(self.dirselbutton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setMinimumSize(QtCore.QSize(200, 400))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 986, 620))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.selectallbutton = QtGui.QPushButton(self.centralwidget)
        self.selectallbutton.setObjectName("selectallbutton")
        self.horizontalLayout_2.addWidget(self.selectallbutton)
        self.deselectallbutton = QtGui.QPushButton(self.centralwidget)
        self.deselectallbutton.setObjectName("deselectallbutton")
        self.horizontalLayout_2.addWidget(self.deselectallbutton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.refreshbutton = QtGui.QPushButton(self.centralwidget)
        self.refreshbutton.setObjectName("refreshbutton")
        self.horizontalLayout_2.addWidget(self.refreshbutton)
        self.gobutton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gobutton.sizePolicy().hasHeightForWidth())
        self.gobutton.setSizePolicy(sizePolicy)
        self.gobutton.setMinimumSize(QtCore.QSize(82, 0))
        self.gobutton.setObjectName("gobutton")
        self.horizontalLayout_2.addWidget(self.gobutton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Match Subtitles", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Select the directory", None, QtGui.QApplication.UnicodeUTF8))
        self.dirselbutton.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.selectallbutton.setText(QtGui.QApplication.translate("MainWindow", "Select All", None, QtGui.QApplication.UnicodeUTF8))
        self.deselectallbutton.setText(QtGui.QApplication.translate("MainWindow", "Deselect All", None, QtGui.QApplication.UnicodeUTF8))
        self.refreshbutton.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.gobutton.setText(QtGui.QApplication.translate("MainWindow", "Go!", None, QtGui.QApplication.UnicodeUTF8))

