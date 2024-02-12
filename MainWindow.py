import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

from Controllers.MainWindowController import MainWindowController
from Views.Crud_Festivales import Ui_Form_Crud_Festivales
from Views.CRUD_Noches import Ui_Form_Crud_Noches
from Views.CRUD_Presentaciones import Ui_Form_Crud_Presentaciones
from Views.CRUD_Estadio_y_Sectores import Ui_Form_Crud_Estadio
from Views.CRUD_Grupos import Ui_Form_Crud_Grupos
from Views.CRUD_Reconocimientos import  Ui_Crud_Reconocimientos
from Views.Entrada import Ui_Form_Entradas
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def __init__(self) -> None:
        self.MainWindowController = MainWindowController(self)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(768, 460)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 390, 400, 19))
        font = QtGui.QFont()
        font.setFamily("MS Gothic")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(691, 392, 55, 16))
        font = QtGui.QFont()
        font.setFamily("MS Sans Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(180, 130, 402, 99))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("MS Gothic")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("MS Gothic")
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("MS Gothic")
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 768, 21))
        self.menubar.setObjectName("menubar")
        self.menufestivales = QtWidgets.QMenu(self.menubar)
        self.menufestivales.setObjectName("menufestivales")
        self.menuEstadios = QtWidgets.QMenu(self.menubar)
        self.menuEstadios.setObjectName("menuEstadios")
        self.menuGrupos_Musicales = QtWidgets.QMenu(self.menubar)
        self.menuGrupos_Musicales.setObjectName("menuGrupos_Musicales")
        self.menuEntradas = QtWidgets.QMenu(self.menubar)
        self.menuEntradas.setObjectName("menuEntradas")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.CRUD_Festival = QtWidgets.QAction(MainWindow)
        self.CRUD_Festival.setCheckable(False)
        self.CRUD_Festival.setObjectName("CRUD_Festival")
        self.CRUD_Noches = QtWidgets.QAction(MainWindow)
        self.CRUD_Noches.setObjectName("CRUD_Noches")
        self.CRUD_Presentaciones = QtWidgets.QAction(MainWindow)
        self.CRUD_Presentaciones.setObjectName("CRUD_Presentaciones")
        self.actionCRUD_Estadios = QtWidgets.QAction(MainWindow)
        self.actionCRUD_Estadios.setObjectName("actionCRUD_Estadios")
        self.CRUD_Estadios = QtWidgets.QAction(MainWindow)
        self.CRUD_Estadios.setObjectName("CRUD_Estadios")
        self.CRUD_Grupos = QtWidgets.QAction(MainWindow)
        self.CRUD_Grupos.setObjectName("CRUD_Grupos")
        self.CRUD_Reconocimientos = QtWidgets.QAction(MainWindow)
        self.CRUD_Reconocimientos.setObjectName("CRUD_Reconocimientos")
        self.actionImprimir = QtWidgets.QAction(MainWindow)
        self.actionImprimir.setObjectName("actionImprimir")
        self.CRUD_VentaDeEntradas = QtWidgets.QAction(MainWindow)
        self.CRUD_VentaDeEntradas.setObjectName("CRUD_VentaDeEntradas")
        self.menufestivales.addAction(self.CRUD_Festival)
        self.menufestivales.addAction(self.CRUD_Noches)
        self.menufestivales.addAction(self.CRUD_Presentaciones)
        self.menuEstadios.addAction(self.CRUD_Estadios)
        self.menuGrupos_Musicales.addAction(self.CRUD_Grupos)
        self.menuGrupos_Musicales.addAction(self.CRUD_Reconocimientos)
        self.menuEntradas.addAction(self.CRUD_VentaDeEntradas)
        self.menubar.addAction(self.menufestivales.menuAction())
        self.menubar.addAction(self.menuEstadios.menuAction())
        self.menubar.addAction(self.menuGrupos_Musicales.menuAction())
        self.menubar.addAction(self.menuEntradas.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #-------------------EVENTS----------------------------
        
        #Abro la pantalla Festival
        self.oFest = self.CRUD_Festival.triggered.connect(lambda:self.MainWindowController.screenCrud_Ventana(Ui_Form_Crud_Festivales))

        #Abro la pantalla Noches
        self.oNoches = self.CRUD_Noches.triggered.connect(lambda:self.MainWindowController.screenCrud_Ventana(Ui_Form_Crud_Noches))

        #Abro la pantalla Presentaciones
        self.oPresentaciones = self.CRUD_Presentaciones.triggered.connect(lambda:self.MainWindowController.screenCrud_Ventana(Ui_Form_Crud_Presentaciones))

        #Abro la pantalla Estadios
        self.oEstadios = self.CRUD_Estadios.triggered.connect(lambda:self.MainWindowController.screenCrud_Ventana(Ui_Form_Crud_Estadio))

        #Abro la pantalla Grupos Musicales
        self.oGrupos = self.CRUD_Grupos.triggered.connect(lambda:self.MainWindowController.screenCrud_Ventana(Ui_Form_Crud_Grupos))

        #Abro la pantalla Reconocimientos
        self.oReconocimientos = self.CRUD_Reconocimientos.triggered.connect(lambda:self.MainWindowController.screenCrud_Ventana(Ui_Crud_Reconocimientos))

        #Abro la pantalla Entradas
        self.oEntradas = self.menuEntradas.triggered.connect(lambda:self.MainWindowController.screenCrud_Ventana(Ui_Form_Entradas))

        

        
        
        
       
        #-------------------END EVENTS------------------------

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Direccion de Cultura de la Municipalidad"))
        self.label_5.setText(_translate("MainWindow", "<A/M>"))
        self.label_3.setText(_translate("MainWindow", "Diagramacion de la programacion"))
        self.label_4.setText(_translate("MainWindow", "Venta de entradas"))
        self.label_2.setText(_translate("MainWindow", "Administración de los Festivales"))
        self.menufestivales.setTitle(_translate("MainWindow", "Festivales"))
        self.menuEstadios.setTitle(_translate("MainWindow", "Estadios"))
        self.menuGrupos_Musicales.setTitle(_translate("MainWindow", "Grupos Musicales"))
        self.menuEntradas.setTitle(_translate("MainWindow", "Entradas"))
        self.CRUD_Festival.setText(_translate("MainWindow", "CRUD Festival"))
        self.CRUD_Noches.setText(_translate("MainWindow", "CRUD Noches"))
        self.CRUD_Presentaciones.setText(_translate("MainWindow", "CRUD Presentaciones"))
        self.actionCRUD_Estadios.setText(_translate("MainWindow", "CRUD Estadios"))
        self.CRUD_Estadios.setText(_translate("MainWindow", "CRUD Estadios"))
        self.CRUD_Grupos.setText(_translate("MainWindow", "CRUD Grupos"))
        self.CRUD_Reconocimientos.setText(_translate("MainWindow", "CRUD Reconocimientos"))
        self.actionImprimir.setText(_translate("MainWindow", "Imprimir"))
        self.CRUD_VentaDeEntradas.setText(_translate("MainWindow", "Venta de Entradas"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
