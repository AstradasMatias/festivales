class Festival():
    def __init__(self,conn):
        self.conn = conn 
        with self.conn.cursor() as cursor:
            sql = """CREATE table if not exists festival(
                    id_festival int primary key auto_increment,
                    codigo_festival varchar(5) unique,
                    nombre varchar(50),
                    id_estadio int,
                    foreign key (id_estadio) references estadio(id_estadio)
                    );"""
            cursor.execute(sql)
            self.conn.commit()

    def crear(self,nombre,id_estadio):
        with self.conn.cursor() as cursor:
            sql = """INSERT INTO festival (nombre,id_estadio)
                     VALUES (%s,%s);"""
            cursor.execute(sql, (nombre,id_estadio))
            self.conn.commit()

    def buscar(self, nombre):
        with self.conn.cursor() as cursor:            
            sql = """ SELECT * FROM festival WHERE nombre = %s"""
            cursor.execute(sql,(nombre)) 
            resultado = cursor.fetchone()
            if resultado:
                return resultado
    
    def listar(self):
        with self.conn.cursor() as cursor:
            sql = """select festival.id_festival, festival.nombre, estadio.nombre 
                     from festival
                     inner join estadio
                     where estadio.id_estadio = festival.id_estadio
                     order by festival.id_festival; """
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        
    def update(self,nombre,id_estadio, id_festival):
        with self.conn.cursor() as cursor:            
            sql = """UPDATE  festival 
                     SET nombre = %s, id_estadio = %s 
                     WHERE id_festival = %s"""
            cursor.execute(sql,(nombre,id_estadio,id_festival)) 
            self.conn.commit()

    def eliminar(self, id_festival):
        with self.conn.cursor() as cursor:            
            sql = """DELETE from festival WHERE id_festival = %s"""
            cursor.execute(sql,(id_festival)) 
            self.conn.commit()

    def entrada_getPrice(self, sector,festival,estadio):
        with self.conn.cursor() as cursor:            
            sql = """ SELECT festival.nombre, estadio.nombre, sectores.ident_sector, 
                      sectores.precio_sector 
                      FROM festival 
                      INNER JOIN estadio on festival.id_estadio = estadio.id_estadio
                      INNER JOIN sectores on estadio.id_estadio = sectores.id_estadio 
                      WHERE sectores.ident_sector = %s AND festival.id_estadio = %s AND estadio.id_estadio = %s """
            cursor.execute(sql,(sector,festival,estadio)) 
            resultado = cursor.fetchone()
            if resultado:
                return resultado

        