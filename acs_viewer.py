import sys
from math import cos, sin, radians

import numpy
import snap7
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QRunnable, QThreadPool, QObject, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QWheelEvent
from PyQt5.QtWidgets import QApplication

import machine_config
from QT_Design import main_ACS


class WorkerSignals(QObject):
    Start = pyqtSignal(bool)
    Data = pyqtSignal(dict)


class PlcWorker(QRunnable):
    def __init__(self, client, data):
        super(PlcWorker, self).__init__()
        self.client = client
        self.data = data
        self.signals = WorkerSignals()
        self.signals.Start.connect(self.start_exec)
        self.Start = True

    def run(self):
        self.client.connect(self.data["PLC"][0], int(self.data["PLC"][1]), int(self.data["PLC"][2]))
        send = {}
        send["machines"] = {}

        while self.Start:
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

                dataS7 = [snap7.util.get_real(DB, int(X)) for X in [Xmin, Xmax, Ymin, Ymax, Zmin, Zmax] if X.isdigit()]
                data["data"] = dataS7
                data["color"] = color

                send["machines"][name] = data
            send["origo"] = self.data["Origo"]

            self.signals.Data.emit(send)
        self.client.disconnect()

    def start_exec(self, start):
        self.Start = start


class ACSviewer(QtWidgets.QMainWindow, main_ACS.Ui_MainWindow):
    keyPressed = QtCore.pyqtSignal(int)
    keyRelese = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super(ACSviewer, self).__init__(parent)
        self.setupUi(self)
        self.worker = None
        self.openGLWidget = MyOPENGL(self)
        self.openGLWidget.setObjectName("openGLWidget")
        self.gridLayout.addWidget(self.openGLWidget, 0, 0, 1, 2)

        self.machConf_Dialog = machine_config.MachineConfig(self)
        self.actionACS.triggered.connect(self.test)
        self.pushButton.setCheckable(True)
        self.pushButton.clicked.connect(self.startcollector)
        self.clientConnected = False
        self.threadpool = QThreadPool()

        self.ip = self.machConf_Dialog.model._data["PLC"][0]
        self.rack = self.machConf_Dialog.model._data["PLC"][1]
        self.slot = self.machConf_Dialog.model._data["PLC"][2]
        self.DB = self.machConf_Dialog.model._data["PLC"][3]
        self.client = snap7.client.Client()
        self.pushButton.setStyleSheet(f"background-color: green")

    def keyPressEvent(self, event):
        self.keyPressed.emit(event.key())

    def keyReleaseEvent(self, event):
        self.keyRelese.emit(event.key())

    def test(self):
        self.machConf_Dialog.show()

    def startcollector(self, cheched):
        if cheched:
            self.worker = PlcWorker(self.client, self.machConf_Dialog.model._data)
            self.worker.signals.Data.connect(self.collector)
            self.clientConnected = True
            self.threadpool.start(self.worker)

        else:
            self.clientConnected = False
            self.worker.signals.Start.emit(False)

    def collector(self, data):
        self.openGLWidget.Data = data
        self.worker._data = self.machConf_Dialog.model._data


