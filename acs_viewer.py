import sys

import snap7
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QRunnable, QThreadPool, QObject, pyqtSignal, QEvent
from PyQt5.QtWidgets import QApplication
from snap7.snap7exceptions import Snap7Exception

import machine_config
from QT_Design import main_ACS


class WorkerSignals(QObject):
    Start = pyqtSignal(bool)
    Data = pyqtSignal(dict)
    error = pyqtSignal(str)


class PlcWorker(QRunnable):
    def __init__(self, client, data):
        super(PlcWorker, self).__init__()
        self.client = client
        self.data = data
        self.signals = WorkerSignals()
        self.signals.Start.connect(self.start_exec)
        self.Start = True

    def run(self):
        try:
            self.client.connect(self.data["PLC"][0], int(self.data["PLC"][1]), int(self.data["PLC"][2]))
        except Snap7Exception as e:
            self.signals.error.emit(str(e))

        send = {}
        send["machines"] = {}

        while self.Start and self.client.get_connected():
            DB = self.client.db_get(int(self.data["PLC"][3]))

            for machine in self.data["Machine"].keys():
                data = {}
                name = self.data["Machine"][machine]["Name"]
                Xmin = self.data["Machine"][machine]["Data"][0][0]
                Xmax = self.data["Machine"][machine]["Data"][0][1]
                Ymin = self.data["Machine"][machine]["Data"][1][0]
                Ymax = self.data["Machine"][machine]["Data"][1][1]
                Zmin = self.data["Machine"][machine]["Data"][2][0]
                Zmax = self.data["Machine"][machine]["Data"][2][1]
                color = self.data["Machine"][machine]["Color"]
                visible = self.data["Machine"][machine]["Visible"]

                dataS7 = [snap7.util.get_real(DB, int(X)) for X in [Xmin, Xmax, Ymin, Ymax, Zmin, Zmax] if X.isdigit()]
                data["data"] = dataS7
                data["color"] = color
                data["Visible"] = visible

                send["machines"][name] = data
            send["origo"] = self.data["Origo"]

            self.signals.Data.emit(send)
        self.client.disconnect()

    def start_exec(self, start):
        self.Start = start


class ACSviewer(QtWidgets.QMainWindow, main_ACS.Ui_MainWindow):

    def __init__(self, parent=None):
        super(ACSviewer, self).__init__(parent)
        self.setupUi(self)
        self.worker = None
        self.data = None
        self.clientConnected = False

        self.machConf_Dialog = machine_config.MachineConfig(self)
        self.actionACS.triggered.connect(lambda: self.machConf_Dialog.show())


        self.threadpool = QThreadPool()

        self.ip = self.machConf_Dialog.model._data["PLC"][0]
        self.rack = self.machConf_Dialog.model._data["PLC"][1]
        self.slot = self.machConf_Dialog.model._data["PLC"][2]
        self.DB = self.machConf_Dialog.model._data["PLC"][3]
        self.client = snap7.client.Client()
        self.listView_2.setModel(self.machConf_Dialog.model)
        self.run = QtWidgets.QPushButton("Run")
        self.run.setIcon(QtGui.QIcon("QT_Design/play-16.png"))
        self.run.setCheckable(True)
        self.run.clicked.connect(self.startcollector)
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.toolBar.addWidget(spacer)
        self.toolBar.addWidget(self.run)

        # Add Actions to right click menu bar
        self.actionHide.triggered.connect(lambda: self.hidei("Hide"))
        self.actionUnhide.triggered.connect(lambda: self.hidei("UnHide"))
        self.actionDetails_2.triggered.connect(self.Machdetails)

        self.listView_2.addAction(self.actionHide)
        self.listView_2.addAction(self.actionUnhide)
        self.listView_2.addAction(self.actionDetails_2)

    def hidei(self, cmd):
        indexes = self.listView_2.selectedIndexes()
        keys = [x for x in self.machConf_Dialog.model._data["Machine"].keys()]
        for index in indexes:
            Visible = self.machConf_Dialog.model._data["Machine"][keys[index.row()]]["Visible"]
            if cmd == "Hide":
                self.machConf_Dialog.model._data["Machine"][keys[index.row()]]["Visible"] = "False"
            elif cmd == "UnHide":
                self.machConf_Dialog.model._data["Machine"][keys[index.row()]]["Visible"] = "True"

    def Machdetails(self):
        indexes = self.listView_2.selectedIndexes()
        if indexes is None: return False
        if len(indexes) > 1:
            self.setDetailedText("Select only one machine to view details from")
        else:
            if self.data is None:
                self.setDetailedText("No data to show, pleace start viewer")
            else:
                keys = [x for x in self.machConf_Dialog.model._data["Machine"].keys()]
                Name = self.data["Machine"][keys[indexes[0].row()]]["Name"]
                Xmin = self.data["Machine"][keys[indexes[0].row()]]["Data"][0][0]
                Xmax = self.data["Machine"][keys[indexes[0].row()]]["Data"][0][1]
                Ymin = self.data["Machine"][keys[indexes[0].row()]]["Data"][1][0]
                Ymax = self.data["Machine"][keys[indexes[0].row()]]["Data"][1][1]
                Zmin = self.data["Machine"][keys[indexes[0].row()]]["Data"][2][0]
                Zmax = self.data["Machine"][keys[indexes[0].row()]]["Data"][2][1]

                self.setDetailedText(f"--------------- \n"
                                     f"{Name} \n"
                                     f"Xmin: {Xmin}, Xmax: {Xmax} \n"
                                     f"Ymin: {Ymin}, Ymax: {Ymax} \n"
                                     f"Zmin: {Zmin}, Zmax: {Zmax} \n"
                                     f"--------------- \n")




    def eventFilter(self, watched, event):
        if self.machConf_Dialog.isActiveWindow():
            return super().eventFilter(watched, event)
        if event.type() == QEvent.KeyPress:
            self.openGLWidget.event(event)
            return True
        elif event.type() == QEvent.KeyRelease:
            self.openGLWidget.event(event)
            return True
        return super().eventFilter(watched, event)

    def startcollector(self, cheched):
        if cheched:
            self.worker = PlcWorker(self.client, self.machConf_Dialog.model._data)
            self.worker.signals.Data.connect(self.collector)
            self.worker.signals.error.connect(self.setDetailedText)
            self.clientConnected = True
            self.threadpool.start(self.worker)

        else:
            self.clientConnected = False
            self.worker.signals.Start.emit(False)

    def collector(self, data):
        self.data = data
        self.openGLWidget.Data = data
        self.worker._data = self.machConf_Dialog.model._data

    def setDetailedText(self, text):
        self.textBrowser.append(text)


def main():
    app = QApplication(sys.argv)
    form = ACSviewer()
    app.installEventFilter(form)
    form.show()
    sys.exit(app.exec_())
    # app.exec_()


if __name__ == '__main__':
    main()
