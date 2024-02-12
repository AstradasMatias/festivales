import sys
import os
myDir = os.getcwd()
sys.path.append(myDir)

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from Database.Connection import connection
from Models.Entradas import Entradas
from Models.Presentaciones import Presentaciones
from Models.Festival import Festival
from Models.Estadio import Estadio
from Models.Sectores import Sectores
from Models.Noches import Noches
from Models.Grupos_folkloricos import Grupos_folkloricos
from datetime import timedelta, time


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter 
from reportlab.lib import colors
import webbrowser

from datetime import datetime
from reportlab.pdfgen import canvas
from PyQt5.QtWidgets import QFileDialog
import qrcode
from PIL import Image

class EntradaController():

    def __init__(self, vistaEntrada,c) -> None:
        self.entrada = Entradas(c)
        print("1")
        self.presentacion = Presentaciones(c)
        #print("2")
        self.festival = Festival(c)
        print("3")
        self.estadio = Estadio(c)
        #print("4")
        self.sector = Sectores(c)
        print("5")
        self.noche = Noches(c)
        #print("6")
        self.banda = Grupos_folkloricos(c)
        print("7")
        self.opcion = 0 
        self.vista_entrada = vistaEntrada

    def buscar_X_opcion(self, int):
        self.opcion +=1
        if self.opcion == 1:
            print("soy opcion 1")  
    
    def listar(self):
        table = self.vista_entrada.tableWidget
        entradas = self.entrada.listar()
        table.setRowCount(0)
        for row_number, row_data in enumerate(entradas):
            table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        #limpiar comboBoxes
        self.vista_entrada.comboBox.clear()
        self.vista_entrada.comboBox_2.clear()
        self.vista_entrada.comboBox_2.setEnabled(False)
        self.vista_entrada.comboBox_4.clear()
        self.vista_entrada.comboBox_4.setEnabled(False)
        self.vista_entrada.comboBox_3.clear()
        self.vista_entrada.comboBox_3.setEnabled(False)
        self.vista_entrada.comboBox_5.clear()
        self.vista_entrada.comboBox_5.setEnabled(False)
        self.vista_entrada.comboBox_6.clear()
        self.vista_entrada.comboBox_6.setEnabled(False)
        self.vista_entrada.comboBox_7.setCurrentIndex(-1)
        self.vista_entrada.comboBox_7.setEnabled(False)
        self.vista_entrada.Edit_Invisible.setText("0")
        self.vista_entrada.Edit_precio_entradas_3.setText(" ")
        self.vista_entrada.Edit_precio_entradas_3.setEnabled(False)
        #self.limpiar()
        self.vista_entrada.Button_buscar_entradas.setEnabled(False)
        self.inicializar_comboBox_Festivales()

    def inicializar_comboBox_Festivales(self):
        #Inicializar Festival
        #buscar todos los festivales
        lista_festival = self.festival.listar()
        for rows in lista_festival:
            festival_nombre = str(rows[1])
            print("festival_nombre",festival_nombre)
            self.vista_entrada.comboBox.addItem(festival_nombre)
        self.vista_entrada.comboBox.setCurrentIndex(-1)

    def inicializar_comboBox_Estadios(self,nombre_festival):
        #Inicializar Estadios
        #Traerme el id del festival
        self.vista_entrada.comboBox_2.clear()
        lista_festival = self.festival.buscar(nombre_festival)
        estadio_festival_id = lista_festival[2]
        #buscar todas las Noches que dependen del Festival
        try: #si no hay noches asignadas se lo aviso
            #busco el nombre del estadio
            lista_estadio = self.estadio.buscar_id(estadio_festival_id)
            nombre_estadio = lista_estadio[1]
            self.vista_entrada.comboBox_2.addItem(str(nombre_estadio))
            self.vista_entrada.comboBox_2.setCurrentIndex(-1)
            #Habilito el comboBox_Noches
            self.vista_entrada.comboBox_2.setEnabled(True)
        except:#Si no encuentra le mando un mensaje
            msg = QMessageBox()
            msg.setWindowTitle("ATENCION")
            msg.setText(nombre_festival)

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("No hay estadios asignados a este Festival")
            
            x = msg.exec_()
            #self.limpiar()

    def inicializar_comboBox_Noches(self,nombre_festival):
        #Inicializar Noches
        #Traerme el id del festival
        self.vista_entrada.comboBox_4.clear()
        lista_festival = self.festival.buscar(nombre_festival)
        id_festival = lista_festival[0]
        print(id_festival)
        #buscar todas las Noches que dependen del Festival
        try: #si no hay noches asignadas se lo aviso
            lista_noches = self.noche.buscar_festival_y_susNoches(id_festival)
            #cuantas noches tiene el festival
            cantidad_noches = lista_noches[0][1]
            #creo el combo
            lista_noches_cantidad = []
            i = 1
            if cantidad_noches>0:
                for i in range(cantidad_noches):
                    lista_noches_cantidad.append(i+1)
                for rows in lista_noches_cantidad:
                        self.vista_entrada.comboBox_4.addItem(str(rows))
                self.vista_entrada.comboBox_4.setCurrentIndex(-1)
                #Habilito el comboBox_Noches
                self.vista_entrada.comboBox_4.setEnabled(True)
        except:#Si no encuentra le mando un mensaje
            msg = QMessageBox()
            msg.setWindowTitle("ATENCION")
            msg.setText(nombre_festival)

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("No hay noches asignadas a este festival.")
            
            x = msg.exec_()
            #self.limpiar()

    def inicializar_comboBox_Bandas(self):
        self.vista_entrada.comboBox_3.setEnabled(True)
        self.vista_entrada.comboBox_3.clear()
        lista_banda = self.banda.listar()
        for rows in lista_banda:
            banda_nombre = str(rows[1])
            self.vista_entrada.comboBox_3.addItem(banda_nombre)
        self.vista_entrada.comboBox_3.setCurrentIndex(-1)

    def inicializar_comboBox_Sectores(self,nombre_estadio):
        #Inicializar Noches
        #Traerme el id del festival
        self.vista_entrada.comboBox_5.clear()
        lista_estadio = self.estadio.buscar(nombre_estadio)
        id_estadio = lista_estadio[0]
        #buscar todas las Noches que dependen del Festival
        try: #si no hay noches asignadas se lo aviso
            lista_sectores = self.sector.buscar_listar(id_estadio)
            print(lista_sectores)
            for rows in lista_sectores:
                    self.vista_entrada.comboBox_5.addItem(str(rows[2]))
            self.vista_entrada.comboBox_5.setCurrentIndex(-1)
            #Habilito el comboBox_Noches
            self.vista_entrada.comboBox_5.setEnabled(True)
        except:#Si no encuentra le mando un mensaje
            msg = QMessageBox()
            msg.setWindowTitle("ATENCION")
            msg.setText(nombre_estadio)

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("No hay sectores agregados al estadio.")
            
            x = msg.exec_()
            #self.limpiar()

    def inicializar_comboBox_Butacas(self,nombre_estadio):
        #Inicializar 
        #Traerme el id del festival
        self.vista_entrada.comboBox_6.clear()
        lista_estadio = self.estadio.buscar(nombre_estadio)
        id_estadio = lista_estadio[0]
        #buscar todas las Noches que dependen del Festival
        try: #si no hay noches asignadas se lo aviso
            lista_sectores = self.sector.buscar_listar(id_estadio)
            print("soy la lista sectores de un amigo perdido butaquita",lista_sectores)
            for rows in lista_sectores:
                    self.vista_entrada.comboBox_6.addItem(str(rows[5]))
            self.vista_entrada.comboBox_6.setCurrentIndex(-1)
            #Habilito el comboBox_Noches
            self.vista_entrada.comboBox_6.setEnabled(True)
        except:#Si no encuentra le mando un mensaje
            msg = QMessageBox()
            msg.setWindowTitle("ATENCION")
            msg.setText(nombre_estadio)

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("Surgio un problema, lo solucionaremos a la brevedad.")
            
            x = msg.exec_()
            #self.limpiar()

    def inicializar_comboBox_Tipo_responsable(self):
        #Activar tipo_responsable
        self.vista_entrada.comboBox_7.setEnabled(True)
       
    def inicializar_precio(self, butacas,sector,nombre_estadio,id_festival):

        #---------Me TRAIGO EL Festival
        lista_festival = self.festival.buscar(id_festival)
        estadio_festival_id = lista_festival[0]
        #buscar todas las Noches que dependen del Festival

        

        #busco el id del estadio
        lista_estadio = self.estadio.buscar(nombre_estadio)
        id_estadio = lista_estadio[0]
        
    

        #------------------------------
        #id_festival - nombre del festival
        #nombre_estadio - que pertenece al festival
        #verificar
        lista_verificar = self.festival.entrada_getPrice(sector,estadio_festival_id,id_estadio)
        print("lista_verificar",lista_verificar)

        
        #Selecciono lo que alla en tipo_responsable
        tipo_responsable = self.vista_entrada.comboBox_7.currentText()
        if tipo_responsable == "Mayores":
            precio = 2000
        elif tipo_responsable == "Menores":
            precio = 4000
        elif tipo_responsable == "Jubilados":
            precio = 1000
        elif tipo_responsable == "Estudiantes":
            precio = 1500
        else:
            msg = QMessageBox()
            msg.setWindowTitle("ATENCION")
            msg.setText("nombre_estadio")

            msg.setIcon(QMessageBox.Information) #critical warning and information

            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

            msg.setInformativeText("Ingrese un tipo de responsable")
            
            x = msg.exec_()

        #me traigo el precio del sector
        #Traerme el id del festival
 
        
        #buscar todas las Noches que dependen del Festival
        #si no hay noches asignadas se lo aviso
        lista_sectores = self.sector.buscar_listar(id_estadio)
        print(lista_sectores)
        for rows in lista_sectores:
                if rows[2] == sector:
                    print("soy igual al sector")
                    precio_sector = rows[4]
        print("lista_sectores",lista_sectores)
        print(precio_sector)
        #calculo el precio, precio_depende_tipo + precio_sector
        precio_final_x_butaca = precio_sector + precio
        #lo imprimo en edit precio
        self.vista_entrada.Edit_precio_entradas.setText(str(precio_final_x_butaca))

        #habilito el numero factura
        self.vista_entrada.Edit_precio_entradas_3.setEnabled(True)
        

    def buscar(self,nombre_festival,nombre_estadio,noche_numero,nombre_grupo,ident_sector,butaca,tipo_entrada,precio,numero_factura):
        #buscar id festival

        lista_festival = self.festival.buscar(nombre_festival)
        festival_id = lista_festival[0]
        
        #buscar id de noche
        #buscar todas las Noches que dependen del Festival
    
        lista_noches = self.noche.buscar_festival_y_susNoches(festival_id)
        #cuantas noches tiene el festival
        
        for rows in lista_noches:
            if rows[2] == int(noche_numero):
                id_noche = rows[0]
        
        #buscar id grupo

        lista_grupo = self.banda.buscar(nombre_grupo)
        id_banda = lista_grupo[0]

        #buscar id estadio
        lista_estadio = self.estadio.buscar(nombre_estadio)
        id_estadio = lista_estadio[0]
        #buscar id sector
        #buscar todas las Noches que dependen del Festival
        #si no hay noches asignadas se lo aviso
        lista_sectores = self.sector.buscar_listar(id_estadio)
        for rows in lista_sectores:
                if rows[2] == ident_sector:
                    id_sector = rows[1]
        #tipo, butacas_vendidas, precio, numero_factura
        tipo = tipo_entrada
        precio_final = precio
        factura = numero_factura

        #consulta a la base de datos
        lista_entrada = self.entrada.buscar(festival_id,id_noche,id_banda,id_sector,factura) 
        print("lista_entrada",lista_entrada)


        if lista_entrada == None:
            print("creo")
            self.vista_entrada.Button_generar_ticket.setEnabled(True)
        #me traigo la cantidad de butacas
        else:
            self.vista_entrada.Edit_Invisible.setText(str(lista_entrada[4]))
            butacas_insertadas = self.vista_entrada.Edit_Invisible.text()
            if butacas_insertadas == butaca:

                print("sector lleno")
                self.vista_entrada.Button_generar_ticket.setEnabled(False)
                msg = QMessageBox()
                msg.setWindowTitle("ATENCION")
                msg.setText(nombre_festival)

                msg.setIcon(QMessageBox.Information) #critical warning and information

                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)

                msg.setInformativeText("El sector se encuentra lleno!!!")
                
                x = msg.exec_()
            else:
                factura = self.vista_entrada.Edit_precio_entradas_3.text()
                factura_existente = lista_entrada[5]
                if factura == factura_existente:
                    msg = QMessageBox()
                    msg.setWindowTitle("ATENCION")
                    msg.setText(self.vista_entrada.Edit_precio_entradas_3.text())

                    msg.setIcon(QMessageBox.Information) #critical warning and information

                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.setDefaultButton(QMessageBox.Ok)

                    msg.setInformativeText("Ya existe una factura con ese codigo!!!")
                    
                    x = msg.exec_()
                else:
                    print("creo_aun teniendo algo!")
                    self.vista_entrada.Button_generar_ticket.setEnabled(True)
        #busco en entradas si butacas vendidas = butacas del sector
        #sino butacas_vendidas +1

    def generar_ticket_y_crear(self,nombre_festival,nombre_estadio,noche_numero,nombre_grupo,ident_sector,butaca,tipo_entrada,precio,numero_factura):
        #buscar id festival

        lista_festival = self.festival.buscar(nombre_festival)
        festival_id = lista_festival[0]
        
        #buscar id de noche
        #buscar todas las Noches que dependen del Festival
    
        lista_noches = self.noche.buscar_festival_y_susNoches(festival_id)
        #cuantas noches tiene el festival
        
        for rows in lista_noches:
            if rows[2] == int(noche_numero):
                id_noche = rows[0]
        
        #buscar id grupo

        lista_grupo = self.banda.buscar(nombre_grupo)
        id_banda = lista_grupo[0]

        #buscar id estadio
        lista_estadio = self.estadio.buscar(nombre_estadio)
        id_estadio = lista_estadio[0]
        #buscar id sector
        #buscar todas las Noches que dependen del Festival
        #si no hay noches asignadas se lo aviso
        lista_sectores = self.sector.buscar_listar(id_estadio)
        print("lista_sectores",lista_sectores)
        for rows in lista_sectores:
                if rows[2] == ident_sector:
                    id_sector = rows[1]
        print(id_sector)
        #tipo, butacas_vendidas, precio, numero_factura
        butaca_cant = int(self.vista_entrada.Edit_Invisible.text())
        tipo = tipo_entrada
        precio_final = precio
        factura = self.vista_entrada.Edit_precio_entradas_3.text()
        butaca_cant += 1
        if butaca_cant > int(butaca):
            print("Sector lleno")
        else:

            existe_factura = self.entrada.verificar_factura(factura)
            if existe_factura:
                msg = QMessageBox()
                msg.setWindowTitle("ATENCION")
                msg.setText(self.vista_entrada.Edit_precio_entradas_3.text())

                msg.setIcon(QMessageBox.Information) #critical warning and information

                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)

                msg.setInformativeText("Ya existe una factura con ese codigo!!!")
                
                x = msg.exec_()
            else:
                self.entrada.insert_Entrada(tipo,precio_final,factura,butaca_cant,festival_id,id_noche,id_banda,id_estadio,id_sector)

                #-----------------------------------------
                #-----------------------------------------
                #-----------------------------------------
                lista_entradas = self.entrada.buscar_id(factura)
                #generar el ticket
                id_entrada = lista_entradas[0]
                entrada_data = self.entrada.buscar_x_id(id_entrada)

                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                file_dialog = QFileDialog()
                file_dialog.setOptions(options)
                file_dialog.setDefaultSuffix(".pdf")
                file_dialog.setNameFilter("Archivos PDF (.pdf);;Todos los archivos ()")

                # Obtener la ruta del archivo seleccionada por el usuario
                
                file_path, _ = file_dialog.getSaveFileName(None, "Guardar como", "ticket_pdf.pdf", "Archivos PDF (.pdf);;Todos los archivos ()")

                # Verificar si el usuario ha cancelado la selección
            
                if file_path:
                # Continuar con la generación del PDF usando la ruta seleccionada
                    pdf_file_path = file_path
                #pdf_file_path = "ticket_pdf.pdf"
                
                # Genera codigo qr 

                qr_data = f"Numero Factura: {entrada_data[0]}\nPrecio: {entrada_data[1]}\nFestival: ${entrada_data[2]}\nEstadio: ${entrada_data[3]}\nBanda: ${entrada_data[5]}"
                qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
                qr.add_data(qr_data)
                qr.make(fit=True)
                qr_img = qr.make_image(fill_color="black", back_color="white")
                qr_path = f"codigo_qr_{entrada_data[0]}.png"
                qr_img.save(qr_path)
                bandera = False
                try:
                    open(pdf_file_path, 'wb')
                    bandera = True
                except:
                    print("Ups...")
                
                if bandera == True:
                        
                    with open(pdf_file_path, 'wb') as pdf_file: 
                        c = canvas.Canvas(pdf_file, pagesize=letter)

                        # Establecer el tipo y el tamaño de la fuente
                        c.setFont("Helvetica", 18)

                        # Establecer el color de relleno a rojo oscuro
                        c.setFillColorRGB(0.5, 0, 0)

                        # Escribir el texto en el centro de la posición (250, 750)
                        c.drawCentredString(250, 750, "TICKET - FESTIVAL")

                        # Dibujar una línea divisoria entre el título y los datos
                        c.setLineWidth(4)
                        c.setStrokeColorRGB(0, 0.5, 0)
                        c.line(50, 720, 450, 720)  # Coordenadas: (x1, y1, x2, y2)

                        # Agregar fecha y hora al ticket
                        now = datetime.now()
                        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
                        c.setFont("Helvetica", 12)
                        c.setFillColorRGB(0, 0, 0)
                        c.drawString(250, 727, f"Fecha y Hora: {formatted_date}")

                        # Agregar logo o imagen del festival o la banda musical
                        #c.drawInlineImage("logo.jpg", 458, 285, width=140, height=420)

                        # Agregar rectángulo con color de fondo y bordes redondeados
                        c.setFillColorRGB(0.5, 0.5, 0.5)  # Color de fondo (blanco)
                        c.setStrokeColorRGB(0, 0, 0)  # Color del borde (negro)
                        c.setLineWidth(2)  # Ancho del borde del rectángulo
                        c.roundRect(50, 285, 400, 430, 10, stroke=1, fill=1)  # Rectángulo redondeado (x, y, ancho, alto, radio)

                        # Agregar código QR al ticket
                        c.setFillColorRGB(0.8, 1, 0.8)  # Color de fondo (verde claro)
                        c.roundRect(270, 575, 130, 130, 10, stroke=1, fill=1)  # Rectángulo redondeado (x, y, ancho, alto, radio)
                        c.drawInlineImage(qr_path, 275, 580, width=120, height=120)

                        # Establecer el tipo y el tamaño de la fuente
                        c.setFont("Helvetica", 14)

                        # Coordenadas iniciales de la tabla
                        x = 60
                        y = 680

                        # Agregar contenido al PDF usando los datos de la consulta
                        for label, value in [
                            ("Factura:", entrada_data[0]),
                            ("Precio: $", entrada_data[1]),
                            ("Festival:", entrada_data[2]),
                            ("Estadio:", entrada_data[3]),
                            ("Noche:", entrada_data[4]),
                            ("Banda Musical:", entrada_data[5]),
                            ("Sector:", entrada_data[6]),
                            ("Butacas Totales:", entrada_data[7]),
                            ("Tipo de Entrada:", entrada_data[8])
                        ]:
                            c.drawString(x, y, f"{label} {value}")
                            y -= 28  # Espacio entre lineas

                        # Establecer el tipo y el tamaño de la fuente
                        c.setFont("Helvetica", 16)

                        # Establecer el color de relleno a azul claro total
                        c.setFillColorRGB(0.8, 1, 0.8)

                        # Escribir el texto en la posición (60, 400)
                        c.drawString(60, 400, f"Total: ${entrada_data[1]}")

                        # Guarda y cierra el archivo PDF
                        c.save()
                        # Abre el navegador con el archivo PDF
                        try:
                            webbrowser.open(pdf_file_path)
                        except Exception as e:
                            QMessageBox.information(self, 'Error', f'Error opening PDF: {str(e)}')

