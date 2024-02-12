class Entradas():
    def __init__(self,conn):
        self.conn = conn 
        with self.conn.cursor() as cursor:
            sql = """CREATE table if not exists entradas(
                    id_entrada int primary key auto_increment,
                    tipo_entrada varchar(30),
                    precio real,
                    codigo_barras varchar(80) unique,
                    numero_factura varchar(30) unique,
                    id_festival int,
                    id_noche int,
                    id_grupo int,
                    foreign key (id_festival) references festival(id_festival),
                    foreign key (id_noche) references noches(id_noche),
                    foreign key (id_grupo) references grupos_folkloricos(id_grupo)
                    ); """
            cursor.execute(sql)
            self.conn.commit()
    
    def listar(self):
        with self.conn.cursor() as cursor:
            sql = """ SELECT entradas.numero_factura, entradas.precio, festival.nombre,
                      estadio.nombre, noches.noche_numero, grupos_folkloricos.nombre, sectores.ident_sector, entradas.butacas_vendidas, entradas.tipo_entrada
                      FROM entradas
                      INNER JOIN festival
                      ON entradas.id_festival = festival.id_festival
                      INNER JOIN estadio
                      ON entradas.id_estadio = estadio.id_estadio
                      INNER JOIN noches
                      ON entradas.id_noche = noches.id_noche
                      INNER JOIN grupos_folkloricos
                      ON entradas.id_grupo = grupos_folkloricos.id_grupo
                      INNER JOIN sectores
                      ON entradas.id_sector = sectores.id_sector
                      ORDER BY festival.nombre
                  """
            cursor.execute(sql)
            result = cursor.fetchall()
            return result 
    
    def buscar(self,id_festival,id_noche,id_grupo,id_sector,numero_factura):
        with self.conn.cursor() as cursor:
            sql = """ SELECT festival.nombre, noches.noche_numero, grupos_folkloricos.nombre,
                      sectores.ident_sector, entradas.butacas_vendidas, entradas.numero_factura
                      FROM entradas
                      INNER JOIN festival
                      ON entradas.id_festival = festival.id_festival
                      INNER JOIN estadio
                      ON entradas.id_estadio = estadio.id_estadio
                      INNER JOIN noches
                      ON entradas.id_noche = noches.id_noche
                      INNER JOIN grupos_folkloricos
                      ON entradas.id_grupo = grupos_folkloricos.id_grupo
                      INNER JOIN sectores
                      ON entradas.id_sector = sectores.id_sector
                      WHERE entradas.id_festival = %s AND entradas.id_noche = %s AND entradas.id_grupo = %s AND
                      entradas.id_sector = %s AND entradas.numero_factura = %s; 
                  """
            cursor.execute(sql,(id_festival,id_noche,id_grupo,id_sector,numero_factura))
            result = cursor.fetchone()
            return result
        
      
    def insert_Entrada(self,tipo_entrada,precio,numero_factura,butacas_vendidas,id_festival,id_noche,id_grupo,id_estadio,id_sector):
        with self.conn.cursor() as cursor:
            sql = """INSERT INTO entradas (tipo_entrada,precio,numero_factura,butacas_vendidas,id_festival,id_noche,id_grupo,id_estadio,id_sector)
                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
            cursor.execute(sql, (tipo_entrada,precio,numero_factura,butacas_vendidas,id_festival,id_noche,id_grupo,id_estadio,id_sector))
            self.conn.commit()

    def verificar_factura(self,numero_factura):
        with self.conn.cursor() as cursor:
            sql = """ SELECT festival.nombre, noches.noche_numero, grupos_folkloricos.nombre,
                      sectores.ident_sector, entradas.butacas_vendidas, entradas.numero_factura
                      FROM entradas
                      INNER JOIN festival
                      ON entradas.id_festival = festival.id_festival
                      INNER JOIN estadio
                      ON entradas.id_estadio = estadio.id_estadio
                      INNER JOIN noches
                      ON entradas.id_noche = noches.id_noche
                      INNER JOIN grupos_folkloricos
                      ON entradas.id_grupo = grupos_folkloricos.id_grupo
                      INNER JOIN sectores
                      ON entradas.id_sector = sectores.id_sector
                      WHERE entradas.numero_factura = %s; 
                  """
            cursor.execute(sql,(numero_factura))
            result = cursor.fetchone()
            return result
        
    def buscar_id(self, cod):
        with self.conn.cursor() as cursor:
            sql = """ SELECT * FROM entradas WHERE entradas.numero_factura = %s ; 
                  """
            cursor.execute(sql,(cod))
            result = cursor.fetchone()
            return result
    def buscar_x_id(self,id_x):
        with self.conn.cursor() as cursor:
            sql = """ SELECT entradas.numero_factura, entradas.precio, festival.nombre,
                      estadio.nombre, noches.noche_numero, grupos_folkloricos.nombre, sectores.ident_sector, entradas.butacas_vendidas, entradas.tipo_entrada
                      FROM entradas
                      INNER JOIN festival
                      ON entradas.id_festival = festival.id_festival
                      INNER JOIN estadio
                      ON entradas.id_estadio = estadio.id_estadio
                      INNER JOIN noches
                      ON entradas.id_noche = noches.id_noche
                      INNER JOIN grupos_folkloricos
                      ON entradas.id_grupo = grupos_folkloricos.id_grupo
                      INNER JOIN sectores
                      ON entradas.id_sector = sectores.id_sector
                      WHERE entradas.id_entrada = %s ; 
                  """
            cursor.execute(sql,(id_x))
            result = cursor.fetchone()
            return result

    def validarEliminacionFestivales(self,cod):
        with self.conn.cursor() as cursor:
            sql = """ SELECT * FROM entradas
                      WHERE entradas.id_festival = %s;
                  """
            cursor.execute(sql,(cod))
            result = cursor.fetchone()
            return result

    def validarEliminacionNoches(self,cod):
        with self.conn.cursor() as cursor:
            sql = """ SELECT * FROM entradas
                      WHERE entradas.id_noche = %s;
                  """
            cursor.execute(sql,(cod))
            result = cursor.fetchone()
            return result
            
    def validarEliminacionSectores(self,cod):
        with self.conn.cursor() as cursor:
            sql = """ SELECT * FROM entradas
                      WHERE entradas.id_sector = %s;
                  """
            cursor.execute(sql,(cod))
            result = cursor.fetchone()
            return result
        
    def validarEliminacionGrupo(self,cod):
        with self.conn.cursor() as cursor:
            sql = """ SELECT * FROM entradas
                      WHERE entradas.id_grupo = %s;
                  """
            cursor.execute(sql,(cod))
            result = cursor.fetchone()
            return result
        