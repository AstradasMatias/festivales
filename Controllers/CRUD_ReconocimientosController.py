import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from Database.Connection import connection
from Models.Reconocimientos import Reconocimientos
from Models.Grupos_folkloricos import Grupos_folkloricos

class CRUD_ReconocimientosController():
    
    def __init__(self, vistaReconocimientos,c) -> None:
        self.reconocimientos = Reconocimientos(c)
        self.banda = Grupos_folkloricos(c)
        self.vista_reconocimientos = vistaReconocimientos
        

    def inicializar(self):
        self.vista_reconocimientos.Button_crear_crud_reconocimientos.setEnabled(False)
        self.vista_reconocimientos.Button_eliminar_crud_reconocimientos.setEnabled(False)
        self.listar_al_principio()

    def buscar(self):
        tipo_r = self.vista_reconocimientos.Edit_tipo_reconocimiento.text()
        print("entre una vez")
        global lista
        lista_dato = self.reconocimientos.buscar_id(tipo_r)
        lista = []
        lista += lista_dato
        if lista != []:
            #existe
            self.listar()
            #si lo encontro habilito los botones
            self.vista_reconocimientos.Button_eliminar_crud_reconocimientos.setEnabled(True)
            self.vista_reconocimientos.Button_crear_crud_reconocimientos.setEnabled(False)
        else:
            self.listar()
            #no existe en la base de datos
            msg = QMessageBox()
            msg.setWindowTitle("ATENCION")
            msg.setText(self.vista_reconocimientos.Edit_tipo_reconocimiento.text())

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("No existe este Tipo de Reconocimiento, por favor agregelo.")
            self.vista_reconocimientos.Button_crear_crud_reconocimientos.setEnabled(True)

            x = msg.exec_()
            
    def crear(self):
        tipo_r = self.vista_reconocimientos.Edit_tipo_reconocimiento.text()
        self.reconocimientos.crear(tipo_r)
        self.buscar()
        self.vista_reconocimientos.Edit_tipo_reconocimiento.setText("")
        self.listar_al_principio()
        

    def listar(self):
        table = self.vista_reconocimientos.tableWidget
        table.setRowCount(0)
        for row_number, row_data in enumerate(lista):
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                print(data)
                table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
    
    def eliminar(self):
        tipo_r = self.vista_reconocimientos.Edit_tipo_reconocimiento.text()
        lista_full = self.reconocimientos.listar_x(tipo_r)
        id_reconocimiento = lista_full[0][0]
        print("id_reconocimiento",id_reconocimiento)
        lista_verifica_eliminar = self.banda.verificar_eliminar_reconocimiento(id_reconocimiento)
        if lista_verifica_eliminar:
            msg = QMessageBox()
            msg.setWindowTitle("ATENCION")
            msg.setText("Reconocimiento No Eliminable.")

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("No se puede eliminar este Reconocimiento ya que pertenece a una Banda.")
            self.listar_al_principio()
            x = msg.exec_()
        else:
            self.reconocimientos.eliminar(tipo_r)
            self.vista_reconocimientos.tableWidget.clearContents()
            self.buscar()

    def listar_al_principio(self):
        lista = self.reconocimientos.listar()
        table = self.vista_reconocimientos.tableWidget
        table.setRowCount(0)
        for row_number, row_data in enumerate(lista):
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                print(data)
                table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        