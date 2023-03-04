import sys
import os
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQuick import QQuickWindow

QQuickWindow.setSceneGraphBackend('software')
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
zadanie="UwU"
engine.load('./UI/main.qml')
engine.rootObjects()[0].setProperty('zadanie', zadanie)
sys.exit(app.exec())