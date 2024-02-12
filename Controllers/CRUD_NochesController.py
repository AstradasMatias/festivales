import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from Database.Connection import connection
from Models.Noches import Noches
from Models.Festival import Festival
from Models.Entradas import Entradas

class CRUD_NochesController():
    
    def __init__(self, vistaNoches,c) -> None:
        self.noches = Noches(c)
        self.festival = Festival(c)
        self.entradas = Entradas(c)
        self.vista_Noches = vistaNoches

    def comboEstadios(self):
        festivales = self.festival.listar()
        for rows in festivales:
            festival_nombre = str(rows[1])
            self.vista_Noches.comboBox.addItem(festival_nombre)
        self.vista_Noches.comboBox.setCurrentIndex(-1)

    def presionarCant_Noches(self):
        try:
            self.vista_Noches.comboBox_noche_numero.clear()
            cant_noches = int(self.vista_Noches.Edit_cantidad_noches.text())
            lista = []
            i = 1
            if cant_noches > 0:
                for i in range(cant_noches):
                    lista.append(i+1)
                self.vista_Noches.comboBox_noche_numero.setEnabled(True)
                self.vista_Noches.dateEdit_crud_noches.setEnabled(True)
                self.vista_Noches.Edit_hora_inicio_noches.setEnabled(True)
                self.habilitar_crear_eliminar()
                for rows in lista:
                    self.vista_Noches.comboBox_noche_numero.addItem(str(rows))
                self.vista_Noches.comboBox_noche_numero.setCurrentIndex(-1)
        except:
            print("Ingrese bien los datos numericos.")
        
        
    def habilitar_crear_eliminar(self):
        self.vista_Noches.Button_crear_noches.setEnabled(True)
        self.vista_Noches.Button_eliminar_noches.setEnabled(True)

    def crear(self):
        festival = self.vista_Noches.comboBox.currentText()
        cant_noches = self.vista_Noches.Edit_cantidad_noches.text()
        noche_numero = self.vista_Noches.comboBox_noche_numero.currentIndex()
        dia = self.vista_Noches.dateEdit_crud_noches.text()
        hora = self.vista_Noches.Edit_hora_inicio_noches.text()

        lista_festival = self.festival.buscar(festival)
        id_festival = lista_festival[0]
        noche_num = int(noche_numero)+1
        se_encuentra_disponible = self.noches.consultar_noche_disponible(noche_num,id_festival)
        if se_encuentra_disponible == ():
            self.noches.crear(cant_noches,noche_num,dia,hora,id_festival)
            self.vista_Noches.comboBox_noche_numero.removeItem(noche_numero)
            self.listar()
            self.presionarCant_Noches()
        else:
            print("La noche ya existe")

    def listar(self):
        festival = self.vista_Noches.comboBox.currentText()
        print(festival)
        try:
            lista_festival = self.festival.buscar(festival)
            id_festival = lista_festival[0]
            table = self.vista_Noches.table_crud_noche
            noches = self.noches.listar(id_festival)
            table.setRowCount(0)
            for row_number, row_data in enumerate(noches):
                table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            self.vista_Noches.Edit_cantidad_noches.setText(str(noches[0][1]))
            self.vista_Noches.Edit_cantidad_noches.setEnabled(True)
        except:
            msg = QMessageBox()
            msg.setWindowTitle("ATENCION")
            msg.setText(self.vista_Noches.comboBox.currentText())

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("No hay noches asignadas a este festival")
            self.vista_Noches.Edit_cantidad_noches.setEnabled(True)

            x = msg.exec_()

    def buscar_Noche(self):
        festival = self.vista_Noches.comboBox.currentText()
        lista_festival = self.festival.buscar(festival)
        global id_festival
        id_festival = lista_festival[0]
        noches = self.noches.listar(id_festival)
        global noche_numero
        noche_numero = noches[0][1]

    def eliminar(self):
        self.buscar_Noche()
        noche_num = int(self.vista_Noches.comboBox_noche_numero.currentText())
        festivales = self.noches.consultar_noche_disponible(noche_num,id_festival)
        if festivales != ():
            id_noche = festivales[0][0]
            noche_entradas = self.entradas.validarEliminacionNoches(id_noche)
            if noche_entradas:
                msg = QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setText("Noche")

                msg.setIcon(QMessageBox.Information) #critical warning and information

                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)

                msg.setInformativeText("No se puede  eliminar debido a un problema en la red, hablar con el encargado.")
                self.presionarCant_Noches()
                x = msg.exec_()
            else:
                self.noches.eliminar(noche_num,id_festival)
                self.listar()
        else:
            # Si hay error, el valor no es un int
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText(self.vista_Noches.comboBox.currentText())

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("No hay Noche a eliminar")
            self.presionarCant_Noches()
            x = msg.exec_()
      


