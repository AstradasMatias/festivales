class Sectores():
    def __init__(self,conn):
        self.conn = conn 
        with self.conn.cursor() as cursor:
            sql = """CREATE table if not exists sectores(
                    id_sector int primary key auto_increment,
                    ident_sector varchar(1),
                    colores varchar(30),
                    precio_sector real,
                    filas int,
                    butacas int,
                    id_estadio int,
                    foreign key (id_estadio) references estadio (id_estadio) 
                    ); """
            cursor.execute(sql)
            self.conn.commit()

    def listar(self,id_estadio,cod_sect):
        with self.conn.cursor() as cursor:
            sql = """SELECT sectores.ident_sector, sectores.colores,
                     sectores.precio_sector, sectores.filas, sectores.butacas 
                     FROM estadio 
                     INNER JOIN sectores on estadio.id_estadio = sectores.id_estadio 
                     WHERE sectores.id_estadio = %s AND sectores.ident_sector = %s"""
            cursor.execute(sql,(id_estadio,cod_sect))
            result = cursor.fetchone()
            return result
        
    def buscar_listar(self, cod):
        with self.conn.cursor() as cursor:         
            sql = """SELECT estadio.nombre, sectores.id_sector, sectores.ident_sector,   
                     sectores.colores,
                     sectores.precio_sector, sectores.filas, sectores.butacas 
                     FROM estadio 
                     INNER JOIN sectores on estadio.id_estadio = sectores.id_estadio 
                     WHERE sectores.id_estadio = %s"""
            cursor.execute(sql, cod) 
            result = cursor.fetchall()
            return result
    
    def crear(self, ident_sector,colores,precio_sector,filas,butacas,id_estadio):
        with self.conn.cursor() as cursor:
            sql = """INSERT INTO sectores (ident_sector, colores, precio_sector,filas,butacas,id_estadio)
                     VALUES (%s,%s,%s,%s,%s,%s);"""
            cursor.execute(sql, (ident_sector,colores,precio_sector,filas,butacas,id_estadio))
            self.conn.commit()

    def actualizar(self, ident_sector,colores,precio_sector,filas,butacas,id_estadio,cod_sect):
        with self.conn.cursor() as cursor:            
            sql = """UPDATE  sectores SET ident_sector = %s, colores = %s, precio_sector = %s, filas = %s, butacas = %s
                     WHERE id_estadio = %s AND sectores.ident_sector = %s"""
            cursor.execute(sql,(ident_sector,colores,precio_sector,filas,butacas,id_estadio,cod_sect)) 
            self.conn.commit()

    def eliminar(self, id_estadio,nombre_estadio):
        with self.conn.cursor() as cursor:            
            sql = """DELETE from sectores WHERE id_estadio = %s AND sectores.ident_sector = %s"""
            cursor.execute(sql,(id_estadio,nombre_estadio)) 
            self.conn.commit()

    def buscar_id_sector(self, id_estadio,cod):
        with self.conn.cursor() as cursor:         
            sql = """SELECT sectores.id_sector 
                     FROM sectores 
                     INNER JOIN estadio on sectores.id_estadio = estadio.id_estadio 
                     WHERE estadio.id_estadio = %s AND sectores.ident_sector = %s"""
            cursor.execute(sql, (id_estadio,cod)) 
            result = cursor.fetchall()
            return result