class MyOPENGL(QtWidgets.QOpenGLWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.up_down_angle = 0.0
        self.diff = QtCore.QPoint(0, 0)
        self.left_right_angle = 0.0

        timer = QtCore.QTimer(self)
        timer.setInterval(20)  # period, in milliseconds
        timer.timeout.connect(self.update)
        timer.start()

        self.cameraPos = [0.0, 0.0, -10]
        self.cameraFront = [0.0, 0.0, -9]
        self.cameraUp = [0.0, 1.0, 0.0]
        self.left_right_angle = -90.0

        parent.keyPressed.connect(self.keyPressEvent_Parent)
        parent.keyRelese.connect(self.keyReleseEvent_Parent)

    def initializeGL(self):
        glClearColor(0.85, 0.85, 0.85, 1.0)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        self.Data = {}
        self.Data["machines"] = {}
        self.Data["origo"] = [[10, False], [10, False], [0, False]]
        self.fwd = False
        self.up = False
        self.bwd = False
        self.down = False
        self.A = False
        self.left = False
        self.D = False
        self.right = False

    def resizeGL(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(1, 1, width, height)
        gluPerspective(45.0, width / height, 0.1, 200.0)

    def CamereMove(self):

        if self.fwd:
            self.cameraPos[0] -= (self.cameraFront[0] * 0.5)
            self.cameraPos[1] -= (self.cameraFront[1] * 0.5)
            self.cameraPos[2] -= (self.cameraFront[2] * 0.5)
        if self.bwd:
            self.cameraPos[0] += (self.cameraFront[0] * 0.5)
            self.cameraPos[1] += (self.cameraFront[1] * 0.5)
            self.cameraPos[2] += (self.cameraFront[2] * 0.5)
        if self.up: self.diff = QtCore.QPoint(0, -100)
        if self.down: self.diff = QtCore.QPoint(0, +100)
        if self.left: self.diff = QtCore.QPoint(-100, 0)
        if self.A:
            a = numpy.cross(self.cameraFront, self.cameraUp)
            self.cameraPos[0] += (a[0] * 0.5)
            self.cameraPos[1] += (a[1] * 0.5)
            self.cameraPos[2] += (a[2] * 0.5)
        if self.D:
            a = numpy.cross(self.cameraFront, self.cameraUp)
            self.cameraPos[0] -= (a[0] * 0.5)
            self.cameraPos[1] -= (a[1] * 0.5)
            self.cameraPos[2] -= (a[2] * 0.5)
        if self.right:   self.diff = QtCore.QPoint(100, 0)

        self.up_down_angle += self.diff.y() * 0.01
        self.left_right_angle += self.diff.x() * 0.01

        direction = [0, 0, 0]
        direction[0] = cos(radians(self.left_right_angle)) * cos(radians(self.up_down_angle))
        direction[1] = sin(radians(self.up_down_angle))
        direction[2] = sin(radians(self.left_right_angle)) * cos(radians(self.up_down_angle))

        self.cameraFront = (direction[0], direction[1], direction[2])
        self.diff = QtCore.QPoint(0, 0)

        return self.cameraPos + (list(map(lambda i, j: i - j, self.cameraPos, self.cameraFront)) + self.cameraUp)

    def paintGL(self):



        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)


        glLoadIdentity()
        gluLookAt(*self.CamereMove())

        for count, machine in enumerate(self.Data["machines"].keys()):

            Xmin = self.Data["machines"][machine]["data"][0] / 1000.0
            Xmax = self.Data["machines"][machine]["data"][1] / 1000.0
            Ymin = self.Data["machines"][machine]["data"][2] / 1000.0
            Ymax = self.Data["machines"][machine]["data"][3] / 1000.0
            Zmin = self.Data["machines"][machine]["data"][4] / 1000.0
            Zmax = self.Data["machines"][machine]["data"][5] / 1000.0
            color = self.hex_to_rgb(self.Data["machines"][machine]["color"])

            if self.Data["origo"][0][1]:
                Xmin = int(self.Data["origo"][0][0]) - Xmin
                Xmax = int(self.Data["origo"][0][0]) - Xmax
            if self.Data["origo"][1][1]:
                Ymin = int(self.Data["origo"][1][0]) - Ymin
                Ymax = int(self.Data["origo"][1][0]) - Ymax

            self.draw_machine(Xmin, Xmax, Ymin, Ymax, Zmin, Zmax,
                              color)

        xmin = int(self.Data["origo"][0][0]) + (int(self.Data["origo"][0][0]) * -0.001)
        xmax = int(self.Data["origo"][0][0]) + (int(self.Data["origo"][0][0]) * 0.001)
        ymin = int(self.Data["origo"][1][0]) + (int(self.Data["origo"][1][0]) * -0.001)
        ymax = int(self.Data["origo"][1][0]) + (int(self.Data["origo"][1][0]) * 0.001)

        if self.Data["origo"][0][1]:
            xmin = int(self.Data["origo"][0][0]) - xmin
            xmax = int(self.Data["origo"][0][0]) - xmax
        if self.Data["origo"][1][1]:
            ymin = int(self.Data["origo"][1][0]) - ymin
            ymax = int(self.Data["origo"][1][0]) - ymax

        zmin = 0
        zmax = 100

        self.draw_machine(xmin, xmax, ymin,
                          ymax, zmin, zmax,
                          (1, 0, 0))



    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) / 255 for i in range(0, lv, lv // 3))

    def Lines(self, a, b, c, d, vertices):
        # draw a quad
        glBegin(GL_QUADS)
        # glNormal3fv(self.normals[n])
        glVertex3fv(vertices[a])
        glVertex3fv(vertices[b])
        glVertex3fv(vertices[c])
        glVertex3fv(vertices[d])
        glEnd()

    # def keyPressEvent(self, event):

    def keyReleseEvent_Parent(self, key):
        if key == QtCore.Qt.Key_W:
            self.fwd = False
        if key == QtCore.Qt.Key_Up:
            self.up = False
        if key == QtCore.Qt.Key_S:
            self.bwd = False
        if key == QtCore.Qt.Key_Down:
            self.down = False
        if key == QtCore.Qt.Key_A:
            self.A = False
        if key == QtCore.Qt.Key_Left:
            self.left = False
        if key == QtCore.Qt.Key_D:
            self.D = False
        if key == QtCore.Qt.Key_Right:
            self.right = False

    def keyPressEvent_Parent(self, key):
        if key == QtCore.Qt.Key_W:
            self.fwd = True
        if key == QtCore.Qt.Key_Up:
            self.up = True
        if key == QtCore.Qt.Key_S:
            self.bwd = True
        if key == QtCore.Qt.Key_Down:
            self.down = True
        if key == QtCore.Qt.Key_A:
            self.A = True
        if key == QtCore.Qt.Key_Left:
            self.left = True

        if key == QtCore.Qt.Key_D:
            self.D = True

        if key == QtCore.Qt.Key_Right:
            self.right = True

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == QtCore.Qt.LeftButton:
            self.mpos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == QtCore.Qt.LeftButton:
            self.diff = event.pos() - self.mpos

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.angleDelta().y() == 120.0:
            self.cameraPos[0] -= (self.cameraFront[0] * 0.1)
            self.cameraPos[1] -= (self.cameraFront[1] * 0.1)
            self.cameraPos[2] -= (self.cameraFront[2] * 0.1)
        elif event.angleDelta().y() == -120.0:
            self.cameraPos[0] += (self.cameraFront[0] * 0.1)
            self.cameraPos[1] += (self.cameraFront[1] * 0.1)
            self.cameraPos[2] += (self.cameraFront[2] * 0.1)

    def draw_machine(self, Xmin, Xmax, Ymin, Ymax, Zmin, Zmax, color):
        glPushMatrix()
        glColor4f(*color,0.7)
        glTranslatef(0, 0, 0)

        vertices = [
            (Xmin, Zmin, Ymax),
            (Xmax, Zmin, Ymax),
            (Xmax, Zmax, Ymax),
            (Xmin, Zmax, Ymax),
            (Xmin, Zmin, Ymin),
            (Xmax, Zmin, Ymin),
            (Xmax, Zmax, Ymin),
            (Xmin, Zmax, Ymin),
        ]

        self.Lines(0, 1, 2, 3, vertices)
        self.Lines(3, 7, 4, 0, vertices)
        self.Lines(0, 1, 5, 4, vertices)
        self.Lines(4, 7, 6, 5, vertices)
        self.Lines(5, 1, 2, 6, vertices)
        self.Lines(6, 7, 3, 2, vertices)

        glPopMatrix()


def main():
    app = QApplication(sys.argv)
    form = ACSviewer()
    form.show()
    sys.exit(app.exec_())
    # app.exec_()


if __name__ == '__main__':
    main()
