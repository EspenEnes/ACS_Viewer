# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'machine_config.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(695, 644)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listView = QtWidgets.QListView(self.widget_3)
        self.listView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listView.setObjectName("listView")
        self.verticalLayout.addWidget(self.listView)
        self.pushButton_Add = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_Add.setObjectName("pushButton_Add")
        self.verticalLayout.addWidget(self.pushButton_Add)
        self.pushButton_Delete = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_Delete.setObjectName("pushButton_Delete")
        self.verticalLayout.addWidget(self.pushButton_Delete)
        self.horizontalLayout.addWidget(self.widget_3)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.widget_4 = QtWidgets.QWidget(self.widget)
        self.widget_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widget_4.setObjectName("widget_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_15 = QtWidgets.QLabel(self.widget_4)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 0, 2, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.widget_4)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout_3.addWidget(self.label_16, 0, 3, 1, 1)
        self.lineEdit_OrigoZ = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_OrigoZ.setObjectName("lineEdit_OrigoZ")
        self.gridLayout_3.addWidget(self.lineEdit_OrigoZ, 1, 3, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.widget_4)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 0, 1, 1, 1)
        self.lineEdit_OrigoX = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_OrigoX.setObjectName("lineEdit_OrigoX")
        self.gridLayout_3.addWidget(self.lineEdit_OrigoX, 1, 1, 1, 1)
        self._OrigoY = QtWidgets.QLineEdit(self.widget_4)
        self._OrigoY.setObjectName("_OrigoY")
        self.gridLayout_3.addWidget(self._OrigoY, 1, 2, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.widget_4)
        self.label_13.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 1, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.widget_4)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 2, 0, 1, 1)
        self.checkBox_X = QtWidgets.QCheckBox(self.widget_4)
        self.checkBox_X.setText("")
        self.checkBox_X.setObjectName("checkBox_X")
        self.gridLayout_3.addWidget(self.checkBox_X, 2, 1, 1, 1)
        self.checkBox_Y = QtWidgets.QCheckBox(self.widget_4)
        self.checkBox_Y.setText("")
        self.checkBox_Y.setObjectName("checkBox_Y")
        self.gridLayout_3.addWidget(self.checkBox_Y, 2, 2, 1, 1)
        self.checkBox_Z = QtWidgets.QCheckBox(self.widget_4)
        self.checkBox_Z.setText("")
        self.checkBox_Z.setObjectName("checkBox_Z")
        self.gridLayout_3.addWidget(self.checkBox_Z, 2, 3, 1, 1)
        self.gridLayout.addWidget(self.widget_4, 1, 0, 1, 5)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 6, 3, 1, 1)
        self.lineEdit_XMax = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_XMax.setObjectName("lineEdit_XMax")
        self.gridLayout.addWidget(self.lineEdit_XMax, 4, 4, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_IP = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_IP.setObjectName("lineEdit_IP")
        self.gridLayout_2.addWidget(self.lineEdit_IP, 1, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.widget_2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)
        self.DB = QtWidgets.QLineEdit(self.widget_2)
        self.DB.setObjectName("DB")
        self.gridLayout_2.addWidget(self.DB, 4, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.widget_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.widget_2)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 3, 0, 1, 1)
        self.lineEdit_Slot = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_Slot.setObjectName("lineEdit_Slot")
        self.gridLayout_2.addWidget(self.lineEdit_Slot, 3, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.widget_2)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 0, 0, 1, 2)
        self.label_11 = QtWidgets.QLabel(self.widget_2)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 4, 0, 1, 1)
        self.lineEdit_Rack = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_Rack.setObjectName("lineEdit_Rack")
        self.gridLayout_2.addWidget(self.lineEdit_Rack, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.widget_2, 0, 0, 1, 5)
        self.listView_2 = QtWidgets.QListView(self.widget)
        self.listView_2.setObjectName("listView_2")
        self.gridLayout.addWidget(self.listView_2, 10, 0, 1, 5)
        self.pushButton_Color = QtWidgets.QPushButton(self.widget)
        self.pushButton_Color.setObjectName("pushButton_Color")
        self.gridLayout.addWidget(self.pushButton_Color, 3, 4, 1, 1)
        self.pushButton_Snapshot = QtWidgets.QPushButton(self.widget)
        self.pushButton_Snapshot.setObjectName("pushButton_Snapshot")
        self.gridLayout.addWidget(self.pushButton_Snapshot, 9, 0, 1, 5)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_7.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 6, 0, 1, 1)
        self.lineEdit_X_Min = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_X_Min.setObjectName("lineEdit_X_Min")
        self.gridLayout.addWidget(self.lineEdit_X_Min, 4, 1, 1, 1)
        self.lineEdit_ZMin = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_ZMin.setObjectName("lineEdit_ZMin")
        self.gridLayout.addWidget(self.lineEdit_ZMin, 6, 1, 1, 1)
        self.lineEdit_ZMax = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_ZMax.setObjectName("lineEdit_ZMax")
        self.gridLayout.addWidget(self.lineEdit_ZMax, 6, 4, 1, 1)
        self.lineEdit_Y_Min = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_Y_Min.setObjectName("lineEdit_Y_Min")
        self.gridLayout.addWidget(self.lineEdit_Y_Min, 5, 1, 1, 1)
        self.lineEdit_YMax = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_YMax.setObjectName("lineEdit_YMax")
        self.gridLayout.addWidget(self.lineEdit_YMax, 5, 4, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 8, 0, 1, 2)
        self.pushButton_Load = QtWidgets.QPushButton(self.widget)
        self.pushButton_Load.setObjectName("pushButton_Load")
        self.gridLayout.addWidget(self.pushButton_Load, 8, 3, 1, 2)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 3, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 3, 1, 1)
        self.checkBox_Visible = QtWidgets.QCheckBox(self.widget)
        self.checkBox_Visible.setObjectName("checkBox_Visible")
        self.gridLayout.addWidget(self.checkBox_Visible, 3, 3, 1, 1)
        self.horizontalLayout.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 695, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_Add.setText(_translate("MainWindow", "Add New"))
        self.pushButton_Delete.setText(_translate("MainWindow", "Delete"))
        self.label_15.setText(_translate("MainWindow", "Y"))
        self.label_16.setText(_translate("MainWindow", "Z"))
        self.label_14.setText(_translate("MainWindow", "X"))
        self.label_13.setText(_translate("MainWindow", "ORIGO"))
        self.label_17.setText(_translate("MainWindow", "Invert\'"))
        self.label_2.setText(_translate("MainWindow", "Z_Max:"))
        self.label_9.setText(_translate("MainWindow", "Rack:"))
        self.label_8.setText(_translate("MainWindow", "IP"))
        self.label_10.setText(_translate("MainWindow", "Slot:"))
        self.label_12.setText(_translate("MainWindow", "Config:"))
        self.label_11.setText(_translate("MainWindow", "DB:"))
        self.pushButton_Color.setText(_translate("MainWindow", "Color"))
        self.pushButton_Snapshot.setText(_translate("MainWindow", "Snapshot"))
        self.label_5.setText(_translate("MainWindow", "X_Min:"))
        self.label_7.setText(_translate("MainWindow", "Add Machine:"))
        self.label.setText(_translate("MainWindow", "Z_Min:"))
        self.pushButton.setText(_translate("MainWindow", "Save"))
        self.pushButton_Load.setText(_translate("MainWindow", "Load"))
        self.label_3.setText(_translate("MainWindow", "Y_Min:"))
        self.label_4.setText(_translate("MainWindow", "Y_Max:"))
        self.label_6.setText(_translate("MainWindow", "X_Max:"))
        self.checkBox_Visible.setText(_translate("MainWindow", "Visible"))
