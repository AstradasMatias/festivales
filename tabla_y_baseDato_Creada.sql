CREATE table festival(
id_festival int primary key auto_increment,
nombre varchar(50),
id_estadio int,
foreign key (id_estadio) references estadio(id_estadio)
);

CREATE table noches(
id_noche int primary key auto_increment,
cantidad_noches int,
noche_numero int,
fecha_noche date,
hora_inicio time,
id_festival int,
foreign key (id_festival) references festival(id_festival)
);

CREATE table grupos_folkloricos(
id_grupo int primary key auto_increment,
nombre varchar(50),
id_reconocimiento int,
foreign key (id_reconocimiento) references reconocimientos(id_reconocimiento)
);

CREATE table reconocimientos(
id_reconocimiento int primary key auto_increment,
tipo_reconocimiento varchar(30)
);

CREATE table presentaciones(
id_presentacion int primary key auto_increment,
horario time,
orden int,
duracion_estimada int,
id_festival int,
id_noche int,
id_grupo int,
foreign key (id_festival) references festival(id_festival),
foreign key (id_noche) references noches(id_noche),
foreign key (id_grupo) references grupos_folkloricos(id_grupo)
);

CREATE table estadio(
id_estadio int primary key auto_increment,
nombre varchar(40) unique,
capacidad_personas int,
cantidad_sectores int
);

CREATE table sectores(
id_sector int primary key auto_increment,
ident_sector varchar(1),
colores varchar(30),
precio_sector int,
filas int,
butacas int,
id_estadio int,
foreign key (id_estadio) references estadio (id_estadio) 
);

CREATE TABLE cant_sect_ingresados(
id_cant_ingre int primary key auto_increment,
cant_sect_ingr int,
id_estadio int,
foreign key (id_estadio) references estadio (id_estadio) 
);

CREATE table entradas(
id_entrada int primary key auto_increment,
tipo_entrada varchar(30),
precio real,
numero_factura varchar(30) unique,
butacas_vendidas int,
id_festival int,
id_noche int,
id_grupo int,
id_estadio int,
id_sector int,
foreign key (id_festival) references festival(id_festival),
foreign key (id_noche) references noches(id_noche),
foreign key (id_grupo) references grupos_folkloricos(id_grupo),
foreign key (id_estadio) references estadio(id_estadio),
foreign key (id_sector) references sectores(id_sector)
);