__author__ = 'Matjaz'

import sys

from string import Template

from PySide import QtGui, QtCore

import numpy as np

import pyqtgraph as pg

import pyqtgraph.dockarea as da
from pyqtgraph.dockarea.Dock import DockLabel


_COLOR_PALETTE_ORANGE = dict(primary='#d35400', hover='#e67e22')
_COLOR_PALETTE_BW = dict(primary='#333333', hover='#666666')

COLOR_PALETTE = _COLOR_PALETTE_BW


pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


def updateStylePatched(self):
    r = '3px'
    if self.dim:
        fg = 'gray'
        bg = 'none'
        border = 'none'
        # border = '#7cf3ac'
    else:
        fg = '#000000'
        bg = 'none'
        border = 'none'

    if self.orientation == 'vertical':
        self.vStyle = """DockLabel {
            background-color : %s;
            color : %s;
            border-top-right-radius: 0px;
            border-top-left-radius: %s;
            border-bottom-right-radius: 0px;
            border-bottom-left-radius: %s;
            border-width: 0px;
            border-right: 0px solid %s;
            padding-top: 30px;
            padding-bottom: 30px;
            padding-left: 0px;
            padding-right: 0px;
            font-size: 18px;
            font-family: Helvetica [Cronyx];
        }""" % (bg, fg, r, r, border)
        self.setStyleSheet(self.vStyle)
    else:
        self.hStyle = """DockLabel {
            background-color : %s;
            color : %s;
            border-top-right-radius: %s;
            border-top-left-radius: %s;
            border-bottom-right-radius: 0px;
            border-bottom-left-radius: 0px;
            border-width: 0px;
            border-bottom: 0px solid %s;
            padding-left: 0px;
            padding-right: 13px;
            font-size: 18px
        }""" % (bg, fg, r, r, border)
        self.setStyleSheet(self.hStyle)


DockLabel.updateStyle = updateStylePatched

class MaximizeButton(QtGui.QGraphicsPolygonItem):
    def __init__(self):
        polygon = QtGui.QPolygon()
        polygon << QtCore.QPoint(10, 20) << QtCore.QPoint(20, 30) << QtCore.QPoint(40, 50)
        super().__init__(polygon)

class FramelessContainer(QtGui.QMainWindow):

    def __init__(self, desktop_widget):
        super().__init__()

        self.desktop_widget = desktop_widget

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.resize(1280, 1024)
        self.setWindowTitle('Hello')
        self.margins = True
        self.setContentsMargins(50, 50,50, 50)
        # self.setContentsMargins(0, 0,0, 0)
        self.main_app = MainApp()

        # scene = QtGui.QGraphicsScene(self)
        # ellipseItem = MaximizeButton()
        # scene.addItem(ellipseItem)
        #
        # view = QtGui.QGraphicsView(scene)
        # view.move(20, 100)
        # # view.show()

        self.setCentralWidget(self.main_app)

        with open('style_template.css', 'r') as fh:
            src = Template(fh.read())
            src = src.substitute(COLOR_PALETTE)
            # print (src)
            self.setStyleSheet(src)
            # self.setStyleSheet(fh.read())
        # self.setWindowFlags(self.windowFlags() & QtCore.Qt.WindowMinimizeButtonHint)


    def resizeEvent(self, event):
        if self.margins:
            pass
        else:
            self.setContentsMargins(50, 50, 50, 50)
            self.margins = True

    def mouseMoveEvent(self, event):
        if event.buttons() and QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.mouse_drag_position)
            event.accept()

    def mousePressEvent(self, event):
        if self.margins:
            add = 50
        else:
            add = 0

        if event.button() == QtCore.Qt.LeftButton:
            if (event.pos().x() < (self.width() - 10 - add)) and (event.pos().x() > (self.width()-20-add))\
                    and (event.pos().y() < (20+add)) and (event.pos().y() > (10+add)):
                self.close()

            if (event.pos().x() < (self.width() - 25 - add)) and (event.pos().x() > (self.width()-35-add))\
                    and (event.pos().y() < (20+add)) and (event.pos().y() > (10+add)):
                if self.margins:
                    rect = self.desktop_widget.availableGeometry(self)
                    self.setContentsMargins(0, 0, 0, 0)
                    self.setGeometry(rect)
                    self.margins = False
                else:
                    self.resize(1280, 1024)

                # self.showFullScreen()

            if (event.pos().x() < (self.width() - 40 - add)) and (event.pos().x() > (self.width()-50-add))\
                    and (event.pos().y() < (20+add)) and (event.pos().y() > (10+add)):
                # TODO: Window goes to sleep (or sth.) here. FIX!
                self.setWindowState(QtCore.Qt.WindowMinimized)
                self.activateWindow()

            self.mouse_drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()



