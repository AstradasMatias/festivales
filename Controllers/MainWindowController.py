import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

from PyQt5 import QtWidgets
from Database.Connection import connection
from Models import *

class MainWindowController():
    def __init__(self, vista_MainWindow) -> None:
        self.c = connection()
        self.vista_MainWindow = vista_MainWindow
    
    def closeDB(self):
        self.c.close()

    def screenCrud_Ventana(self,Ui_Ventana):
        self.vista_MainWindow.Form = QtWidgets.QWidget()
        self.vista_MainWindow.ui = Ui_Ventana(self.c)
        self.vista_MainWindow.ui.setupUi(self.vista_MainWindow.Form)
        self.vista_MainWindow.Form.show()

    