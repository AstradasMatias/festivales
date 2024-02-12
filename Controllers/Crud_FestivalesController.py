import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from Database.Connection import connection
from Models.Festival import Festival
from Models.Estadio import Estadio
from Models.Entradas import Entradas

class Crud_FestivalesController():
    
    def __init__(self, vistaFestival,c) -> None:
        self.festival = Festival(c)
        self.estadio = Estadio(c)
        self.entradas = Entradas(c)
        self.vistaFestival = vistaFestival
    
    def buscarFestival(self):
        global nombre_festival
        nombre_festival = self.vistaFestival.Edit_nombre_festivales.text()
        festival_encontrado = self.festival.buscar(nombre_festival)
        if festival_encontrado:
            global festival_id
            festival_id = festival_encontrado[0]
            self.vistaFestival.comboBox_estadio_crud_festival.setEnabled(True)
            global estadio_id
            estadio_id = festival_encontrado[2]
            nombre_estadio = self.estadio.buscar_id(estadio_id)
            global nombre_estadio_cb
            nombre_estadio_cb = nombre_estadio[1]

            self.vistaFestival.comboBox_estadio_crud_festival.setCurrentText(nombre_estadio_cb)
            #----
            table = self.vistaFestival.table_crud_festivales
            festivales = self.festival.listar()
            table.setRowCount(0)
            for row_number, row_data in enumerate(festivales):
                table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            self.vistaFestival.Button_crear_festivales.setEnabled(False)
            #----
            self.vistaFestival.Button_actualizar_festivales.setEnabled(True)
            self.vistaFestival.Button_eliminar_festivales.setEnabled(True)
        else:
            # Si hay error, el valor no es un int
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText(self.vistaFestival.Edit_nombre_festivales.text())

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("El estadio no existe")
            self.habilitarComboBox()
            x = msg.exec_()     

        return nombre_festival


    def habilitarComboBox(self):
        #habilito el crear
        self.vistaFestival.Button_crear_festivales.setEnabled(True)
        #Habilito el comboBox con los estadios que existan
        self.vistaFestival.comboBox_estadio_crud_festival.setEnabled(True)

    def comboEstadios(self):
        self.vistaFestival.comboBox_estadio_crud_festival.setEnabled(True)
        estadios = self.estadio.listar()
        for rows in estadios:
            estadio_nombre = str(rows[1])
            self.vistaFestival.comboBox_estadio_crud_festival.addItem(estadio_nombre)
        self.vistaFestival.comboBox_estadio_crud_festival.setCurrentIndex(-1)  

    def crear(self):
        nombre = nombre_festival
        print("soy el nombre que vengo de buscar",nombre)
        festival_existe = self.festival.buscar(nombre)
        print("festival_existe es: ",festival_existe)
        estadio_elegido = self.vistaFestival.comboBox_estadio_crud_festival.currentText()
        print("el estado elegido es: ",estadio_elegido)
        if festival_existe == None:
            ("ENTRE AL PRIMER TRY")         
            if nombre and estadio_elegido:
                #buscamos el id del estadio elegido
                self.estadio_elegido()
                self.festival.crear(str(nombre),estadio_seleccionado)
                self.listar()
            else:
                # Si hay error, el valor no es un int
                msg = QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setText(nombre)

                msg.setIcon(QMessageBox.Information) #critical warning and information

                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)

                msg.setInformativeText("Debe ingresar el estadio")
                x = msg.exec_()        
        else:
            # Si hay error, el valor no es un int
            msg = QMessageBox()
            msg.setWindowTitle("ERROR Festival no existe")
            msg.setText(self.vista_EstadioSector.Edit_nombre_crud_estadio.text())

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("El Festival ya existe.")
            x = msg.exec_()
        
    def estadio_elegido(self):
        estadio_elegido = self.vistaFestival.comboBox_estadio_crud_festival.currentText()
        estadio = self.estadio.buscar(estadio_elegido)
        global estadio_seleccionado
        estadio_seleccionado = estadio[0]
        return estadio_seleccionado
    
    def listar(self):
        table = self.vistaFestival.table_crud_festivales
        festivales = self.festival.listar()
        table.setRowCount(0)
        for row_number, row_data in enumerate(festivales):
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        self.vistaFestival.Button_crear_festivales.setEnabled(False)
        self.limpiar_pantalla()

    def actualizar(self):
        id_festival = festival_id
        festivales = []
        fila = []
        nombre = self.vistaFestival.Edit_nombre_festivales.text() 
        self.estadio_elegido()
        estadio = estadio_seleccionado
        id_estadio = estadio_id
        print("id del festival",id_festival)
        print("soy el id del estadio", id_estadio)


        if (str(nombre) != None) and (str(estadio) != None):
            fila.append(nombre)
            fila.append(estadio)
            fila.append(id_festival)
        else:
            print("Ingrese los datos correspondientes")
        if len(fila)>=0:
            festivales.append(fila)
        fila = []
        if len(festivales)>=0:
            for stadium in festivales:
                self.festival.update(stadium[0],stadium[1],stadium[2])
        self.listar()

    def eliminar(self):
        id_festival = festival_id
        festivales = self.festival.buscar(nombre_festival)
        if festivales:
            validar_eliminacion = self.entradas.validarEliminacionFestivales(id_festival)
            if validar_eliminacion:
                msg = QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setText(nombre_festival)

                msg.setIcon(QMessageBox.Information) #critical warning and information

                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)

                msg.setInformativeText("El Festival posee entradas no se puede eliminar. \nPara mas Informacion ponerse en contacto con el Directivo. ")
                x = msg.exec_()
            else:    
                self.festival.eliminar(id_festival)
                self.limpiar_pantalla()
                self.listar()
        else:
            # Si hay error, el valor no es un int
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText(self.vista_EstadioSector.Edit_nombre_crud_estadio.text())

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("No existe el estadio")
            x = msg.exec_() 

    def limpiar_pantalla(self):
        self.vistaFestival.Button_actualizar_festivales.setEnabled(False)
        self.vistaFestival.Button_crear_festivales.setEnabled(False)
        self.vistaFestival.comboBox_estadio_crud_festival.setEnabled(False)
        self.vistaFestival.Button_eliminar_festivales.setEnabled(False)
        self.vistaFestival.Edit_nombre_festivales.setText("")
