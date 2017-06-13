# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 22:19:26 2017

@author: Frederik
"""

from PyQt5 import QtWidgets, QtCore, QtGui
import sys

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.paintArea = paintWidget(self)
        self.setCentralWidget(self.paintArea)
        self.setWindowTitle('PUBG Flight Tracker')
        self.styleSet = False
        self.setGeometry(350,100,904,904)
        
        self.setAutoFillBackground(False)
        self.bg_palette = QtGui.QPalette()
        self.bg_palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("pubg_map.jpg").scaled(
                self.frameGeometry().width(), self.frameGeometry().height())))
        
        self.empty_palette = QtGui.QPalette()
        self.setPalette(self.empty_palette)
        
    def resizeEvent(self, event):
        if self.styleSet:
            self.bg_palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(QtGui.QPixmap("pubg_map.jpg").scaled(
                    self.frameGeometry().width(), self.frameGeometry().height())))
            self.setPalette(self.bg_palette)
        else:
            pass
        
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
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0

        self.map_button = QtWidgets.QPushButton('Show Map', self)
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
        self.vbox.addWidget(self.map_button, 0, QtCore.Qt.AlignLeft)
        self.vbox.addWidget(self.slider_label)
        self.vbox.addWidget(self.opac_slider, 0, QtCore.Qt.AlignLeft)
        
    def mousePressEvent(self, QMouseEvent):
        self.x1 = QMouseEvent.x()
        self.y1 = QMouseEvent.y()
        
    def mouseMoveEvent(self, QMouseEvent):
        self.x2 = QMouseEvent.x()
        self.y2 = QMouseEvent.y()
        self.update()
        
    def mouseReleaseEvent(self, QMouseEvent):
        self.x2 = QMouseEvent.x()
        self.y2 = QMouseEvent.y()
        
        self.x2 = (self.x2 - self.x1) * 500
        self.y2 = (self.y2 - self.y1) * 500
        
        self.x1 = (self.x2 - self.x1) * - 500
        self.y1 = (self.y2 - self.y1) * - 500
        
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.setOpacity(0.9)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.begin(self)
        try:
            self.drawLines(event, painter)
        except:
            pass
        painter.end()
        
    def drawLines(self, event, painter):
        pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.red), 5, QtCore.Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(self.x1, self.y1, self.x2, self.y2)
        
       
def main():
    app = QtWidgets.QApplication(sys.argv) 
    app.setWindowIcon(QtGui.QIcon('flighttracker_icon.png'))
    window = Window() 
    window.show() 
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()