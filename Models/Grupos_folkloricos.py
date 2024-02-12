class Grupos_folkloricos():
    def __init__(self,conn):
        self.conn = conn 
        with self.conn.cursor() as cursor:
            sql = """CREATE table if not exists grupos_folkloricos(
                    id_grupo int primary key auto_increment,
                    codigo_gruposMusicales varchar(5) unique,
                    nombre varchar(50),
                    id_reconocimiento int,
                    foreign key (id_reconocimiento) references reconocimientos(id_reconocimiento)
                    ); """
            cursor.execute(sql)
            self.conn.commit()

    def buscar(self, nombre):
        with self.conn.cursor() as cursor:            
            sql = """ SELECT * FROM grupos_folkloricos WHERE nombre = %s"""
            cursor.execute(sql,(nombre)) 
            resultado = cursor.fetchone()
            if resultado:
                return resultado
    
    def listar(self):
        with self.conn.cursor() as cursor:
            sql = """select grupos_folkloricos.id_grupo,
                     grupos_folkloricos.nombre, reconocimientos.tipo_reconocimiento 
                     from grupos_folkloricos
                     inner join reconocimientos
                     on grupos_folkloricos.id_reconocimiento = reconocimientos.id_reconocimiento
                     order by grupos_folkloricos.nombre;"""
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    
    def listado_especial(self,nombre):
        with self.conn.cursor() as cursor:
            sql = """select grupos_folkloricos.id_grupo,
                     grupos_folkloricos.nombre, reconocimientos.tipo_reconocimiento 
                     from grupos_folkloricos
                     inner join reconocimientos
                     on grupos_folkloricos.id_reconocimiento = reconocimientos.id_reconocimiento
                     where grupos_folkloricos.nombre = %s;"""
            cursor.execute(sql, nombre)
            result = cursor.fetchall()
            return result

    def crear(self, nombre,id_reconocimiento):
        with self.conn.cursor() as cursor:
            sql = """INSERT INTO grupos_folkloricos (nombre,
                     id_reconocimiento)
                     VALUES (%s,%s);"""
            cursor.execute(sql, (nombre,id_reconocimiento))
            self.conn.commit()
    
    def actualizar(self, nombre,id_reconocimiento,id_nombre):
        with self.conn.cursor() as cursor:
            sql = """UPDATE  grupos_folkloricos SET nombre = %s, 
                     id_reconocimiento = %s WHERE grupos_folkloricos.id_grupo = %s"""
            cursor.execute(sql, (nombre,id_reconocimiento,id_nombre))
            self.conn.commit()
    
    def eliminar(self,id_nombre):
        with self.conn.cursor() as cursor:            
            sql = """DELETE from grupos_folkloricos WHERE id_grupo = %s"""
            cursor.execute(sql,id_nombre) 
            self.conn.commit()

    def verificar_eliminar_reconocimiento(self, cod):
        with self.conn.cursor() as cursor:
            sql = """select * from grupos_folkloricos
                     where grupos_folkloricos.id_reconocimiento = %s"""
            cursor.execute(sql, cod)
            result = cursor.fetchone()
            return result
    