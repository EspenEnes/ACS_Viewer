import json
import sys

import snap7
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QColorDialog

from QT_Design import machine_config


class Model(QtCore.QAbstractTableModel):
    def __init__(self, channel=None):
        super(Model, self).__init__()
        self._data = channel or {"Machine": {"0": {"Name": "New", "Data": [["1", "4"], ["2", "5"], ["3", "6"]]}}}

    def data(self, index, role):
        if role == Qt.DisplayRole:
            keys = [x for x in self._data["Machine"].keys()]
            value = self._data["Machine"][keys[index.row()]]["Name"]
            return value

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            if value:
                keys = [x for x in self._data["Machine"].keys()]
                self._data["Machine"][keys[index.row()]]["Name"] = value
            return True

    def rowCount(self, parent):
        return len(self._data["Machine"])

    def columnCount(self, parent):
        return 1

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable


class Model2(QtCore.QAbstractTableModel):
    def __init__(self, channel=None):
        super(Model2, self).__init__()
        self._data = channel or [""]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row()]
            return value

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return 1


class MachineConfig(QtWidgets.QMainWindow, machine_config.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MachineConfig, self).__init__(parent)
        self.setupUi(self)
        self.model = Model()
        self.model2 = Model2()
        self.load()
        self.populatePLC()

        self.listView.setModel(self.model)
        self.listView_2.setModel(self.model2)
        self.selectionModel = self.listView.selectionModel()

        self.pushButton_Add.clicked.connect(self.add)
        self.pushButton.clicked.connect(self.save)
        self.pushButton_Delete.clicked.connect(self.delete)
        self.selectionModel.currentChanged.connect(self.populate)
        self.pushButton_Snapshot.clicked.connect(self.snapshot)
        self.pushButton_Color.clicked.connect(self.openColorDialog)

    def openColorDialog(self):
        indexes = self.listView.selectedIndexes()
        if indexes:
            color = QColorDialog.getColor()
            if color.isValid():
                self.pushButton_Color.setStyleSheet(f"background-color: {str(color.name())}")

    def populate(self, index):
        keys = [x for x in self.model._data["Machine"].keys()]
        xmin = self.model._data["Machine"][keys[index.row()]]["Data"][0][0]
        xmax = self.model._data["Machine"][keys[index.row()]]["Data"][0][1]
        ymin, ymax = self.model._data["Machine"][keys[index.row()]]["Data"][1]
        zmin, zmax = self.model._data["Machine"][keys[index.row()]]["Data"][2]
        color = self.model._data["Machine"][keys[index.row()]]["Color"]



        self.lineEdit_X_Min.setText(xmin)
        self.lineEdit_XMax.setText(xmax)
        self.lineEdit_Y_Min.setText(ymin)
        self.lineEdit_YMax.setText(ymax)
        self.lineEdit_ZMin.setText(zmin)
        self.lineEdit_ZMax.setText(zmax)





        self.pushButton_Color.setStyleSheet(f"background-color: {color}")



    def snapshot(self):
        try:
            DB = self.DB.text()
            Xmin = self.lineEdit_X_Min.text()
            Xmax = self.lineEdit_XMax.text()
            ymin = self.lineEdit_Y_Min.text()
            ymax = self.lineEdit_YMax.text()
            zmin = self.lineEdit_ZMin.text()
            zmax = self.lineEdit_ZMax.text()
            ip = self.lineEdit_IP.text()
            rack = self.lineEdit_Rack.text()
            slot = self.lineEdit_Slot.text()



            if self.parent().clientConnected:
                data = self.self.parent().client.db_get(int(DB))
                self.model2._data = [snap7.util.get_real(data, int(X)) for X in [Xmin, Xmax, ymin, ymax, zmin, zmax] if X.isdigit()]
                self.model2.layoutChanged.emit()
            else:
                self.parent().client.connect(ip, int(rack), int(slot))
                data = self.parent().client.db_get(int(DB))
                self.model2._data = [snap7.util.get_real(data, int(X)) for X in [Xmin, Xmax, ymin, ymax, zmin, zmax]]
                self.parent().client.disconnect()
                self.model2.layoutChanged.emit()
        except:
            self.model2._data = ["Not able to catc PLC data"]
            self.model2.layoutChanged.emit()

    def populatePLC(self):
        self.lineEdit_IP.setText(self.model._data["PLC"][0])
        self.lineEdit_Rack.setText(self.model._data["PLC"][1])
        self.lineEdit_Slot.setText(self.model._data["PLC"][2])
        self.DB.setText(self.model._data["PLC"][3])

        origo_x = self.model._data["Origo"][0][0]
        origo_y = self.model._data["Origo"][1][0]
        origo_z = self.model._data["Origo"][2][0]

        chk_x = self.model._data["Origo"][0][1]
        chk_y = self.model._data["Origo"][1][1]
        chk_z = self.model._data["Origo"][2][1]

        self.lineEdit_OrigoX.setText(origo_x)
        self._OrigoY.setText(origo_y)
        self.lineEdit_ZMax.setText(origo_z)

        if chk_x:
            self.checkBox_X.setChecked(True)
        elif chk_y:
            self.checkBox_Y.setChecked(True)
        elif chk_z:
            self.checkBox_Z.setChecked(True)


    def add(self):
        if len(self.model._data["Machine"]) > 0:
            key = max([int(x) for x in self.model._data["Machine"].keys()])
            self.model._data["Machine"][str(key + 1)] = {"Name": "New", "Data": [["", ""], ["", ""], ["", ""]]}
        else:
            self.model._data["Machine"]["0"] = {"Name": "New", "Data": [["", ""], ["", ""], ["", ""]]}
        self.model.layoutChanged.emit()

    def save(self):
        indexes = self.listView.selectedIndexes()
        for index in indexes:
            Xmin = self.lineEdit_X_Min.text()
            Xmax = self.lineEdit_XMax.text()
            ymin = self.lineEdit_Y_Min.text()
            ymax = self.lineEdit_YMax.text()
            zmin = self.lineEdit_ZMin.text()
            zmax = self.lineEdit_ZMax.text()
            color = self.pushButton_Color.palette().button().color().name()


            self.model._data["Machine"][str(index.row())]["Data"] = [[Xmin, Xmax], [ymin, ymax], [zmin, zmax]]
            self.model._data["Machine"][str(index.row())]["Color"] = color

        ip = self.lineEdit_IP.text()
        rack = self.lineEdit_Rack.text()
        slot = self.lineEdit_Slot.text()
        db = self.DB.text()
        self.model._data["PLC"] = [ip, rack, slot, db]

        x = self.lineEdit_OrigoX.text()
        y = self._OrigoY.text()
        z = self.lineEdit_OrigoZ.text()
        x_chk = self.checkBox_X.isChecked()
        y_chk = self.checkBox_Y.isChecked()
        z_chk = self.checkBox_Z.isChecked()

        self.model._data["Origo"] = [[x,x_chk], [y,y_chk], [z,z_chk]]

        with open("Setup.json", "w") as f:
            data = json.dump(self.model._data, f)

    def load(self):
        try:
            with open("Setup.json", "r") as f:
                self.model._data = json.load(f)
        except:
            pass

    def delete(self):
        keys = [x for x in self.model._data["Machine"].keys()]
        if len(keys) > 0:
            indexes = self.listView.selectedIndexes()
            index = indexes[0]
            row = index.row()
            del self.model._data["Machine"][keys[row]]
            self.model.layoutChanged.emit()
            self.listView.clearSelection()
            self.save()


def main():
    app = QApplication(sys.argv)
    form = MachineConfig()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
