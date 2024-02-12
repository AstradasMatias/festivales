class Noches():
    def __init__(self,conn):
        self.conn = conn 
        with self.conn.cursor() as cursor:
            sql = """CREATE table if not exists noches(
                    id_noche int primary key auto_increment,
                    cantidad_noches int,
                    noche_numero int,
                    fecha_noche date,
                    hora_inicio time,
                    id_festival int,
                    foreign key (id_festival) references festival(id_festival)
                    ); """
            cursor.execute(sql)
            self.conn.commit()

    def crear(self, cantidad_noches,noche_numero,fecha_noche,hora_inicio,id_festival):
        with self.conn.cursor() as cursor:
            sql = """INSERT INTO noches (cantidad_noches,noche_numero,fecha_noche,hora_inicio,id_festival)
                     VALUES (%s,%s,%s,%s,%s);"""
            cursor.execute(sql, (cantidad_noches,noche_numero,fecha_noche,hora_inicio,id_festival))
            self.conn.commit()

    def listar(self, id_festival):
        with self.conn.cursor() as cursor:
            sql = """select noches.id_noche,noches.cantidad_noches,noches.noche_numero,noches.fecha_noche,
                     noches.hora_inicio 
                     from noches
                     where noches.id_festival = %s;"""
            cursor.execute(sql,id_festival)
            result = cursor.fetchall()
            return result
    
    def consultar_noche_disponible(self, numero_noche,id_festival):
            with self.conn.cursor() as cursor:
                sql = """select noches.id_noche,noches.cantidad_noches,noches.noche_numero,noches.fecha_noche,
                         noches.hora_inicio, noches.id_festival 
                         from noches
                         inner join festival on noches.id_festival = festival.id_festival
                         where noches.noche_numero = %s and noches.id_festival = %s; """
                cursor.execute(sql,(numero_noche, id_festival))
                result = cursor.fetchall()
                return result
            
    def eliminar(self, numero_noche,id_festival):
        with self.conn.cursor() as cursor:            
            sql = """delete from noches
                     where noches.noche_numero = %s and noches.id_festival = %s; """
            cursor.execute(sql,(numero_noche,id_festival)) 
            self.conn.commit()

    def buscar_festival_y_susNoches(self,id_festival):
        with self.conn.cursor() as cursor:
                sql = """select * from noches 
                         inner join festival on noches.id_festival = festival.id_festival
                         where noches.id_festival = %s;"""
                cursor.execute(sql,id_festival)
                result = cursor.fetchall()
                return result
