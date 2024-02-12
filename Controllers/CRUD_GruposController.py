import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from Database.Connection import connection
from Models.Grupos_folkloricos import Grupos_folkloricos
from Models.Reconocimientos import Reconocimientos
from Models.Entradas import Entradas

class CRUD_GruposController():

    def __init__(self, vistaGrupos,c) -> None:
        self.grupos = Grupos_folkloricos(c)
        self.reconocimientos = Reconocimientos(c)
        self.entradas = Entradas(c)
        self.vista_grupos = vistaGrupos
    
    def buscarGrupo(self):
        #texto del edit
        nombre = self.vista_grupos.Edit_nombre_crud_grupos.text()
        try:
            lista_grupo = self.grupos.buscar(nombre)
            if len(lista_grupo)>0:
                #Si entra aca es por existe en la bd
                print("existe")

                #lo listo
                self.listado_especial()

                #me traigo los datos
                self.habilitar__ifFound()
                
        except:
            #si entra aca es porque no existe en bd
            # Si hay error, el valor no es un int
            msg = QMessageBox()
            msg.setWindowTitle("ATENCION!")
            msg.setText(self.vista_grupos.Edit_nombre_crud_grupos.text())

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("Puede ser que lo que busca no exista, ingrese el nombre y crealo!!!")

            #habilito el ifNotFound
            self.habilitar__ifNotFound()

            x = msg.exec_()
            print("Hubo un error")

    def listar(self):
        table = self.vista_grupos.tableWidget
        grupos = self.grupos.listar()
        table.setRowCount(0)
        for row_number, row_data in enumerate(grupos):
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
    
    def listado_especial(self):
        #texto del edit
        nombre = self.vista_grupos.Edit_nombre_crud_grupos.text()
        table = self.vista_grupos.tableWidget
        grupos = self.grupos.listado_especial(nombre)
        table.setRowCount(0)
        for row_number, row_data in enumerate(grupos):
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        global codigo
        codigo = grupos[0]
        return codigo

    def habilitar__ifFound(self):
        #habilito los botones
        self.vista_grupos.Button_actualizar_crud_grupos.setEnabled(True)
        self.vista_grupos.Button_eliminar_crud_grupos.setEnabled(True)

        #habilito los textos
        self.vista_grupos.comboBox_reconocimientos_crud_grupos.setEnabled(True)
        
        #Me traigo el codigo
        self.vista_grupos.Edit_codigo_crud_grupos.setText(str(codigo[0]))
        self.vista_grupos.comboBox_reconocimientos_crud_grupos.setCurrentText((codigo[2]))

    def habilitar__ifNotFound(self):
        #habilito los botones
        self.vista_grupos.Button_crear_crud_grupos.setEnabled(True)

        #habilito los textos
        self.vista_grupos.comboBox_reconocimientos_crud_grupos.setEnabled(True)
    

    def cargar_comboBox(self):
        lista_reconocimientos = self.reconocimientos.listar()
        for rows in lista_reconocimientos:
            reconocimiento_nombre = str(rows[1])
            self.vista_grupos.comboBox_reconocimientos_crud_grupos.addItem(reconocimiento_nombre)
        self.vista_grupos.comboBox_reconocimientos_crud_grupos.setCurrentIndex(-1)

    def crearGrupo(self):
        #traerme el nombre del edit
        nombre = self.vista_grupos.Edit_nombre_crud_grupos.text()
        #traerme el texto del comboBox
        combo = self.vista_grupos.comboBox_reconocimientos_crud_grupos.currentText()
        #buscar el combo en la base de datos
        lista_combo = self.reconocimientos.buscar_id(combo)
        #traerme el id de ese nombre
        id_reconocimiento = lista_combo[0][0]
        #Insertarlo en la base de datos
        self.grupos.crear(nombre,id_reconocimiento)
        #listarlo
        self.listado_especial()
        #resetear a valores iniciales
        self.resetear_valores()

    def resetear_valores(self):
        self.vista_grupos.Edit_nombre_crud_grupos.setText("")
        self.vista_grupos.Edit_codigo_crud_grupos.setText("")
        self.vista_grupos.comboBox_reconocimientos_crud_grupos.setCurrentIndex(-1)
        self.vista_grupos.comboBox_reconocimientos_crud_grupos.setEnabled(False)
        self.vista_grupos.Button_crear_crud_grupos.setEnabled(False)
        self.vista_grupos.Button_actualizar_crud_grupos.setEnabled(False)
        self.vista_grupos.Button_eliminar_crud_grupos.setEnabled(False)

    def actualizarGrupo(self):
        #traerme el nombre del edit
        nombre = self.vista_grupos.Edit_nombre_crud_grupos.text()
        #buscar el id del nombre
        lista_nombre = self.grupos.buscar(nombre)
        id_nombre = lista_nombre[0]
        #traerme el texto del comboBox
        combo = self.vista_grupos.comboBox_reconocimientos_crud_grupos.currentText()
        #buscar el combo en la base de datos
        lista_combo = self.reconocimientos.buscar_id(combo)
        #traerme el id de ese nombre
        id_reconocimiento = lista_combo[0][0]
        #Actualizar la base de datos
        self.grupos.actualizar(nombre,id_reconocimiento,id_nombre)
        #listarlo
        self.listado_especial()
        #resetear a valores iniciales
        self.resetear_valores()
    
    def eliminarGrupo(self):
        #traerme el nombre del edit
        nombre = self.vista_grupos.Edit_nombre_crud_grupos.text()
        #buscar el id del nombre
        lista_nombre = self.grupos.buscar(nombre)
        id_nombre = lista_nombre[0]
        lista_eliminar = self.entradas.validarEliminacionGrupo(id_nombre)
        if lista_eliminar:
            msg = QMessageBox()
            msg.setWindowTitle("ATENCION!")
            msg.setText("Grupo No Eliminable")

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("No se puede Eliminar debido a que existe en otro lado!!!")

            #habilito el ifNotFound
            self.habilitar__ifNotFound()

            x = msg.exec_()
        else:
            #Eliminar en la base de datos
            self.grupos.eliminar(id_nombre)
            #listarlo pero no especial sino general
            self.listar()
            #resetear a valores iniciales
            self.resetear_valores()