# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loadFilesButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadFilesButton.setObjectName("loadFilesButton")
        self.horizontalLayout.addWidget(self.loadFilesButton)
        self.encryptFilesButton = QtWidgets.QPushButton(self.centralwidget)
        self.encryptFilesButton.setObjectName("encryptFilesButton")
        self.horizontalLayout.addWidget(self.encryptFilesButton)
        self.decryptFilesButton = QtWidgets.QPushButton(self.centralwidget)
        self.decryptFilesButton.setObjectName("decryptFilesButton")
        self.horizontalLayout.addWidget(self.decryptFilesButton)
        self.regenKeysButton = QtWidgets.QPushButton(self.centralwidget)
        self.regenKeysButton.setObjectName("regenKeysButton")
        self.horizontalLayout.addWidget(self.regenKeysButton)
        self.saveKeysButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveKeysButton.setObjectName("saveKeysButton")
        self.horizontalLayout.addWidget(self.saveKeysButton)
        self.loadKeysButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadKeysButton.setObjectName("loadKeysButton")
        self.horizontalLayout.addWidget(self.loadKeysButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.logTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.logTextBrowser.setObjectName("logTextBrowser")
        self.verticalLayout.addWidget(self.logTextBrowser)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.loadFilesButton.setText(_translate("MainWindow", "Загрузить файлы"))
        self.encryptFilesButton.setText(_translate("MainWindow", "Зашифровать файлы"))
        self.decryptFilesButton.setText(_translate("MainWindow", "Расшифровать файлы"))
        self.regenKeysButton.setText(_translate("MainWindow", "Пересоздать ключи"))
        self.saveKeysButton.setText(_translate("MainWindow", "Сохранить ключи"))
        self.loadKeysButton.setText(_translate("MainWindow", "Загрузить ключи"))
