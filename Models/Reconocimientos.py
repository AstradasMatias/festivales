class Reconocimientos():
    def __init__(self,conn):
        self.conn = conn 
        with self.conn.cursor() as cursor:
            sql = """CREATE table if not exists reconocimientos(
                    id_reconocimiento int primary key auto_increment,
                    codigo_reconocimiento varchar(5) unique,
                    tipo_reconocimiento varchar(30)
                    ); """
            cursor.execute(sql)
            self.conn.commit()

    def buscar_id(self, nombre_reconocimientos):
        with self.conn.cursor() as cursor:
            sql = """select  reconocimientos.id_reconocimiento,
                     reconocimientos.tipo_reconocimiento 
                     from reconocimientos
                     where reconocimientos.tipo_reconocimiento = %s;"""
            cursor.execute(sql,nombre_reconocimientos)
            result = cursor.fetchall()
            return result
        
    def buscar_datoFull(self, id_reconocimientos):
        with self.conn.cursor() as cursor:
            sql = """select reconocimientos.tipo_reconocimiento 
                     from reconocimientos
                     where reconocimientos.id_reconocimiento = %s;"""
            cursor.execute(sql,id_reconocimientos)
            result = cursor.fetchall()
            return result
        
    def crear(self, tipo):
        with self.conn.cursor() as cursor:
            sql = """INSERT INTO reconocimientos (tipo_reconocimiento) VALUES (%s);"""
            cursor.execute(sql, tipo)
            self.conn.commit()

    def eliminar(self, tipo):
        with self.conn.cursor() as cursor:            
            sql = """delete from reconocimientos
                     where reconocimientos.tipo_reconocimiento = %s; """
            cursor.execute(sql,tipo) 
            self.conn.commit()

    def listar(self):
        with self.conn.cursor() as cursor:
            sql = """select * from reconocimientos
                     order by reconocimientos.id_reconocimiento;"""
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    
    def listar_x(self, nombre):
        with self.conn.cursor() as cursor:
            sql = """select * from reconocimientos
                     where reconocimientos.tipo_reconocimiento = %s;"""
            cursor.execute(sql, nombre)
            result = cursor.fetchall()
            return result