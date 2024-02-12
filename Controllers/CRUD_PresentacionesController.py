import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from Database.Connection import connection
from Models.Presentaciones import Presentaciones
from Models.Festival import Festival
from Models.Noches import Noches
from Models.Grupos_folkloricos import Grupos_folkloricos
from datetime import timedelta, time



class CRUD_PresentacionesController():

    def __init__(self, vistaPresentaciones,c) -> None:
        self.presentaciones = Presentaciones(c)
        self.festival = Festival(c)
        self.noches = Noches(c)
        self.banda = Grupos_folkloricos(c)
        self.vista_presentaciones = vistaPresentaciones

    def listarPresentaciones(self):
        table = self.vista_presentaciones.tableWidget
        presentaciones = self.presentaciones.listar()
        table.setRowCount(0)
        for row_number, row_data in enumerate(presentaciones):
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        self.vista_presentaciones.comboBox_festival_crud_presentaciones.clear()
        self.limpiar()
        self.inicializar_comboBox_Festivales()

        
        
    def inicializar_comboBox_Festivales(self):
        #Inicializar Festival
        #buscar todos los festivales
        lista_festival = self.festival.listar()
        for rows in lista_festival:
            festival_nombre = str(rows[1])
            print("festival_nombre",festival_nombre)
            self.vista_presentaciones.comboBox_festival_crud_presentaciones.addItem(festival_nombre)
        self.vista_presentaciones.comboBox_festival_crud_presentaciones.setCurrentIndex(-1)

    def inicializar_comboBox_Noches(self,nombre_festival):
        #Inicializar Noches
        #Traerme el id del festival
        self.vista_presentaciones.comboBox_noche_crud_presentaciones_2.clear()
        lista_festival = self.festival.buscar(nombre_festival)
        id_festival = lista_festival[0]
        #buscar todas las Noches que dependen del Festival
        try: #si no hay noches asignadas se lo aviso
            lista_noches = self.noches.buscar_festival_y_susNoches(id_festival)
            #cuantas noches tiene el festival
            cantidad_noches = lista_noches[0][1]
            #creo el combo
            lista_noches_cantidad = []
            i = 1
            if cantidad_noches>0:
                for i in range(cantidad_noches):
                    lista_noches_cantidad.append(i+1)
                for rows in lista_noches_cantidad:
                        self.vista_presentaciones.comboBox_noche_crud_presentaciones_2.addItem(str(rows))
                self.vista_presentaciones.comboBox_noche_crud_presentaciones_2.setCurrentIndex(-1)
                #Habilito el comboBox_Noches
                self.vista_presentaciones.comboBox_noche_crud_presentaciones_2.setEnabled(True)
        except:#Si no encuentra le mando un mensaje
            msg = QMessageBox()
            msg.setWindowTitle("ATENCION")
            msg.setText(nombre_festival)

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("No hay noches asignadas a este festival.")
            
            x = msg.exec_()
            self.limpiar()

    
    def inicializar_comboBox_Bandas(self, noche_numero):
        self.vista_presentaciones.comboBox_banda_crud_presentaciones.clear()
        self.vista_presentaciones.comboBox_banda_crud_presentaciones.setEnabled(True)
        #Inicializar Bandas
        #buscar todos las Bandas
        numero_noche = noche_numero
        self.vista_presentaciones.comboBox_banda_crud_presentaciones.clear()
        lista_banda = self.banda.listar()
        for rows in lista_banda:
            banda_nombre = str(rows[1])
            self.vista_presentaciones.comboBox_banda_crud_presentaciones.addItem(banda_nombre)
        self.vista_presentaciones.comboBox_banda_crud_presentaciones.setCurrentIndex(-1)

    def verificar_ifBandaRepeat(self):
        #me traigo el nombre del festival
        nombre_festival = self.vista_presentaciones.comboBox_festival_crud_presentaciones.currentText()
    
        lista_festival = self.festival.buscar(nombre_festival)
        print("lista_festival",lista_festival)
        id_festival = lista_festival[0]
        print("id_festival",id_festival)

        #me traigo el numero de noche
        num_noche = self.vista_presentaciones.comboBox_noche_crud_presentaciones_2.currentText()
        print("num_noche",num_noche)

        #me traigo el nombre de la banda
        nombre_banda = self.vista_presentaciones.comboBox_banda_crud_presentaciones.currentText()

        #el mas complejo
        lista_noches = self.noches.buscar_festival_y_susNoches(id_festival)
        #cuantas noches tiene el festival
        id_noche = lista_noches[0][0]
        #
        lista_banda = self.banda.buscar(nombre_banda)
        print("nombre_banda",nombre_banda)
        id_banda = lista_banda[0]
        print("id_banda",id_banda)

        #consulto en la base de datos
        lista_presentaciones = self.presentaciones.verificar_banda(id_banda,id_noche,num_noche,id_festival)
        print("lista_presentaciones",lista_presentaciones)
        if len(lista_presentaciones)>0:
            #si me trae algo le mando un mensaje para que no continue y reseteo todo
            msg = QMessageBox()
            msg.setWindowTitle("ATENCION")
            msg.setText(nombre_festival)

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("La banda ya tiene un concierto en la noche seleccionada")
            #self.inicializar_comboBox_Festivales()
            
            x = msg.exec_()
            self.vista_presentaciones.Button_eliminar_crud_presentaciones.setEnabled(True)
            #self.limpiar()
            print("tengo algo, no puedo ingresar")
        else:
            #si no me trae nada (), habilito el resto y voy a chequear los horarios.
            #primero chequeo si el horario esta disponible si es asi, cargo el comboBox
            #Inicializar combo
            try:
                self.vista_presentaciones.comboBox_horario_crud_presentaciones_2.clear()
                
                #hay que generar una lista 
                #si la lista tiene algo es porque existe en presentaciones
                lista_horario = self.presentaciones.get_horario(id_noche,num_noche)
                print("lista_horario",lista_horario)
                try:#si la lista es vacia se rompe, tengo que crearle un horario a esa noche
                    hora = lista_horario[0][1]
                    hora_x = lista_horario[0][1]
                    
                    #Calculo las horas
                    string = str(hora) # Crear un string que representa 2 horas y 30 minutos
                    horas_x, minutos, segundos = map(int, string.split(":")) # Separar el string por los dos puntos y convertir cada parte en un entero
                    
                    duracion_x_show = timedelta(hours=horas_x, minutes=minutos, seconds=segundos) # Crear un objeto timedelta a partir de los argumentos con nombre
                    #
                    print("duracion_x_show",horas_x)
                    #Horario Maximo
                    string = "24:00:00"
                    horas_y, minutos, segundos = map(int, string.split(":"))
                    duracion_final = timedelta(hours=horas_y, minutes=minutos, seconds=segundos)
                    print("duracion_final",horas_y)
                    #
                    i = 0
                    while horas_x<horas_y:
                        horas_x +=2
                        i += 1

                    lista = []
                    string = str(hora)
                    horas, minutos, segundos = map(int, string.split(":"))
                    for rows in range(i):
                        duracion_x_show = timedelta(hours=horas, minutes=minutos, seconds=segundos)
                        lista.append(duracion_x_show)
                        horas +=2
                        print("horas",horas)
                        print("duracion_x_show",duracion_x_show)
                    
                    print(lista)
                    for rows in lista:
                        #Inicializar Bandas
                        #buscar todos las Bandas
                        horario = str(rows)
                        self.vista_presentaciones.comboBox_horario_crud_presentaciones_2.addItem(horario)
                    self.vista_presentaciones.comboBox_horario_crud_presentaciones_2.setCurrentIndex(-1)
                    #----------------
                    
                    self.vista_presentaciones.comboBox_horario_crud_presentaciones_2.setEnabled(True)
                    self.vista_presentaciones.Button_verificarHorario_crud_presentaciones.setEnabled(True)
                    print("ya existo")
                    
                    
                    return lista
                except:#si no existe la lista, puedo agregar laa presentacion
                    lista_horario = self.noches.buscar_festival_y_susNoches(id_festival)
                    print("lista_horario",lista_horario)
                    hora = lista_horario[0][4]
                    hora_x = lista_horario[0][4]
                    
                    #Calculo las horas
                    string = str(hora) # Crear un string que representa 2 horas y 30 minutos
                    horas_x, minutos, segundos = map(int, string.split(":")) # Separar el string por los dos puntos y convertir cada parte en un entero
                    
                    duracion_x_show = timedelta(hours=horas_x, minutes=minutos, seconds=segundos) # Crear un objeto timedelta a partir de los argumentos con nombre
                    #
                    print("duracion_x_show",horas_x)
                    #Horario Maximo
                    string = "24:00:00"
                    horas_y, minutos, segundos = map(int, string.split(":"))
                    duracion_final = timedelta(hours=horas_y, minutes=minutos, seconds=segundos)
                    print("duracion_final",horas_y)
                    #
                    i = 0
                    while horas_x<horas_y:
                        horas_x +=2
                        i += 1

                    lista = []
                    string = str(hora)
                    horas, minutos, segundos = map(int, string.split(":"))
                    for rows in range(i):
                        duracion_x_show = timedelta(hours=horas, minutes=minutos, seconds=segundos)
                        lista.append(duracion_x_show)
                        horas +=2
                        print("horas",horas)
                        print("duracion_x_show",duracion_x_show)
                    
                    print(lista)
                    for rows in lista:
                        #Inicializar Bandas
                        #buscar todos las Bandas
                        horario = str(rows)
                        self.vista_presentaciones.comboBox_horario_crud_presentaciones_2.addItem(horario)
                    self.vista_presentaciones.comboBox_horario_crud_presentaciones_2.setCurrentIndex(-1)
                    #----------------
                    
                    self.vista_presentaciones.comboBox_horario_crud_presentaciones_2.setEnabled(True)
                    self.vista_presentaciones.Button_verificarHorario_crud_presentaciones.setEnabled(True)
                    print("soy nuevo")
                    
                    
                    return lista

            except:
            
                msg = QMessageBox()
                msg.setWindowTitle("ATENCION")
                msg.setText(nombre_festival)

                msg.setIcon(QMessageBox.Information) #critical warning and information

                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)

                msg.setInformativeText("Aun no se han programado las funciones para ese dia/s.")
                
                x = msg.exec_()
                self.limpiar()
    
    def boton_verificar(self):
        try:
            boolean = True
            if boolean:
                horario = self.vista_presentaciones.comboBox_horario_crud_presentaciones_2.currentText()
                lista = self.verificar_ifBandaRepeat()
                boolean = False
            
            count = 0
            for x in lista:
                count +=1 
            
            lista_nueva = []
            for y in range(count):
                lista_nueva += [str(lista[y])]

            i = 1
            for hora in lista_nueva:
                hora_x = str(hora)
                print("Soy la hora en la lista",hora_x)
                if hora_x == horario:
                    posicion = i
                    combo = hora_x
                i += 1
            print(posicion)
            
            self.vista_presentaciones.comboBox_horario_crud_presentaciones_2.setCurrentText(str(combo))
            self.vista_presentaciones.Edit_orden_crud_presentaciones.setText(str(posicion))
            #habilito el crear
            self.vista_presentaciones.Button_crear_crud_presentaciones.setEnabled(True)
        except:
            print("Ingrese los datos")

    def limpiar(self):
        self.vista_presentaciones.comboBox_festival_crud_presentaciones.setCurrentIndex(-1)
        self.vista_presentaciones.comboBox_noche_crud_presentaciones_2.setCurrentIndex(-1)
        self.vista_presentaciones.comboBox_noche_crud_presentaciones_2.setEnabled(False)
        self.vista_presentaciones.comboBox_banda_crud_presentaciones.setCurrentIndex(-1)
        self.vista_presentaciones.comboBox_banda_crud_presentaciones.setEnabled(False)
        self.vista_presentaciones.comboBox_horario_crud_presentaciones_2.setCurrentIndex(-1)
        self.vista_presentaciones.comboBox_horario_crud_presentaciones_2.setEnabled(False)
        self.vista_presentaciones.Edit_orden_crud_presentaciones.setText(" ")

        self.vista_presentaciones.Button_crear_crud_presentaciones.setEnabled(False)
        self.vista_presentaciones.Button_verificarHorario_crud_presentaciones.setEnabled(False)

    def crear_presentacion(self):
        #traerme el nombre del edit
        nombre = self.vista_presentaciones.comboBox_festival_crud_presentaciones.currentText()
        #buscar id del festival
        lista_festival = self.festival.buscar(nombre)
        id_festival = lista_festival[0]
        #traerme el numero de la noche
        noche = self.vista_presentaciones.comboBox_noche_crud_presentaciones_2.currentText()
        lista_noche = self.noches.consultar_noche_disponible(noche,id_festival)
        id_noche = lista_noche[0][0]
        print(lista_noche)
        print(id_noche)
        #buscar la banda
        banda = self.vista_presentaciones.comboBox_banda_crud_presentaciones.currentText()
        lista_banda = self.banda.buscar(banda)
        id_banda = lista_banda[0]
        #traerme el horario
        horario = self.vista_presentaciones.comboBox_horario_crud_presentaciones_2.currentText()
        #traerme el edit de Orden
        orden = self.vista_presentaciones.Edit_orden_crud_presentaciones.text()
        #traerme la duracion estimada
        duracion_estimada = self.vista_presentaciones.comboBox_duracion_crud_presentaciones.currentText()
        #Insertarlo en la base de datos
        #consulto en la base de datos si existe
        lista_x = self.presentaciones.verificar_antes_deInsert(id_banda,id_noche)
        if len(lista_x)==0:
            lista_y = self.presentaciones.verificar_antes_deInsert_2(orden,id_noche)
            if len(lista_y)==0:
                self.presentaciones.crear(horario,int(orden),int(duracion_estimada),id_festival,id_noche,id_banda)
                #listarlo
                self.listarPresentaciones()
                #resetear a valores iniciales
                self.limpiar()
            else:
                msg = QMessageBox()
                msg.setWindowTitle("ATENCION")
                msg.setText(nombre)

                msg.setIcon(QMessageBox.Information) #critical warning and information

                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)

                msg.setInformativeText("Otra banda toca en ese horario :(")
                
                x = msg.exec_()
                #self.listarPresentaciones()
                #self.limpiar()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("ATENCION")
            msg.setText(nombre)

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("Ya hay una presentacion de la banda en ese dia")
            
            x = msg.exec_()
            #self.listarPresentaciones()
            self.vista_presentaciones.Button_eliminar_crud_presentaciones.setEnabled(True)
            #self.limpiar()

    def eliminar(self):
        #traerme el nombre del edit
        nombre = self.vista_presentaciones.comboBox_festival_crud_presentaciones.currentText()
        #buscar id del festival
        lista_festival = self.festival.buscar(nombre)
        id_festival = lista_festival[0]
        #traerme el numero de la noche
        noche = self.vista_presentaciones.comboBox_noche_crud_presentaciones_2.currentText()
        lista_noche = self.noches.consultar_noche_disponible(noche,id_festival)
        id_noche = lista_noche[0][0]
        print(lista_noche)
        print(id_noche)
        #buscar la banda
        banda = self.vista_presentaciones.comboBox_banda_crud_presentaciones.currentText()
        lista_banda = self.banda.buscar(banda)
        id_banda = lista_banda[0]
        lista_a_borrar = self.presentaciones.conocer_id(id_banda,id_noche)
        id_presentacion = lista_a_borrar[0][0]
        self.presentaciones.eliminar(id_presentacion)
        msg = QMessageBox()
        msg.setWindowTitle("ATENCION")
        msg.setText(nombre)

        msg.setIcon(QMessageBox.Information) #critical warning and information

        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)

        msg.setInformativeText("ELIMINASTE LA BANDA en esa Noche")
        
        x = msg.exec_()
        self.listarPresentaciones()
        self.vista_presentaciones.Button_crear_crud_presentaciones.setEnabled(True)
        
        
        