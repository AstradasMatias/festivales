class Cant_sect_ing():
    def __init__(self,conn):
        self.conn = conn 
        with self.conn.cursor() as cursor:
            sql = """CREATE table if not exists cant_sect_ingresados(
                    id_cant_ingre int primary key auto_increment,
                    cant_sect_ingr int,
                    id_estadio int,
                    foreign key (id_estadio) references estadio (id_estadio) 
                    ); """
            cursor.execute(sql)
            self.conn.commit()

    def getCantSectIng(self, id_estadio):
        with self.conn.cursor() as cursor:            
            sql = """ SELECT * FROM cant_sect_ingresados WHERE id_estadio = %s"""
            cursor.execute(sql,id_estadio) 
            resultado = cursor.fetchone()
            if resultado:
                return resultado
    
        
    def insert_cant_sect(self, cant_sect_ingr, id_estadio):
        with self.conn.cursor() as cursor:
            sql = """INSERT INTO cant_sect_ingresados (cant_sect_ingr, id_estadio)
                     VALUES (%s,%s);"""
            cursor.execute(sql, (cant_sect_ingr,id_estadio))
            self.conn.commit()

    def eliminar(self, id_estadio):
        with self.conn.cursor() as cursor:            
            sql = """DELETE from cant_sect_ingresados WHERE id_estadio = %s"""
            cursor.execute(sql,(id_estadio)) 
            self.conn.commit()

    def update(self,cant_sect_ingr,id_estadio):
        with self.conn.cursor() as cursor:            
            sql = """UPDATE  cant_sect_ingresados SET cant_sect_ingr = %s WHERE id_estadio = %s"""
            cursor.execute(sql,(cant_sect_ingr,id_estadio)) 
            self.conn.commit()

