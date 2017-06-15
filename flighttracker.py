# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 22:19:26 2017

@author: Frederik
"""

from PyQt5 import QtWidgets, QtCore, QtGui
from math import sqrt
import sys

class FlightLine:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

class ParachutePolygons:
    def __init__(self):
        self.innerPolygon = QtGui.QPolygonF()
        self.outerPolygon_1 = QtGui.QPolygonF()
        self.outerPolygon_2 = QtGui.QPolygonF()
        
class Marker:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xrange = (x-2, x+2)
        self.yrange = (y-2, y+2)

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.paintArea = paintWidget(self)              
        self.setCentralWidget(self.paintArea)
        self.setWindowTitle('PUBG Flight Tracker')
        
#        screen = QtWidgets.QApplication.desktop().screenNumber()
        self.resize(QtWidgets.QDesktopWidget().availableGeometry().height(), QtWidgets.QDesktopWidget().availableGeometry().height())
        self.move(QtWidgets.QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())
        
#        self.flags = QtCore.Qt.Window
        self.flag_toggle = False
#        self.setWindowFlags(self.flags)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)
        
        self.bg_palette = QtGui.QPalette()
        self.bg_palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("pubg_map.jpg").scaled(
                self.frameGeometry().width(), self.frameGeometry().height())))
        
        self.styleSet = False
        self.empty_palette = QtGui.QPalette()
        self.setPalette(self.empty_palette)

    def resizeEvent(self, event):
        if self.styleSet:
            self.bg_palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("pubg_map.jpg").scaled(
                    self.frameGeometry().width(), self.frameGeometry().height())))
            self.setPalette(self.bg_palette)
        else:
            pass
        
    def move_toggle(self):
        flags = QtCore.Qt.Window
        print(flags)
        if self.flag_toggle is False:
            flags |= QtCore.Qt.FramelessWindowHint
            self.flag_toggle = True
        
        elif self.flag_toggle is True:
            self.flag_toggle = False
            
        self.setWindowFlags(flags)
        self.show()
        
    def setOpacity(self, value):
        opacity = value / 100
        self.setWindowOpacity(opacity)
        
    def setStyle(self):
        if self.styleSet:
#            self.setStyleSheet('')
            self.setPalette(self.empty_palette)
            self.styleSet = False
        else:
#            self.setStyleSheet("QWidget {border-image: url('pubg_map.jpg');}")
            self.setPalette(self.bg_palette)
            self.styleSet = True 
            
        
class paintWidget(QtWidgets.QWidget):
    def __init__(self, parent = Window):
        super(paintWidget, self).__init__(parent)
        
        self.FlightLine = True
        self.redraw = False
        self.scatter = False
        self.parachuteDrawn = False
        
        self.markers = []
        self.polygons = ParachutePolygons()
        self.flightLine = None
        self.flightAreaToggle = True
        
        self.size = self.frameGeometry().width()
        self.offset_inner = 0.1875 * self.size
        self.offset_outer = 0.075 * self.size
        
        self.brush = QtGui.QBrush()
        self.brush.setStyle(QtCore.Qt.SolidPattern)
                
        self.start_button = QtWidgets.QPushButton('(Re)Start', self)
        self.start_button.clicked.connect(self.start)
        self.move_toggle_button = QtWidgets.QPushButton('Toggle Window Frame', self)
        self.move_toggle_button.clicked.connect(parent.move_toggle)
        self.chute_toggle_button = QtWidgets.QPushButton('Toggle Parachute', self)
        self.chute_toggle_button.clicked.connect(self.chute_toggle)
        self.map_button = QtWidgets.QPushButton('Toggle Map', self)
        self.map_button.clicked.connect(parent.setStyle)   
        self.opac_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.opac_slider.setRange(40, 100)
        self.opac_slider.valueChanged.connect(parent.setOpacity)
        self.opac_slider.setProperty('value', 100)
        self.slider_label = QtWidgets.QLabel()
        self.slider_label.setText('Change Opacity')
        
        self.logo = QtWidgets.QLabel()
        self.logo.setGeometry(10, 10, 90, 100)
        self.logo.setPixmap(QtGui.QPixmap('flighttracker_logo.png'))
        
        self.vbox = QtWidgets.QVBoxLayout()
        self.setLayout(self.vbox)
        self.vbox.addWidget(self.logo)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.start_button, 0, QtCore.Qt.AlignLeft)
        self.vbox.addWidget(self.move_toggle_button, 0, QtCore.Qt.AlignLeft)
        self.vbox.addWidget(self.chute_toggle_button, 0, QtCore.Qt.AlignLeft)
        self.vbox.addWidget(self.map_button, 0, QtCore.Qt.AlignLeft)
        self.vbox.addWidget(self.slider_label)
        self.vbox.addWidget(self.opac_slider, 0, QtCore.Qt.AlignLeft)

    def start(self):
        self.redraw = True
        self.markers = []
        self.parachuteDrawn = False
        self.flightLine = None
        self.flightAreaToggle = True
        self.polygons = ParachutePolygons()
        self.update()       
        
    def chute_toggle(self):
        if self.flightAreaToggle is False:
            self.flightAreaToggle = True
        
        else:
            self.flightAreaToggle = False
            
        self.update()
    
    def resizeEvent(self, event):
        self.size = self.frameGeometry().width()
        self.offset_inner = 0.1875 * self.size
        self.offset_outer = 0.075 * self.size
        
    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == QtCore.Qt.RightButton:
            self.scatter = True
            self.FlightLine = False
            self.FlightArea = False
            
        if QMouseEvent.button() == QtCore.Qt.LeftButton:
            self.FlightLine = True
            self.FlightArea = False
    
        self.x1 = QMouseEvent.x()
        self.y1 = QMouseEvent.y()
        
    def mouseMoveEvent(self, QMouseEvent):
        self.x2 = QMouseEvent.x()
        self.y2 = QMouseEvent.y()
        self.update()
        
    def mouseReleaseEvent(self, QMouseEvent):
        self.x2 = QMouseEvent.x()
        self.y2 = QMouseEvent.y()
        
        if QMouseEvent.button() == QtCore.Qt.RightButton:
            for i, marker in enumerate(self.markers):
                if abs(self.x2 - marker.x) < 10 and abs(self.y2 - marker.y) < 10:
                    del self.markers[i]
                    self.scatter = False

        if self.FlightLine is True: 
            self.x2 = (self.x2 - self.x1) * 100
            self.y2 = (self.y2 - self.y1) * 100
            self.x1 = (self.x2 - self.x1) * - 100
            self.y1 = (self.y2 - self.y1) * - 100
        
        if self.parachuteDrawn is False and QMouseEvent.button() == QtCore.Qt.LeftButton:
            self.FlightArea = True
            
        self.update()
        
    def paintEvent(self, event):
        
        if self.redraw is True:
            self.redraw = False
            painter = QtGui.QPainter()
            painter.setPen(QtGui.QPen(QtCore.Qt.gray,3,QtCore.Qt.DashDotLine ) )
            painter.begin(self)
            rect = QtCore.QRectF(0, 0, self.frameGeometry().width()-1, self.frameGeometry().height()-1)
            painter.drawRect(rect)
            painter.fillRect(rect, QtGui.QBrush(QtGui.QColor(128, 128, 255, 1))) 
            return
        painter = QtGui.QPainter()
        
        painter.setPen(QtGui.QPen(QtCore.Qt.gray,3,QtCore.Qt.DashDotLine ) )
        
        painter.begin(self)
               
        rect = QtCore.QRectF(0, 0, self.frameGeometry().width()-1, self.frameGeometry().height()-1)
        painter.drawRect(rect)
        painter.fillRect(rect, QtGui.QBrush(QtGui.QColor(128, 128, 255, 1)))  

        painter.setOpacity(1)
        
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        try:
            if self.scatter is True:
                self.drawScatter(event, painter)
                self.scatter = False
            
            elif len(self.markers) > 0:
                self.redrawScatter(event, painter)
            
            if self.parachuteDrawn is False and self.FlightLine is True:
                    self.drawFlightLine(event, painter)
                    
            if self.parachuteDrawn is False and self.FlightArea is True:
                self.drawParachute(event, painter)
                    
            if self.parachuteDrawn is True:
                self.redrawFlightLine(event, painter)
                if self.flightAreaToggle is True:
                    self.redrawParachute(event, painter)
            
        except:
            pass
        
        painter.end()
        
    def drawScatter(self, event, painter):
        painter.setOpacity(1)
        pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.blue), 10, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        
        self.markers.append(Marker(self.x2, self.y2))
        
        for marker in self.markers:
            painter.drawPoint(marker.x, marker.y)
            
    def redrawScatter(self, event, painter):
        painter.setOpacity(1)
        pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.blue), 10, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        
        for marker in self.markers:
            painter.drawPoint(marker.x, marker.y)
        
    def drawFlightLine(self, event, painter):
        pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.red), 5, QtCore.Qt.SolidLine)
        painter.setOpacity(1)
        painter.setPen(pen)
        painter.drawLine(self.x1, self.y1, self.x2, self.y2)
        self.flightLine = FlightLine(self.x1, self.y1, self.x2, self.y2)
        
    def redrawFlightLine(self, event, painter):
        pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.red), 5, QtCore.Qt.SolidLine)
        painter.setOpacity(1)
        painter.setPen(pen)
        painter.drawLine(self.flightLine.x1, self.flightLine.y1, self.flightLine.x2, self.flightLine.y2)
        
    def drawParachute(self, event, painter):
        painter.setOpacity(0.6)
        
        pen = QtGui.QPen(QtCore.Qt.NoPen)
        painter.setPen(pen)
                       
        path_inner = QtGui.QPainterPath()
        path_outer = QtGui.QPainterPath()
        
        xperp_inner, yperp_inner, xperp_outer, yperp_outer = self.perpCalc(self.x1, self.y1, self.x2, self.y2, self.offset_inner)
              
        x3, y3 = self.x1 + yperp_inner, self.y1 - xperp_inner
        x4, y4 = self.x1 - yperp_inner, self.y1 + xperp_inner
        x5, y5 = self.x2 - yperp_inner, self.y2 + xperp_inner
        x6, y6 = self.x2 + yperp_inner, self.y2 - xperp_inner
        
        for x, y in zip([x3, x4, x5, x6], [y3, y4, y5, y6]):
            self.polygons.innerPolygon.append(QtCore.QPointF(x, y))
               
        self.brush.setColor(QtGui.QColor(255, 127, 80, 128))
        painter.drawPolygon(self.polygons.innerPolygon)
        path_inner.addPolygon(self.polygons.innerPolygon)
        painter.fillPath(path_inner, self.brush)
        
        x7, y7 = x3 + yperp_outer, y3 - xperp_outer
        x8, y8 = x6 + yperp_outer, y6 - xperp_outer
            
        for x, y in zip([x3, x6, x8, x7], [y3, y6, y8, y7]):
            self.polygons.outerPolygon_1.append(QtCore.QPointF(x, y))
                        
        painter.drawPolygon(self.polygons.outerPolygon_1)
        path_outer.addPolygon(self.polygons.outerPolygon_1)
        
        x9, y9 = x4 - yperp_outer, y4 + xperp_outer
        x10, y10 = x5 - yperp_outer, y5 + xperp_outer

        for x, y in zip([x5, x4, x9, x10], [y5, y4, y9, y10]):
            self.polygons.outerPolygon_2.append(QtCore.QPointF(x, y))
        
        painter.drawPolygon(self.polygons.outerPolygon_2)
        path_outer.addPolygon(self.polygons.outerPolygon_2)
        
        self.brush.setColor(QtGui.QColor(255, 215, 10, 128))
        painter.fillPath(path_outer, self.brush)
        
        self.parachuteDrawn = True
        
    def redrawParachute(self, event, painter):
        painter.setOpacity(0.6)
        
        pen = QtGui.QPen(QtCore.Qt.NoPen)
        painter.setPen(pen)
        
        path_inner = QtGui.QPainterPath()
        path_outer = QtGui.QPainterPath()
        
        self.brush.setColor(QtGui.QColor(255, 127, 80, 128))
        painter.drawPolygon(self.polygons.innerPolygon)
        path_inner.addPolygon(self.polygons.innerPolygon)
        painter.fillPath(path_inner, self.brush)
        
        painter.drawPolygon(self.polygons.outerPolygon_1)
        path_outer.addPolygon(self.polygons.outerPolygon_1)
        
        painter.drawPolygon(self.polygons.outerPolygon_2)
        path_outer.addPolygon(self.polygons.outerPolygon_2)
        
        self.brush.setColor(QtGui.QColor(255, 215, 10, 128))
        painter.fillPath(path_outer, self.brush)
         
    def perpCalc(self, x1, y1, x2, y2, offset):
        dx = x1 - x2
        dy = y1 - y2
        
        dist = sqrt(dx * dx + dy * dy)
        
        normx = dx / dist
        normy = dy / dist
        
        xperp_inner = self.offset_inner * normx
        yperp_inner = self.offset_inner * normy
        
        xperp_outer = self.offset_outer * normx
        yperp_outer = self.offset_outer * normy
        
        return xperp_inner, yperp_inner, xperp_outer, yperp_outer
             
def main():
    app = QtWidgets.QApplication(sys.argv) 
    app.setWindowIcon(QtGui.QIcon('flighttracker_icon.png'))
    window = Window() 
    window.show() 
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()