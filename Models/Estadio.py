class Estadio():
    def __init__(self,conn):
        self.conn = conn 
        with self.conn.cursor() as cursor:
            sql = """CREATE table if not exists estadio(
                    id_estadio int primary key auto_increment,
                    nombre varchar(40),
                    capacidad_personas int,
                    cantidad_sectores int
                    ); """
            cursor.execute(sql)
            self.conn.commit()

    def listar(self):
        with self.conn.cursor() as cursor:
            sql = """SELECT * FROM estadio; """
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        
    def buscar(self, nombre):
        with self.conn.cursor() as cursor:            
            sql = """ SELECT * FROM estadio WHERE nombre = %s"""
            cursor.execute(sql,(nombre)) 
            resultado = cursor.fetchone()
            if resultado:
                return resultado
            
    def actualizar(self, nombre, capacidad_personas, cantidad_sectores,id_estadio):
        with self.conn.cursor() as cursor:            
            sql = """UPDATE  estadio SET nombre = %s, capacidad_personas = %s, cantidad_sectores = %s WHERE id_estadio = %s"""
            cursor.execute(sql,(nombre,capacidad_personas,cantidad_sectores,id_estadio)) 
            self.conn.commit()

    def eliminar(self, id_estadio):
        with self.conn.cursor() as cursor:            
            sql = """DELETE from estadio WHERE id_estadio = %s"""
            cursor.execute(sql,(id_estadio)) 
            self.conn.commit()

    def crear(self, nombre,capacidad_personas,cantidad_sectores):
        with self.conn.cursor() as cursor:
            sql = """INSERT INTO estadio (nombre, capacidad_personas, cantidad_sectores)
                     VALUES (%s,%s,%s);"""
            cursor.execute(sql, (nombre,capacidad_personas,cantidad_sectores))
            self.conn.commit()

    def buscar_id(self,id_estadio):
        with self.conn.cursor() as cursor:            
            sql = """ SELECT * FROM estadio WHERE id_estadio = %s"""
            cursor.execute(sql,(id_estadio)) 
            resultado = cursor.fetchone()
            if resultado:
                return resultado