class MainApp(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.main_window = MainWindow()
        self.setAutoFillBackground(True)
        self.box = QtGui.QHBoxLayout()
        self.box.addWidget(self.main_window)

        self.box.addWidget(QtGui.QSizeGrip(self.parent()), 0, QtCore.Qt.AlignBottom |QtCore.Qt.AlignRight)

        # self.setCentralWidget(self.main_window)
        self.setLayout(self.box)

        self.main_window.setContentsMargins(25, 25, 25, 25)
        self.box.setContentsMargins(0, 0, 0, 0)

        self.shadow = QtGui.QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(50)
        self.setGraphicsEffect(self.shadow)

    def paintEvent(self, event):

        self.painter = QtGui.QPainter()
        self.painter.begin(self)

        self.painter.setBrush(QtCore.Qt.white)
        self.painter.setPen(QtCore.Qt.lightGray)

        # .. Draw a rectangle around the main window.
        self.painter.drawRect(0, 0, self.width()-1, self.height()-1)

        self.painter.drawLine(300, 180, 300, self.height())

        self.painter.drawLine(self.width() - 20, 20, self.width() - 10, 10)
        self.painter.drawLine(self.width() - 20, 10, self.width() - 10, 20)

        self.painter.drawLine(self.width() - 35, 10, self.width() - 25, 10)
        self.painter.drawLine(self.width() - 35, 20, self.width() - 25, 20)
        self.painter.drawLine(self.width() - 35, 10, self.width() - 35, 20)
        self.painter.drawLine(self.width() - 25, 10, self.width() - 25, 20)

        self.painter.drawLine(self.width() - 50, 20, self.width() - 40, 20)


        self.painter.end()


class MainMenu(QtGui.QWidget):
    def __init__(self):
        super().__init__()

        # self.button_go = QtGui.QPushButton('Start')
        # self.button_go = QtGui.QComboBox()

        self.button_go = QtGui.QToolButton()
        self.button_go.setText('START')

        # self.button_go.addItems(['Geometry', 'Measurement', 'Analysis', 'Identification'])

        subwindow_menu = QtGui.QMenu()
        subwindow_menu.addAction('Geometry')
        subwindow_menu.addAction('Measurement')
        subwindow_menu.addAction('Analysis')
        subwindow_menu.addAction('Identification')
        with open('style_template.css', 'r') as fh:
            src = Template(fh.read())
            src = src.substitute(COLOR_PALETTE)
            # print (src)
            subwindow_menu.setStyleSheet(src)
            # subwindow_menu.setStyleSheet(fh.read())


        self.button_go.setMenu(subwindow_menu)
        self.button_go.setPopupMode(QtGui.QToolButton.InstantPopup)


        # self.button_go.setView(QtGui.QListView())
        # self.button_go.setStyleSheet("QComboBox QAbstractItemView::item { min-height: 35px; min-width: 50px; }");
        self.button_settings = QtGui.QToolButton()
        self.button_settings.setText('settings')
        self.button_settings.setObjectName('linkbutton')
        # self.button_settings.setFlat(True)

        self.button_save = QtGui.QToolButton()
        self.button_save.setText('save')
        self.button_save.setObjectName('linkbutton')

        self.button_import = QtGui.QToolButton()
        self.button_import.setText('import')
        self.button_import.setObjectName('linkbutton')

        # self.button_import = QtGui.QLabel('<a href="#bu">import</a>')
        # # self.button_import.setText('import')
        # # self.button_import.setObjectName('linkbutton')
        # self.button_import.linkActivated.connect(lambda: print('bu'))


        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addWidget(self.button_go)
        self.hbox.addStretch()
        self.hbox.addWidget(self.button_settings)
        self.hbox.addWidget(self.button_save)
        self.hbox.addWidget(self.button_import)



        self.setLayout(self.hbox)

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super().__init__()

        self.menu = MainMenu()
        self.graphics = GraphicWindow()
        self.graphics.setMaximumHeight(400)
        self.table = QtGui.QTableWidget(10, 6)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(250)
        self.table.setMaximumWidth(600)
        self.table.setMinimumWidth(600)
        self.table.verticalHeader().hide()
        style =  ('::section {'
                 'spacing: 10px;'
                 'background-color: none;'
                 'color: white;'
                 'border: 1px solid red;'
                 'margin: 1px;'
                 'text-align: right;'
                 'font-family: arial;'
                 'font-size: 12px; }')

        style = ('::section {'
                 'background-color: #333333;'
                 'color: white;'
                 '}'
                 '::section:hover {'
                 'background-color: #666666;'
                 '}')

        self.table.horizontalHeader().setStyleSheet(style)

        self.hmenubox = QtGui.QHBoxLayout()
        self.hmenubox.addWidget(self.menu)
        self.vbox_gobal = QtGui.QVBoxLayout()
        self.vbox_gobal.addLayout(self.hmenubox)

        self.vbox = QtGui.QVBoxLayout()
        # self.vbox.addWidget(self.menu)
        self.vbox.addStretch()
        self.vbox.addWidget(self.graphics)

        self.table_hbox = QtGui.QHBoxLayout()
        self.table_hbox.addStretch()
        self.table_hbox.addWidget(self.table)
        self.table_hbox.addStretch()

        self.vbox.addLayout(self.table_hbox)

        self.graphics.sample()

        self.hbox = QtGui.QHBoxLayout()

        self.vbox_left = QtGui.QVBoxLayout()

        self.hbox.addLayout(self.vbox_left)
        self.hbox.addStretch()
        self.hbox.addLayout(self.vbox)

        self.vbox_gobal.addLayout(self.hbox)

        self.setLayout(self.vbox_gobal)

class GraphicWindow(da.DockArea):
    def __init__(self, title='All graphics go here'):
        super().__init__()

        self.resize(400, 200)
        self.dock_measuerement = da.Dock('Time-domain')
        self.graphic_view_measuerement = pg.GraphicsWindow()
        self.dock_measuerement.addWidget(self.graphic_view_measuerement)

        self.dock_frf = da.Dock('Frequency-domain')
        self.graphic_view_frf = pg.GraphicsWindow()
        self.dock_frf.addWidget(self.graphic_view_frf)

        self.addDock(self.dock_frf)
        self.addDock(self.dock_measuerement, 'above', self.dock_frf)


    def sample(self):
        sample_plot = self.graphic_view_measuerement.addPlot()
        sample_plot_frf = self.graphic_view_frf.addPlot()
        # sample_plot.showAxis('top', True)
        # sample_plot.showAxis('right', True)
        # sample_plot.showGrid(x=True, y=True)

        curve = sample_plot.plot(pen='#e67e22')
        curve_frf = sample_plot_frf.plot(pen='#2ecc71')
        def update(curve, curve_frf):
            curve.setData(np.random.rand(1000))
            curve_frf.setData(np.random.rand(1000))
            # sample_plot.enableAutoRange('xy', False)
            # sample_plot_frf.enableAutoRange('xy', False)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda curve=curve, curve_frf=curve_frf: update(curve, curve_frf))
        self.timer.start(50)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)



    app.setFont(QtGui.QFont('Helvetica [Cronyx]'))
    # app.setStyle(QtGui.QStyleFactory.create('windows'))
    main = FramelessContainer(app.desktop())
    main.show()
    # main.showFullScreen()

    sys.exit(app.exec_())