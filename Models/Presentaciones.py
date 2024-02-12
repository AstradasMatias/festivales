class Presentaciones():
    def __init__(self,conn):
        self.conn = conn 
        with self.conn.cursor() as cursor:
            sql = """CREATE table if not exists presentaciones(
                    id_presentacion int primary key auto_increment,
                    codigo_presentaciones varchar(5) unique,
                    horario time,
                    orden int,
                    duracion_estimada int,
                    id_grupo int,
                    foreign key (id_grupo) references grupos_folkloricos(id_grupo)
                    ); """
            cursor.execute(sql)
            self.conn.commit()

    def verificar_banda(self, banda_id, noche_id, noche_num, id_festival):
        with self.conn.cursor() as cursor:
                sql = """select presentaciones.id_festival, presentaciones.id_noche,
                         presentaciones.id_grupo from presentaciones
                         inner join grupos_folkloricos
                         on presentaciones.id_grupo = grupos_folkloricos.id_grupo
                         inner join noches
                         on presentaciones.id_noche = noches.id_noche
                         inner join festival
                         on presentaciones.id_festival = festival.id_festival
                         where grupos_folkloricos.id_grupo = %s and noches.id_noche = %s and noches.noche_numero = %s and festival.id_festival = %s;"""
                cursor.execute(sql,(banda_id, noche_id, noche_num, id_festival))
                result = cursor.fetchall()
                return result
        
    def get_horario(self, noche_id, noche_num):
         with self.conn.cursor() as cursor:
                sql = """select presentaciones.id_noche, noches.hora_inicio, 
                         presentaciones.duracion_estimada, presentaciones.horario 
                         from presentaciones
                         inner join noches
                         on presentaciones.id_noche = noches.id_noche
                         where presentaciones.id_noche = %s and noches.noche_numero = %s; """
                cursor.execute(sql,(noche_id, noche_num))
                result = cursor.fetchall()
                return result
         
    def listar(self):
        with self.conn.cursor() as cursor:
            sql = """SELECT festival.nombre, noches.noche_numero, grupos_folkloricos.nombre,
                     presentaciones.horario, presentaciones.duracion_estimada, presentaciones.orden
                     FROM presentaciones
                     INNER JOIN festival
                     ON presentaciones.id_festival = festival.id_festival
                     INNER JOIN noches
                     ON presentaciones.id_noche = noches.id_noche
                     INNER JOIN grupos_folkloricos
                     ON presentaciones.id_grupo = grupos_folkloricos.id_grupo
                     ORDER BY festival.nombre AND noches.noche_numero;"""
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        
    def crear(self, horario,orden,duracion_estimada,id_festival,id_noche,id_grupo):
        with self.conn.cursor() as cursor:
            sql = """INSERT INTO presentaciones (horario,orden,duracion_estimada,id_festival,
                     id_noche,id_grupo)
                     VALUES (%s,%s,%s,%s,%s,%s);"""
            cursor.execute(sql, (horario,orden,duracion_estimada,id_festival,id_noche,id_grupo))
            self.conn.commit()

    def verificar_antes_deInsert(self,id_grupo,id_noche):
         with self.conn.cursor() as cursor:
            sql = """select * from presentaciones
                     where presentaciones.id_grupo = %s and presentaciones.id_noche = %s;"""
            cursor.execute(sql,(id_grupo,id_noche))
            result = cursor.fetchall()
            return result
    
    def verificar_antes_deInsert_2(self,orden,id_noche):
         with self.conn.cursor() as cursor:
            sql = """select * from presentaciones
                     where presentaciones.orden = %s and presentaciones.id_noche = %s;"""
            cursor.execute(sql,(orden,id_noche))
            result = cursor.fetchall()
            return result
    
    def conocer_id(self,id_grupo,id_noche):
        with self.conn.cursor() as cursor:
            sql = """select presentaciones.id_presentacion from presentaciones
                    where presentaciones.id_grupo = %s and presentaciones.id_noche = %s;"""
            cursor.execute(sql,(id_grupo,id_noche))
            result = cursor.fetchall()
        return result
    
    def eliminar(self,id_presentacion):
        with self.conn.cursor() as cursor:            
            sql = """DELETE from presentaciones WHERE id_presentacion = %s"""
            cursor.execute(sql,id_presentacion) 
            self.conn.commit()
    