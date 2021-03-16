# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ACS.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(873, 690)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.openGLWidget = MyOPENGL(self.centralwidget)
        self.openGLWidget.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.openGLWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.openGLWidget.setObjectName("openGLWidget")
        self.gridLayout.addWidget(self.openGLWidget, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 873, 21))
        self.menubar.setObjectName("menubar")
        self.menu_Config = QtWidgets.QMenu(self.menubar)
        self.menu_Config.setObjectName("menu_Config")
        self.menuShow = QtWidgets.QMenu(self.menubar)
        self.menuShow.setObjectName("menuShow")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = CostumStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_2 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listView_2 = QtWidgets.QListView(self.dockWidgetContents_2)
        self.listView_2.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.listView_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listView_2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listView_2.setObjectName("listView_2")
        self.verticalLayout_2.addWidget(self.listView_2)
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_2)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setMaximumSize(QtCore.QSize(524287, 111))
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.dockWidgetContents)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget)
        self.actionACS = QtWidgets.QAction(MainWindow)
        self.actionACS.setObjectName("actionACS")
        self.actionEnviorment = QtWidgets.QAction(MainWindow)
        self.actionEnviorment.setObjectName("actionEnviorment")
        self.actionMacines = QtWidgets.QAction(MainWindow)
        self.actionMacines.setObjectName("actionMacines")
        self.actionDetails = QtWidgets.QAction(MainWindow)
        self.actionDetails.setObjectName("actionDetails")
        self.actionHide = QtWidgets.QAction(MainWindow)
        self.actionHide.setObjectName("actionHide")
        self.actionUnhide = QtWidgets.QAction(MainWindow)
        self.actionUnhide.setObjectName("actionUnhide")
        self.actionDetails_2 = QtWidgets.QAction(MainWindow)
        self.actionDetails_2.setObjectName("actionDetails_2")
        self.actionCompare = QtWidgets.QAction(MainWindow)
        self.actionCompare.setObjectName("actionCompare")
        self.menu_Config.addAction(self.actionACS)
        self.menu_Config.addAction(self.actionEnviorment)
        self.menuShow.addAction(self.actionMacines)
        self.menuShow.addAction(self.actionDetails)
        self.menubar.addAction(self.menu_Config.menuAction())
        self.menubar.addAction(self.menuShow.menuAction())

        self.retranslateUi(MainWindow)
        self.actionMacines.triggered.connect(self.dockWidget_2.show)
        self.actionDetails.triggered.connect(self.dockWidget.show)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu_Config.setTitle(_translate("MainWindow", "&Config"))
        self.menuShow.setTitle(_translate("MainWindow", "Show"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionACS.setText(_translate("MainWindow", "Config"))
        self.actionEnviorment.setText(_translate("MainWindow", "Overview"))
        self.actionMacines.setText(_translate("MainWindow", "Macines"))
        self.actionDetails.setText(_translate("MainWindow", "Details"))
        self.actionHide.setText(_translate("MainWindow", "Hide"))
        self.actionUnhide.setText(_translate("MainWindow", "Unhide"))
        self.actionDetails_2.setText(_translate("MainWindow", "Details"))
        self.actionCompare.setText(_translate("MainWindow", "Compare"))
from costumstatusbar import CostumStatusBar
from myopengl import MyOPENGL
