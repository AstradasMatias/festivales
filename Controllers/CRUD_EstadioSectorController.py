import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from Database.Connection import connection
from Models.Estadio import Estadio
from Models.Sectores import Sectores
from Models.Cant_sect_ing import Cant_sect_ing
from Models.Entradas import Entradas


class CRUD_EstadioSectorController():

    #recibe la vista como segundo parametro
    def __init__(self, EstadioSector,c) -> None:
        self.estadio = Estadio(c)
        self.sector = Sectores(c)
        self.cant_sect_ingr = Cant_sect_ing(c)
        self.entradas = Entradas(c)
        #Ahora convierto la vista en un atributo
        self.vista_EstadioSector = EstadioSector

    #-------------------ESTADIOS
    def listarEstadios(self):
        table = self.vista_EstadioSector.table_estadio
        estadios = self.estadio.listar()
        table.setRowCount(0)
        for row_number, row_data in enumerate(estadios):
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        self.vista_EstadioSector.Button_crear_crud_sectores_2.setEnabled(False)

        

    def buscar_estadio(self,nombre):
        self.vista_EstadioSector.Button_eliminar_crud_sectores_2.setEnabled(False)
        self.vista_EstadioSector.Button_actualizar_crud_sectores_2.setEnabled(False)
        estadio_especifico = self.estadio.buscar(nombre)                
        if estadio_especifico: 
            self.vista_EstadioSector.Edit_capacidad_crud_estadio.setEnabled(True)
            self.vista_EstadioSector.Edit_cant_sectores.setEnabled(True)
            self.vista_EstadioSector.Edit_nombre_crud_estadio.setText(str(estadio_especifico[1]))             
            self.vista_EstadioSector.Edit_capacidad_crud_estadio.setText(str(estadio_especifico[2]))
            self.vista_EstadioSector.Edit_cant_sectores.setText(str(estadio_especifico[3]))
            self.vista_EstadioSector.Edit_invisible.setText(str(estadio_especifico[0]))
            self.vista_EstadioSector.Button_eliminar_crud_sectores_2.setEnabled(True)
            self.vista_EstadioSector.Button_actualizar_crud_sectores_2.setEnabled(True)
            self.listarEstadios()
            self.habilitar_sectores()
            capacidad = int(self.vista_EstadioSector.Edit_capacidad_crud_estadio.text())
            cantidad = int(self.vista_EstadioSector.Edit_cant_sectores.text())
            butacas_X_sector = capacidad//cantidad
            self.vista_EstadioSector.Edit_butacas_X_sector.setText(str(butacas_X_sector))
        else:
            self.vista_EstadioSector.Button_crear_crud_sectores_2.setEnabled(True)
            msg = QMessageBox()
            msg.setWindowTitle("Informacion")
            msg.setText("Informacion")
            msg.setIcon(QMessageBox.Icon.Information) #Critical,Warning,Information
            msg.setStandardButtons(QMessageBox.StandardButton.Ok) #"Cancel,"war,close,yes,not,retry            
            msg.setInformativeText("El Estadio no existe, por favor presione el boton crear y agregelo!")
            self.habilitar_crearEstadios()
            msg.exec()

    def habilitar_crearEstadios(self):
        #Edit_capacidad_crud_estadio
        self.vista_EstadioSector.Edit_capacidad_crud_estadio.setEnabled(True)
        self.vista_EstadioSector.Edit_capacidad_crud_estadio.setText("")
        #Edit_cant_sectores
        self.vista_EstadioSector.Edit_cant_sectores.setEnabled(True)
        self.vista_EstadioSector.Edit_cant_sectores.setText("")

    def actualizar_estadios(self):
        id = self.vista_EstadioSector.Edit_invisible.text()
        estadio = []
        fila = []
        nombre = self.vista_EstadioSector.Edit_nombre_crud_estadio.text() 
        capacidad = self.vista_EstadioSector.Edit_capacidad_crud_estadio.text()
        cant_sectores = self.vista_EstadioSector.Edit_cant_sectores.text()
       
        if (str(nombre) != None) and (str(capacidad) != None) and (str(cant_sectores) != None):
            fila.append(nombre)
            fila.append(capacidad)
            fila.append(cant_sectores)
            fila.append(id)
        else:
            print("Ingrese los datos correspondientes")
        if len(fila)>=0:
            estadio.append(fila)
        fila = []
        if len(estadio)>=0:
            for stadium in estadio:
                self.estadio.actualizar(stadium[0],stadium[1],stadium[2],stadium[3])
        self.listarEstadios()
        butacas_X_sector = int(capacidad) // int(cant_sectores)
        self.vista_EstadioSector.Edit_butacas_X_sector.setText(str(butacas_X_sector)) 

    def eliminar_estadios(self):
        id_estadio = self.vista_EstadioSector.Edit_invisible.text()
        sectores = self.sector.buscar_listar(id_estadio)
        print(sectores)
        if sectores == ():
            self.cant_sect_ingr.eliminar(id_estadio)
            self.estadio.eliminar(id_estadio)
            self.resetear_valores()
            self.vista_EstadioSector.Button_listar_crud_sectores.setEnabled(False)
            self.limpiar_pantalla()
        else:
            # Si hay error, el valor no es un int
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText(self.vista_EstadioSector.Edit_nombre_crud_estadio.text())

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("Este Estadio cuenta con Sectores asignados. Primero eliminelos!")
            x = msg.exec_() 

    def crear_estadio(self, nombre, capacidad_personas,cantidad_sectores):
        estadio = self.estadio.buscar(nombre)
        if estadio == None:
            try:
                # Intenta convertir el texto del edit a un int
                valor_capacidad = int(self.vista_EstadioSector.Edit_capacidad_crud_estadio.text())
                valor_cant_sect = int(self.vista_EstadioSector.Edit_cant_sectores.text())
                # Si no hay error, el valor es un int
                print("no se encuentra en la base de datos.")
                if nombre and capacidad_personas and cantidad_sectores:
                    self.estadio.crear(nombre,capacidad_personas,cantidad_sectores)
                    self.listarEstadios
                butacas_X_sector = valor_capacidad//valor_cant_sect
                self.vista_EstadioSector.Edit_butacas_X_sector.setText(str(butacas_X_sector))
                self.buscar_estadio(self.vista_EstadioSector.Edit_nombre_crud_estadio.text())
                self.cant_sect_ingr.insert_cant_sect(0,int(self.vista_EstadioSector.Edit_invisible.text()))
                cant_Sect_ingr = self.cant_sect_ingr.getCantSectIng(self.vista_EstadioSector.Edit_invisible.text()) 
                self.vista_EstadioSector.Edit_cant_sect_disponibles.setText(str(cant_Sect_ingr[1]))
            except ValueError:
                # Si hay error, el valor no es un int
                msg = QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setText(self.vista_EstadioSector.Edit_nombre_crud_estadio.text())

                msg.setIcon(QMessageBox.Information) #critical warning and information

                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)

                msg.setInformativeText("Debe ingresar un valor numerico sin comas en capacidad_personas y cantidad_sectores")
                x = msg.exec_()        
        else:
            # Si hay error, el valor no es un int
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText(self.vista_EstadioSector.Edit_nombre_crud_estadio.text())

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("El estadio ya existe.")
            x = msg.exec_()
        
            
         
    #----------------------------------------        
    #Funcion interna
    def resetear_valores_sectores(self):
        #---sector
        #Edit_identSector_crud_sectores
        self.vista_EstadioSector.Edit_identSector_crud_sectores.setEnabled(False)
        self.vista_EstadioSector.Edit_identSector_crud_sectores.setText("")
        #Edit_ColorSector_crud_sectores
        self.vista_EstadioSector.Edit_ColorSector_crud_sectores.setEnabled(False)
        self.vista_EstadioSector.Edit_ColorSector_crud_sectores.setText("")
        #Edit_PrecioSector_crud_sectores
        self.vista_EstadioSector.Edit_PrecioSector_crud_sectores.setEnabled(False)
        self.vista_EstadioSector.Edit_PrecioSector_crud_sectores.setText("")
        #Edit_FilasSector_crud_sectores
        self.vista_EstadioSector.Edit_FilasSector_crud_sectores.setEnabled(False)
        self.vista_EstadioSector.Edit_FilasSector_crud_sectores.setText("")
        #Edit_ButacasSector_crud_sectores
        self.vista_EstadioSector.Edit_ButacasSector_crud_sectores.setEnabled(False)
        self.vista_EstadioSector.Edit_ButacasSector_crud_sectores.setText("")

        #Button_crear_crud_sectores
        self.vista_EstadioSector.Button_crear_crud_sectores.setEnabled(False)
        #Button_actualizar_crud_sectores
        self.vista_EstadioSector.Button_actualizar_crud_sectores.setEnabled(False)
        #Button_eliminar_crud_sectores
        self.vista_EstadioSector.Button_eliminar_crud_sectores.setEnabled(False)


    def resetear_valores(self):
        #listo
        self.listarEstadios()
        #pongo en blanco los edit
        self.vista_EstadioSector.Edit_nombre_crud_estadio.setText(str(""))             
        self.vista_EstadioSector.Edit_capacidad_crud_estadio.setText(str(""))
        self.vista_EstadioSector.Edit_cant_sectores.setText(str(""))
        self.vista_EstadioSector.Edit_invisible.setText(str(""))
        #inabilito los botones
        self.vista_EstadioSector.Button_actualizar_crud_sectores_2.setEnabled(False)
        self.vista_EstadioSector.Button_eliminar_crud_sectores_2.setEnabled(False)
        self.vista_EstadioSector.Button_crear_crud_sectores_2.setEnabled(False)

    #Funcion interna
    def habilitar_sectores(self):
        self.vista_EstadioSector.Button_listar_crud_sectores.setEnabled(True)
        self.vista_EstadioSector.Button_Seleccionar_Sector.setEnabled(True)

    def habilitar_editsYbotones(self):
        self.vista_EstadioSector.Edit_identSector_crud_sectores.setEnabled(True)
        self.vista_EstadioSector.Edit_ColorSector_crud_sectores.setEnabled(True)
        self.vista_EstadioSector.Edit_PrecioSector_crud_sectores.setEnabled(True)
        self.vista_EstadioSector.Edit_FilasSector_crud_sectores.setEnabled(True)
        self.vista_EstadioSector.Edit_ButacasSector_crud_sectores.setEnabled(False)

        #botones
        self.vista_EstadioSector.Button_actualizar_crud_sectores.setEnabled(True)
        self.vista_EstadioSector.Button_eliminar_crud_sectores.setEnabled(True)
    
    def habilitar_crear_sector(self):
        self.vista_EstadioSector.Edit_identSector_crud_sectores.setEnabled(True)
        self.vista_EstadioSector.Edit_ColorSector_crud_sectores.setEnabled(True)
        self.vista_EstadioSector.Edit_PrecioSector_crud_sectores.setEnabled(True)
        self.vista_EstadioSector.Edit_FilasSector_crud_sectores.setEnabled(True)
        self.vista_EstadioSector.Edit_ButacasSector_crud_sectores.setEnabled(False)

        self.vista_EstadioSector.Button_crear_crud_sectores.setEnabled(True)
        self.vista_EstadioSector.Button_CalcularButacas.setEnabled(True)
        #botones
        self.vista_EstadioSector.Button_actualizar_crud_sectores.setEnabled(False)
        self.vista_EstadioSector.Button_eliminar_crud_sectores.setEnabled(False)

    def limpiar_pantalla(self):
        #habilito nombre sector
        self.vista_EstadioSector.Edit_nombre_crud_estadio.setEnabled(True)
        self.vista_EstadioSector.Edit_nombre_crud_estadio.setText("")
        #habilito boton buscar
        self.vista_EstadioSector.Button_capacidad_crud_estadio.setEnabled(True)

        #Edit_capacidad_crud_estadio
        self.vista_EstadioSector.Edit_capacidad_crud_estadio.setEnabled(False)
        self.vista_EstadioSector.Edit_capacidad_crud_estadio.setText("")
        #Edit_cant_sectores
        self.vista_EstadioSector.Edit_cant_sectores.setEnabled(False)
        self.vista_EstadioSector.Edit_cant_sectores.setText("")

        #listar - Button_listar_crud_sectores_2
        self.vista_EstadioSector.Button_listar_crud_sectores_2.setEnabled(True)

        #crear - Button_crear_crud_sectores_2
        self.vista_EstadioSector.Button_crear_crud_sectores_2.setEnabled(False)
        #actualizar - Button_actualizar_crud_sectores_2
        self.vista_EstadioSector.Button_actualizar_crud_sectores_2.setEnabled(False)
        #eliminar - Button_eliminar_crud_sectores_2
        self.vista_EstadioSector.Button_eliminar_crud_sectores_2.setEnabled(False)

        self.vista_EstadioSector.Edit_invisible.setText("")
        self.vista_EstadioSector.Edit_invisible.setVisible(False)

        #---sector
        #Edit_identSector_crud_sectores
        self.vista_EstadioSector.Edit_identSector_crud_sectores.setEnabled(False)
        self.vista_EstadioSector.Edit_identSector_crud_sectores.setText("")
        #Edit_ColorSector_crud_sectores
        self.vista_EstadioSector.Edit_ColorSector_crud_sectores.setEnabled(False)
        self.vista_EstadioSector.Edit_ColorSector_crud_sectores.setText("")
        #Edit_PrecioSector_crud_sectores
        self.vista_EstadioSector.Edit_PrecioSector_crud_sectores.setEnabled(False)
        self.vista_EstadioSector.Edit_PrecioSector_crud_sectores.setText("")
        #Edit_FilasSector_crud_sectores
        self.vista_EstadioSector.Edit_FilasSector_crud_sectores.setEnabled(False)
        self.vista_EstadioSector.Edit_FilasSector_crud_sectores.setText("")
        #Edit_ButacasSector_crud_sectores
        self.vista_EstadioSector.Edit_ButacasSector_crud_sectores.setEnabled(False)
        self.vista_EstadioSector.Edit_ButacasSector_crud_sectores.setText("")

        #Button_listar_crud_sectores
        self.vista_EstadioSector.Button_listar_crud_sectores.setEnabled(False)
        #Button_crear_crud_sectores
        self.vista_EstadioSector.Button_crear_crud_sectores.setEnabled(False)
        #Button_actualizar_crud_sectores
        self.vista_EstadioSector.Button_actualizar_crud_sectores.setEnabled(False)
        #Button_eliminar_crud_sectores
        self.vista_EstadioSector.Button_eliminar_crud_sectores.setEnabled(False)
        #Button_Seleccionar_Sector
        self.vista_EstadioSector.Button_Seleccionar_Sector.setEnabled(False)

        self.vista_EstadioSector.Edit_cant_sect_disponibles.setText("")
        self.vista_EstadioSector.Edit_butacas_X_sector.setText("")
        
        self.vista_EstadioSector.Button_CalcularButacas.setEnabled(False)

        #tabla
        self.vista_EstadioSector.table_estadio.setRowCount(0)
        self.vista_EstadioSector.table_sectores.setRowCount(0)

   
    #-----------------------------------------

    #----------SECTOR
    def listarSectores(self):
        id_estadio = self.vista_EstadioSector.Edit_invisible.text()
        table = self.vista_EstadioSector.table_sectores
        sector = self.sector.buscar_listar(id_estadio)
        table.setRowCount(0)
        if sector:    
            for row_number, row_data in enumerate(sector):
                table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            self.vista_EstadioSector.Button_crear_crud_sectores.setEnabled(False)
            #verifico cuantos sectores tengo
            cant_sectores = self.cant_sect_ingr.getCantSectIng(id_estadio)
            print(cant_sectores)
            self.vista_EstadioSector.Edit_cant_sect_disponibles.setText(str(cant_sectores[1]))
            self.habilitar_editsYbotones()
            self.habilitar_crear_sector()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Nuevo Estadio!")
            msg.setText(self.vista_EstadioSector.Edit_nombre_crud_estadio.text())

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("Sector: "+"Ingrese una letra x Sector"+"\nColor: "+"Ingrese el color del sector"+"\nPrecio: "+"Ingrese el precio del sector"+"\nFilas: "+"las filas se generan automaticamente"+"\nButacas: "+"las butacas se generan automaticamente")
            x = msg.exec_()
            #verifico cuantos sectores tengo
            self.habilitar_crear_sector()
            cant_sectores = self.cant_sect_ingr.getCantSectIng(id_estadio)
            print(cant_sectores)
            self.vista_EstadioSector.Edit_cant_sect_disponibles.setText(str(cant_sectores[1]))
    
        
            

    def seleccionar_Sector(self):
        nombre_estadio = self.vista_EstadioSector.Edit_nombre_crud_estadio.text()
        id_estadio = self.vista_EstadioSector.Edit_invisible.text()
        table = self.vista_EstadioSector.table_sectores
        if table.currentItem() != None:
            cod = table.currentItem().text()#el .text es para que me lo haga string
            product = self.sector.listar(id_estadio,cod)
            if product:
                msg = QMessageBox()
                msg.setWindowTitle(nombre_estadio)
                msg.setText(nombre_estadio)

                msg.setIcon(QMessageBox.Information) #critical warning and information

                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)

                msg.setInformativeText("Sector: "+str(product[0])+"\nColor: "+str(product[1])+"\nPrecio: "+str(product[2])+"\nFilas: "+str(product[3])+"\nButacas: "+str(product[4]))

                self.vista_EstadioSector.Edit_identSector_crud_sectores.setText(str(product[0]))
                self.vista_EstadioSector.Edit_ColorSector_crud_sectores.setText(str(product[1]))
                self.vista_EstadioSector.Edit_PrecioSector_crud_sectores.setText(str(product[2]))
                self.vista_EstadioSector.Edit_FilasSector_crud_sectores.setText(str(product[3]))
                self.vista_EstadioSector.Edit_ButacasSector_crud_sectores.setText(str(product[4]))

                x = msg.exec_()
                #habilitar botones y edit excepto filas y butacas
                self.habilitar_editsYbotones()
                global ident_sectorUpdate
                ident_sectorUpdate = product
                return ident_sectorUpdate
    
    def calcular_butacas(self):
        butacas_X_sector = self.vista_EstadioSector.Edit_butacas_X_sector.text()
        filas = self.vista_EstadioSector.Edit_FilasSector_crud_sectores.text()
        try:
            butacas = int(butacas_X_sector)//int(filas)
            self.vista_EstadioSector.Edit_ButacasSector_crud_sectores.setText(str(butacas))
        except:
            print("Ingrese los datos de fila")


    def crearSector(self,identificador,color,precio,fila,butaca,id_estadio):
        sector = self.sector.listar(id_estadio,identificador)
        if sector == None:
            cant_sectores = int(self.vista_EstadioSector.Edit_cant_sectores.text())
            cant_sect_disp = int(self.vista_EstadioSector.Edit_cant_sect_disponibles.text())
            if cant_sect_disp<cant_sectores:
                try:
                    # Intenta convertir el texto del edit a un int
                    id_estadio = self.vista_EstadioSector.Edit_invisible.text()
                    valor_precio = int(self.vista_EstadioSector.Edit_PrecioSector_crud_sectores.text())
                    valor_fila = int(self.vista_EstadioSector.Edit_FilasSector_crud_sectores.text())
                    valor_butaca = int(self.vista_EstadioSector.Edit_ButacasSector_crud_sectores.text())
                    # Si no hay error, el valor es un int
                    if identificador and color and precio and fila and butaca and id_estadio:
                        self.sector.crear(identificador,color,precio,fila,butaca,id_estadio)
                        self.listarSectores()
                    #update
                    cant_anterior = int(self.vista_EstadioSector.Edit_cant_sect_disponibles.text())
                    self.cant_sect_ingr.update(cant_anterior+1,id_estadio)
                    #--
                    cant_Sect_ingr = self.cant_sect_ingr.getCantSectIng(id_estadio) 
                    self.vista_EstadioSector.Edit_cant_sect_disponibles.setText(str(cant_Sect_ingr[1]))
                except:
                     # Si hay error, el valor no es un int
                    msg = QMessageBox()
                    msg.setWindowTitle("ERROR")
                    msg.setText(self.vista_EstadioSector.Edit_nombre_crud_estadio.text())

                    msg.setIcon(QMessageBox.Information) #critical warning and information

                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.setDefaultButton(QMessageBox.Ok)

                    msg.setInformativeText("Debe ingresar los datos correctamente!")
                    x = msg.exec_()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setText(self.vista_EstadioSector.Edit_nombre_crud_estadio.text())

                msg.setIcon(QMessageBox.Information) #critical warning and information

                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)

                msg.setInformativeText("Ya se han ingresado todos los sectores disponibles")
                x = msg.exec_()
        else:
            # Si hay error, el valor no es un int
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText(self.vista_EstadioSector.Edit_nombre_crud_estadio.text())

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("Debe ingresar los datos correctamente!")
            x = msg.exec_()
        
    def actualizar_Sector(self):
        producto = ident_sectorUpdate
        id = self.vista_EstadioSector.Edit_invisible.text()
        sector = []
        fila = []

        ident_Sector = self.vista_EstadioSector.Edit_identSector_crud_sectores.text()
        color = self.vista_EstadioSector.Edit_ColorSector_crud_sectores.text()
        precio = self.vista_EstadioSector.Edit_PrecioSector_crud_sectores.text()
        filas = self.vista_EstadioSector.Edit_FilasSector_crud_sectores.text()
        butacas = self.vista_EstadioSector.Edit_ButacasSector_crud_sectores.text()

       
        if (str(ident_Sector) != None) and (str(color) != None) and (str(precio) != None) and (str(filas) != None) and (str(butacas) != None):
            fila.append(ident_Sector)
            fila.append(color)
            fila.append(precio)
            fila.append(filas)
            fila.append(butacas)
            fila.append(id)
            fila.append(producto[0])
        else:
            print("Ingrese los datos correspondientes")
        if len(fila)>=0:
            sector.append(fila)
        fila = []
        print(sector)
        if len(sector)>=0:
            for stadium in sector:
                self.sector.actualizar(stadium[0],stadium[1],stadium[2],stadium[3],stadium[4],stadium[5],stadium[6])
        self.listarSectores()

    def eliminar_Sector(self):
        nombre_estadio = self.vista_EstadioSector.Edit_identSector_crud_sectores.text()
        cant_sect = int(self.vista_EstadioSector.Edit_cant_sect_disponibles.text())
        act_cant_sect = cant_sect - 1
        id_estadio = self.vista_EstadioSector.Edit_invisible.text()
        sectore_a_eliminar = self.sector.listar(id_estadio,nombre_estadio)
        print("sectore_a_eliminar",sectore_a_eliminar)
        if sectore_a_eliminar:
            if act_cant_sect>0:
                self.cant_sect_ingr.update(act_cant_sect,id_estadio)
                self.vista_EstadioSector.Edit_cant_sect_disponibles.setText(str(act_cant_sect))
            
            
            nombre_sector = sectore_a_eliminar[0]
            buscar_id_sector  = self.sector.buscar_id_sector(id_estadio, nombre_sector)
            print(buscar_id_sector)
            id_sector = buscar_id_sector[0]
            lista_eliminar = self.entradas.validarEliminacionSectores(id_sector)
            if lista_eliminar:
                msg = QMessageBox()
                msg.setWindowTitle("ERROR")
                msg.setText("Sectores No eliminables")

                msg.setIcon(QMessageBox.Information) #critical warning and information

                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)

                msg.setInformativeText("Los sectores no se pueden eliminar debido a que estan registrados por alguna entrada.")
                x = msg.exec_()
            else:
                self.sector.eliminar(id_estadio,nombre_estadio)
                self.resetear_valores_sectores()
        else:
            # Si hay error, el valor no es un int
            msg = QMessageBox()
            msg.setWindowTitle("ERROR")
            msg.setText(self.vista_EstadioSector.Edit_nombre_crud_estadio.text())

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("No hay Sectores a eliminar.")
            x = msg.exec_()