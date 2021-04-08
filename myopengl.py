
from math import cos, sin, radians
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
from PyQt5 import QtWidgets, QtCore

from PyQt5.QtGui import QMouseEvent, QWheelEvent


class MyOPENGL(QtWidgets.QOpenGLWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.up_down_angle = 20.0
        self.diff = QtCore.QPoint(0, 0)
        self.left_right_angle = 0.0

        timer = QtCore.QTimer(self)
        timer.setInterval(20)  # period, in milliseconds
        timer.timeout.connect(self.update)
        timer.start()

        self.cameraPos = [0, 10.0, -10]
        self.cameraFront = [0.0, 10.0, -9]
        self.cameraUp = [0.0, 1.0, 0.0]
        self.left_right_angle = -90.0
        self.test_mode = True

    def initializeGL(self):
        glClearColor(0.85, 0.85, 0.85, 1.0)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        # glEnable(GL_BLEND)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)
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

        self.cameraPos = [int(self.Data["origo"][0][0]), 10.0, -10]


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
            a = np.cross(self.cameraFront, self.cameraUp)
            self.cameraPos[0] += (a[0] * 0.5)
            self.cameraPos[1] += (a[1] * 0.5)
            self.cameraPos[2] += (a[2] * 0.5)
        if self.D:
            a = np.cross(self.cameraFront, self.cameraUp)
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
            if self.Data["machines"][machine]["Visible"] == "False":
                continue

            Xmin = self.Data["machines"][machine]["data"][0]  # / 1000.0
            Xmax = self.Data["machines"][machine]["data"][1]  # / 1000.0
            Ymin = self.Data["machines"][machine]["data"][2]  # / 1000.0
            Ymax = self.Data["machines"][machine]["data"][3]  # / 1000.0
            Zmin = self.Data["machines"][machine]["data"][4]  # / 1000.0
            Zmax = self.Data["machines"][machine]["data"][5]  # / 1000.0
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

        self.grid()

        if self.test_mode:
            self.draw_machine(5, 6, 5,
                              6, 0, 5,
                              (0, 1, 0))
            self.draw_machine(1, 2, 1,
                              2, 0, 5,
                              (0, 0, 1))

            self.draw_machine(10, 11, 10,
                              11, 0, 5,
                              (.15725, .43256, 1))



    def grid(self):
        glDisable(GL_LIGHTING)
        for i in range(1, 20):
            for j in range(1, 20):

                if i % 2 == 0:
                    glColor3f(.5, .5, .5)
                else:
                    glColor3f(0, 0, 0)
                if j % 2 == 0:
                    x = 0 + i
                else:
                    x = 1 + i
                glBegin(GL_POLYGON)
                glVertex3f(-0.5+x, 0.0, -0.5+j)
                glVertex3f(-0.5+x, 0.0, 0.5+j)
                glVertex3f(0.5+x, 0, 0.5+j)
                glVertex3f(0.5+x, 0, -0.5+j)
                glEnd()
        glEnable(GL_LIGHTING)



    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) / 255 for i in range(0, lv, lv // 3))

    def Lines(self, a, b, c, d, vertices,plane):
        if plane == "up": plane = (0,1,0)
        if plane == "down": plane = (0,-1,0)
        if plane == "front": plane = (0,0,-1)
        if plane == "back": plane = (0,0,1)
        if plane == "left": plane = (-1,0,0)
        if plane == "right": plane = (1,0,0)
        # draw a quad
        glBegin(GL_QUADS)
        glNormal3fv(plane)
        glVertex3fv(vertices[a])
        glVertex3fv(vertices[b])
        glVertex3fv(vertices[c])
        glVertex3fv(vertices[d])
        glEnd()

    # def keyPressEvent(self, event):

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key_W:
            self.fwd = False
        if event.key() == QtCore.Qt.Key_Up:
            self.up = False
        if event.key() == QtCore.Qt.Key_S:
            self.bwd = False
        if event.key() == QtCore.Qt.Key_Down:
            self.down = False
        if event.key() == QtCore.Qt.Key_A:
            self.A = False
        if event.key() == QtCore.Qt.Key_Left:
            self.left = False
        if event.key() == QtCore.Qt.Key_D:
            self.D = False
        if event.key() == QtCore.Qt.Key_Right:
            self.right = False

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_W:
            self.fwd = True
        if event.key() == QtCore.Qt.Key_Up:
            self.up = True
        if event.key() == QtCore.Qt.Key_S:
            self.bwd = True
        if event.key() == QtCore.Qt.Key_Down:
            self.down = True
        if event.key() == QtCore.Qt.Key_A:
            self.A = True
        if event.key() == QtCore.Qt.Key_Left:
            self.left = True

        if event.key() == QtCore.Qt.Key_D:
            self.D = True

        if event.key() == QtCore.Qt.Key_Right:
            self.right = True

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == QtCore.Qt.LeftButton:
            self.mpos = event.pos()

            pos = event.pos()
            x = pos.x()
            y = pos.y()
            a = (GLuint * 1)(0)
            glReadPixels(x, y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE, a)
            print(f"{a[0]:2x}")

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
        glColor4f(*color, 0.7)
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

        self.Lines(0, 1, 2, 3, vertices, "back" )
        self.Lines(3, 7, 4, 0, vertices, "left")
        self.Lines(0, 1, 5, 4, vertices, "down")
        self.Lines(4, 7, 6, 5, vertices, "front")
        self.Lines(5, 1, 2, 6, vertices, "right")
        self.Lines(6, 7, 3, 2, vertices, "up")

        glPopMatrix()

