### Descripción
Esté es un poryecto desarrollado en python con el micro framework FLASK  el cual contiene dos microservicios:

El primero implementa un la llamada a un `endpoint` `"/active"` por el método  [POST] por el puerto 5000 para almacenar en una base de datos y podemos acceder a estos datos almacenados usando el el mismo `endpoint` por el método `[GET]` y tambien podemos acceder al mismo endpoint por el método `[PUT]` para activar o desactivar la disponibilidad de una ciudad y esté método sera validado por una atorización `Authorization: Bearer 2234hj234h2kkjjh42kjj2b20asd6918` tambien implementaresmos un sistema de cache con `REDIS` el cual consistira en agregar la clave cache al resultado tomando el valor `"miss"` si el dato se obtiene de la base de datos y `"hit"` si los datos se obtubieron de la cache.

```
{
  "active": true,
  "city": "Managua",
  "country": "ni",
  "cache": "miss"
}
```

El segundo microservicio se va usar por el puerto 5001 ya que el 5000 esta usado por el primer microservicio e implementa un llamado a un endpoint `/quote` por el método [POST] el cual debe recibir
como parámetro la siguiente estructura:

```
{
  "sku": "AZ00001",
  "country": "ni",
  "city": "León"
}
```

y debe retornar un json de la siguiente manera `sku` es el código de un producto `city` es la ciudad y `country` es el país pero para poder determinar el precio que debe retornar el microservicio debe realizar una consulta a un `api` de terceros donde otendra un valor 
dependiendo del país y la ciudad que enviemos como parámetros y esto se basara en una serie de reglas que tienen registradas en la base de datos para poder determinar la variación de precio que se le puede aplicar a un producto x:

```
{
  "sku": "AZ00001",
  "description": "Paraguas de señora estampado",
  "country": "ni",
  "city": "León",
  "base_price": 10,
  "variation": 1.5
}
```
Tambien debe tener un endpoint `/price/<:sku>` por el método `[GET]` que permita permita visualizar el precio base de un proucto pasandole como parametro por la url el codigo de un producto 
pero debe ser una URL limpia sin paramkeys y nos debe retornar algo como lo siguiente.

```
{
  "cachce": "miss",
  "descripcion": "Paraguas de señora estampado",
  "precio": 10,
  "sku": "AZ00001"
}
```

Este microservicio tambien debe implementar el uso de la cache de redis por loque debemos tener levantado un servicio de redis en paralelo pero la cache debe tener una expiración en 5 minutos que serian 300 segundo en `redis`.

### Soliciar variación de precio
Para revisar la variación de precio  lo hacemos por el endpoint /quote y nos podemos apoyar de CURLs para poder hacer pruebas desde la terminal con el siguiente comando:
```
curl -X POST -d '{"city":"León","country":"ni","sku":"AZ00001"}' -H "Content-Type: application/json" localhost:5001/quote
```
### Solicar el precio base de un producto
Para solicitar el precio base de un producto lo hacemos por el `endpoint`  `/price/AZ00001` por el método `[GET]` y esto lo podemos probar con CURL con la siguiente linea de código en la terminal
```
curl -X GET  http://localhost:5001/price/AZ00001
```
### Enviando datos a la Base de datos
Para hacer una prueba de guardado lo haremos haciendo uso de ` CURL `  el cual nos permitira hacer las peticiones a nuestra aplicación por el puerto `5000` por el método `[POST]` como característica propia de este método vamos a darle la funcionalidad que cuando se grabe un nuevo registro se debe vaciar la `cache` de `redis` y está petición la hacemos de la siguiente manera:
```
curl -X POST -d '{"city":"Managua","country":"ni","active":true}' -H "Content-Type: application/json" localhost:5000/active
```
### Obteniendo datos desde la base de datos
Para obtener datos dede la base de datos lo haeremos con `CURL` con la diferencia que ahora al `endpoint` le enviaremos como parámetros por la `URL` las siguientes keys `[city=Managua,country=ni]` y con CURL lo hacemos de la siguiente manera.
```
curl -X GET 'http://localhost:5000/active?city=Managua&country=ni'
```
### Modificar disponibilidad 
Para modificar las disponibilidad de una ciudad debemos modificar el campo `active` entre `verdad` y `falso` segun sea necesario una vez que modifiquemos una disponibilidad esté debe vaciar la cache existente en la aplicación para evitar que la cache retorno un valor no correcto y esto lo podemos probar con `curl` de la siguiente manera por el puerto 5000.

Recordemos que está peticion debe llevar una autorización `Authorization: Bearer 2234hj234h2kkjjh42kjj2b20asd6918`
```
curl -X PUT -d '{"city":"Managua","country":"ni","active":false}' -H 'Authorization: Bearer 2234hj234h2kkjjh42kjj2b20asd6918'  -H "Content-Type: application/json" localhost:5000/active
```

### Directorio del proyecto
```
app
 |_requirements.txt       * Archivo que contiene las dependencias del proyecto
 |_readme.md   		  * Documentación 
 |_app.py      		  * Aplicación principal del proyecto
 |_config.py		  * Archivo maneja la conexión a la base de datos y la creación de la aplicación
 |_helpers.py		  * Archivo que maneja validaciones de datos y filtro en la base de datos
 |_helperRedis.py.        * Esté archivo lo usaremos para crear una clase que nos permita manipular el comportamiento de REDIS
 |_openwather.py          * Este archivo lo usaremos para crear una clase que nos facilite la comunicación con la api de openwathermap
 |_models.py		  * Archivo que mapea nuestra tabla para poderla usar como un objeto
 |_seed.py	          * Archivo que inserta algunos registro al momento de ejecutar nuestra aplicación	

```

### Requerimientos
Los requerimientos son los paquetes necesarios para que nuestra aplicación funciones bien.
```
Click==7.0
Flask==1.1.1
Flask-SQLAlchemy==2.4.0
itsdangerous==1.1.0
Jinja2==2.10.1
MarkupSafe==1.1.1
psycopg2-binary==2.8.3
SQLAlchemy==1.3.7
redis==3.3.8
Werkzeug==0.15.5
```

### Conexión a la base de datos
Para pode trabajar con una base de datos con python y flask primero debemos solver los driver del manejador de nuestra base de datos para eso hacemso uso del paquete de  `psycopg2-binary==2.8.3` el cual nos permite manejar bases de datos en posgres y para poder mapear nuestra base de datos y trabajarla como si fuese un objeto hacemos uso de otro paquete llamado  `Flask-SQLAlchemy==2.4.0` el cual trabaja como un `ORM` para python habiendo explicado esto ahora podemos trabajar nuestro archivo de configuración llamado `config.py`

Dentro de nuestro archivo config.py lo primero que debemos hacer es importar todos los paquetes que deseamos incluir en nuestro archivo.

Como en está aplicación vamos a usar `REDIS` debemos importalo en nuestro archivo de configuración para poder usarlo en nuestro proyecto.

```
# Importamos el paquete de redes para poder usarlo en nuestra aplicación
import redis
# Importamos FLASK para manejar nuestra aplicación
from flask import Flask

# Importtamos el ORM SQLAlchemy para manajera nuestra base de datos
from flask_sqlalchemy import SQLAlchemy

#Importamos el paquete os para acceder a nuestras variables de entorno
import os
```
Despues de esto debemos hacer una instancia del ORM SQLAlchemy de la siguiente manera.
```
# Creamos una instancia al ORM SQLAlchemy
db = SQLAlchemy()
```

Ahora definimos nuestra clase de configuración la cual va levantar nuestra conexión a la base de datos y creamos una clase llamada `DevelopmentConfig` la cual debe heredar de nuestra clase `Cinfig` y luego esta clase de la pasamos como parametro a nuestra a la configuración de nuestra aplicación
```
#Clase que nos permite configurar nuestra aplicación 
class Config(object):
    DEBUG = True
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_HOST = os.environ.get('DATABASE_HOST')
    DATABASE_NAME = os.environ.get('DATABASE_NAME')
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(DATABASE_USER, DATABASE_PASSWORD,
                                                                DATABASE_HOST, DATABASE_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

```

Dentro de nuestro archivo de configuración tambien escribimos una función la cual al momento de ser invocada creara nuestra aplicación

```
# Función que se encarga de crear nuestra aplicación almomento de ser invocada
def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    return app
```

Ahora debemos hacer una instancia a `redis` que nos permita interactuar con la cache de `REDIS` y para esto vamos a usar una variable `rdb` la cual vamos a igual a redis pasandole como parámetro los datos necesarios para conectarnos al servidor de REDIS tales como `[HOST, NOMBRE DE LA BASE DE DATOS, PUERTO]` y esto lo hacemos de la siguiente manera.

```
rdb = redis.Redis(host=os.environ['REDIS_LOCATION'], port=os.environ['REDIS_PORT'], db=0)
```

### Conexión a openwathermaps
Para interactuar con openwather map cree una archivo llamado openwather.py el contiene una clase que se encarga realizar las peticiones al api
por medio de tres metodos:

`def armar_ruta(self, c, p):` Esté método solo se encarga de establecer la conexión y retornarla.

`def pedir_datos(self, c, p):` Está función se encarga de hacer la petición a openwather y retornarla en formato json.

`def pedir_id(self, c, p):` Está función a diferencia de la anterior se encarga de hacer la petición a openwather pero solo 
retorna el id del clima.

``` 
import os, requests, json
from flask import escape

key = os.environ.get('OPENWATHER_KEY')


class OpenWather():
    url = "http://api.openweathermap.org/data/2.5/weather?q={},{}&APPID={}"

    def armar_ruta(self, c, p):
        return self.url.format(c, p, key)

    def pedir_datos(self, c, p):
        u = self.armar_ruta(c, p)        
        r = requests.get(u, stream=True)
        return r.json()

    def pedir_id(self, c, p):
        u = self.armar_ruta(c, p)        
        r = requests.get(u, stream=True)
        a = r.json()
        id = a['weather'][0]['id']
        return id
```

### Modelos
##### models.py

Los modelos son clases que se encargan de mapear nuestras tablas para interactuar con estas como si fuesen objetos con los que estamos tratando y esto se logra con la ayuda de un `ORM` en nuestro caso con `SQLAlchemy`

Para este ejercicio solo usaremos las clases llamadas `Active`, `Descripcion`, `Regla`  las cuales nos permitiran interactuar con las tablas `actives`, `descripciones` y `reglas` de nuestra base de datos, esto lo confifguramos con el parámetro `__tablename__` igualandolo al nombre de nuestra tabla. Ahora cuando queramos interactuar con nuestras tablas `actives, descripciones, reglas` lo que debemos hacer es importar la instancia de `db` y la clase `Active, Descripcion o Regla` de nuestro archivo de configuración `config.py`

```
class Active(db.Model):
    __tablename__ = "actives"
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    country = db.Column(db.String(2), nullable=False)
    city = db.Column(db.String(30), nullable=False)


class Descripcion(db.Model):
    __tablename__ = "descripciones"
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(7), unique=True, nullable=False)
    descripcion = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)


class Regla(db.Model):
    __tablename__ = "reglas"
    id_regla = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(60), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    sku = db.Column(db.String(50), db.ForeignKey('descripciones.sku'), nullable=False)
    min_condition = db.Column(db.Integer, nullable=False)
    max_condition = db.Column(db.Integer, nullable=False)
    variation = db.Column(db.Float, nullable=False)
```

### Helper para validar datos
##### helpers.py
Para ayudarnos un poco con la validacion de los datos escribimos un helpers que nos ayude a realizar algunas tareas especificas en nuestro caso este helper solo contendra una funcion llamada `isTupla` que recibe como parámetro la instancia de nuestra aplicación para manejar mas a delante el contexto de la aplicacion y comunicarnos con las base de datos tambien  agregamos una función que llamada `find_row_active()` que nos permite hacer busquedas por ciudad y país pasandole estos dos como parámetros  acontinuación detallo el codigo de dicho helpers.

Para que esté trabaje bien se debe importar el `request` de `FLASK` y la clase `Active` de de `models` 

```
Importando los modelos a usar para interactuar con la base de datos
from models import Active, Descripcion, Regla
# Importando la clase RedisApp
from helperRedis import RedisApp
# Importando json para dumpear los diccionariios a formato json
import json
# Creando una instancia a Redis
rdb = RedisApp()

# Función para buscar una disponibilidad de una ciudad pasando como parámetros el país y la ciudad
def find_row_active(acountry, acity):
    return Active.query.filter_by(country=acountry).filter_by(city=acity).first()

# Función que se encarga de buscar el precio base de un producto pasadole como parámetro el código del producto
def find_price(sku):
    return Descripcion.query.filter_by(sku=sku).first()

# Está funcíon se encarga de retornar el precio de un producto y valida si este producto
# esa aun cache lo devuelve de la cache de lo contrario va a la base de datos y hace la petición 
# Nuevamente para extraer los datos crear el diccionario y lo retorna en formato 
# JSON 
def retornar_precio(sku):
    # buscar en redis
    p = rdb.rGet(sku)

    if p:
        return p

    # obtener el precio
    precio = find_price(sku)
    if precio:
        rdb.storePrecio(sku, precio)
        salida = {
            "sku": precio.sku,
            "descripcion": precio.descripcion,
            "precio": precio.precio,
            "cachce": "miss"
        }
        return json.dumps(salida)

# La función calcular_precio se encarga de buscar el precio con variación de precio
# basándose en una serie de reglas definidas en la base de datos en la tabla reglas 
# para poder determinar la variación y recibe como parámetro cuatro valores
# [ciudad, país, código producto, wather id] para poder hacer estas verificaciones

def calcular_precio(c, p, s, id):
    # Buscando en redis
    key = "{}:{}:{}".format(p, c, s)

    k = rdb.rGet(key)
    if k:
        return k

    # buscar en la base de datos
    # filter(Descripcion).filter(Descripcion.sku == Regla.sku)
    datos = Regla.query \
        .join(Descripcion, Descripcion.sku == Regla.sku) \
        .filter(Regla.city == c) \
        .filter(Regla.country == p) \
        .filter(id >= Regla.min_condition) \
        .filter(id <= Regla.max_condition) \
        .filter(Regla.sku == s) \
        .first()

    precios = find_price(s)

    rdb.storeVariacion(key, datos, precios)

    data = {
        "sku": datos.sku,
        "description": precios.descripcion,
        "country": datos.country,
        "city": datos.city,
        "base_price": precios.precio,
        "variation": datos.variation,
        'cache': 'miss'
    }

    return json.dumps(data)
```
### Helpers para Redis
##### helperRedis.py
Dentro del archivo helperRedis.py crearemos una clase que nos permita interactur con la cache de redis, apoyandonos de varios métodos que ayudaran a interactuar con la base de datos dentro de estos métodos tenemos:

`def rSet(self, key, value):` Este método nos permite agregarle un valor a una clave x que deseemos agregar a la cache pasandole dos parámetros la `clave` y el `valor` que tendra la clave, seguidamente le coloca un tiempo de expiración a la clave que se este grabando.

`def rGet(self, key):` Está función nos permite validar si éxiste una clave dentro de la cache y si la clave éxiste la retorna ya escapada de lo contrario retorna falso.

`def validarActive(self, city, country):` Esté método recibe como parámetro la ciudad y el país crea una clave cobinando el país y la ciudad por ejemplo `"ni:Managua"` y busca si existe en la cache de redis.

`def storePrecio(self, key, value):` El método storePrecio recibe dos parámetros la clave y el valor, la función crea un
 diccionario y  agrega dentro de este diccionario la `clave` de `cache:hit`y lo graba dentro de la cache usando el método rSet() de la clase.

`def storeVariacion(self, key, value, value2):` El método storeVariacion recibe tres parámetros la clave, la regla y el producto, la función crea un
 diccionario y  agrega dentro de este diccionario la `clave` de `cache:hit`y lo graba dentro de la cache usando el método rSet() de la clase.

```
entrada = {
            "active": value.active,
            "country": value.country,
            "city": value.city,
            "cache": "hit"
        }
```
`def vaciar_redis(self):` Esté método se encarga como dise su nombre vaciar la cache.

```
# Importando la instancia de REDIS
from config import rdb
Importando JSON para dumpear los diccionarios en formato json
import json
# funcion escape de FLASK para escapar claves en redis
from flask import escape

# Tiempo de expiración de la cache
ttl = 300

class RedisApp(object):

    def rSet(self, key, value):
        # if not rdb.exists(key):
        rdb.set(escape(key), json.dumps(value))
        rdb.expire(key, ttl)

    def rGet(self, key):
        if rdb.exists(key):
            a = rdb.get(escape(key))
            return a
        else:
            return False

    def validarActive(self, city, country):
        key = "{}:{}".format(country, city)
        return self.rGet(key)

    def storePrecio(self, key, value):
        entrada = {
            "sku": value.sku,
            "descripcion": value.descripcion,
            "precio": value.precio,
            "cachce": "hit"
        }
        self.rSet(key, entrada)

    def storeVariacion(self, key, value, value2):
        data = {
            "sku": value.sku,
            "description": value2.descripcion,
            "country": value.country,
            "city": value.city,
            "base_price": value2.precio,
            "variation": value.variation,
            'cache': 'hist'
        }
        self.rSet(key, data)

    def vaciar_redis(self):
        keys = rdb.keys('*')
        for key in keys:
            rdb.delete(key)

```


### Inserción de datos iniciales con SQLAlchemy
#### seeddb.sql
El archivo seeddb.sql contiene una serie comando sql que permiten crear lasta tablas e insertar datos dummy en las tablas para realizar pruebas iniciales con reglas, productos y ciudades 
los detalles del archivo los escribo acontinuación.

``` 

CREATE TABLE "public"."actives" (
  "id" serial,
  "city" varchar(128) COLLATE "pg_catalog"."default",
  "country" varchar(60) COLLATE "pg_catalog"."default" NOT NULL,
  "active" bool,  
  CONSTRAINT "actives_pkey" PRIMARY KEY ("id")
);

CREATE TABLE "public"."descripciones" (
  "id" serial,
  "sku" varchar(7) COLLATE "pg_catalog"."default" NOT NULL,
  "descripcion" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "precio" float8 NOT NULL,
  CONSTRAINT "descripciones_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "descripciones_sku_key" UNIQUE ("sku")
);

CREATE TABLE "public"."reglas" (
  "id_regla" serial,
  "country" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "city" varchar(60) COLLATE "pg_catalog"."default" NOT NULL,
  "sku" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "min_condition" int4 NOT NULL,
  "max_condition" int4 NOT NULL,
  "variation" float8 NOT NULL,
  CONSTRAINT "reglas_pkey" PRIMARY KEY ("id_regla"),
  CONSTRAINT "reglas_sku_fkey" FOREIGN KEY ("sku") REFERENCES "public"."descripciones" ("sku") ON DELETE NO ACTION ON UPDATE NO ACTION
);

INSERT INTO "public"."actives"("city", "active", "country") VALUES ('Nueva Guinea', 't', 'ni');
INSERT INTO "public"."actives"("city", "active", "country") VALUES ('Masaya', 't', 'ni');
INSERT INTO "public"."actives"("city", "active", "country") VALUES ('Esteli', 't', 'ni');
INSERT INTO "public"."actives"("city", "active", "country") VALUES ('León', 't', 'ni');
INSERT INTO "public"."actives"("city", "active", "country") VALUES ('Chinandega', 't', 'ni');
INSERT INTO "public"."actives"("city", "active", "country") VALUES ('Matagalpa', 't', 'ni');
INSERT INTO "public"."actives"("city", "active", "country") VALUES ('Managua', 't', 'ni');
INSERT INTO "public"."actives"("city", "active", "country") VALUES ('Granada', 't', 'ni');


INSERT INTO "public"."descripciones"("sku", "descripcion", "precio") VALUES ('AZ00001', 'Paraguas de señora estampado', 10);
INSERT INTO "public"."descripciones"("sku", "descripcion", "precio") VALUES ('AZ00002', 'Helado de sabor fresa', 1);
INSERT INTO "public"."descripciones"("sku", "descripcion", "precio") VALUES ('AZ00003', 'Sandalia para caballero', 15);
INSERT INTO "public"."descripciones"("sku", "descripcion", "precio") VALUES ('AZ00004', 'Mochila', 12);

INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Esteli', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Esteli', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Esteli', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Esteli', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'El Rama', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'El Rama', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'El Rama', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'El Rama', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'León', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'León', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'León', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'León', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Managua', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Managua', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Managua', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Managua', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Chinandega', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Chinandega', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Chinandega', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Chinandega', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Bluefields', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Bluefields', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Bluefields', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Bluefields', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Nueva Guinea', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Nueva Guinea', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Nueva Guinea', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Nueva Guinea', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Juigalpa', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Juigalpa', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Juigalpa', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Juigalpa', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Rivas', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Rivas', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Rivas', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."reglas"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Rivas', 'AZ00001', 800, 810, 0.5);

```

##### seed.py
Para hacer pruebas iniciales escrimos un archivo seed que se encargue de crear la tabla y llenarla con algunos datos dummys para hacer pruebas. Esté archivo es independiente a nuestra aplicación y se ejecuta cuando iniciamos nuestra aplicación y trabaja solo si la base de datos y las tablas estan vacias, en este archivo se creo un engine para manejar la conexión a la base de datos y mapear nuestras tablas para el proceso de creado de las tablas y se agregaron  dos funciones:

`llenarTabla()` La que se encarga de llenar la tabla con datos dummys 
`create_seed()` Esta funcion debe ser importada desde nuestra aplicación principal e invocada cuando se inicia el programa, esta función se encarga de crear las tablas mapeadas en el archivo `seed.py` y de invocar a la función `llenarTabla()`

```
from sqlalchemy import *
import os
from sqlalchemy.orm import (
    relationship,
    sessionmaker,
    scoped_session)

DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
ruta = "postgresql://{}:{}@{}/{}".format(DATABASE_USER, DATABASE_PASSWORD,
                                         DATABASE_HOST, DATABASE_NAME)

engine = create_engine(ruta)

metadata = MetaData()

actives = Table('actives', metadata,
                Column('id', Integer, primary_key=True),
                Column('active', Boolean),
                Column('country', String(60), nullable=False),
                Column('city', String(50), nullable=False)
                )

descripciones = Table('descripciones', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('sku', String(7), unique=True, nullable=False),
                      Column('descripcion', String(100), nullable=False),
                      Column('precio', Float, nullable=False)
                      )

reglas = Table('reglas', metadata,
               Column('id_regla', Integer, primary_key=True),
               Column('city', String(60), nullable=False),
               Column('country', String(50), nullable=False),
               Column('sku', String(50), ForeignKey('descripciones.sku'), nullable=False),
               Column('min_condition', Integer, nullable=False),
               Column('max_condition', Integer, nullable=False),
               Column('variation', Float, nullable=False),
               )


def create_seed():
    metadata.create_all(engine)
    llenarTabla()


def llenarTabla():
    conn = engine.connect()
    Session = scoped_session(sessionmaker(bind=engine))
    # Tabla de Actives
    q = Session.query(actives).count()
    if q == 0:
        conn.execute(actives.insert(), [
            {'city': 'Nueva Guinea', 'country': 'ni', 'active': True},
            {'city': 'León', 'country': 'ni', 'active': True},
            {'city': 'Managua', 'country': 'ni', 'active': True},
            {'city': 'Masaya', 'country': 'ni', 'active': True}
        ])
    d = Session.query(descripciones).count()
    if d == 0:
        conn.execute(descripciones.insert(), [
            {'sku': 'AZ00001', 'descripcion': 'Paraguas de señora estampado', 'precio': 10},
            {'sku': 'AZ00002', 'descripcion': 'Helado de sabor fresa', 'precio': 1},
        ])
    r = Session.query(reglas).count()
    if r == 0:
        conn.execute(reglas.insert(), [
            {
                'city': 'León',
                'country': 'ni',
                'sku': 'AZ00001',
                'min_condition': 500,
                'max_condition': 599,
                'variation': 1.5
            },
            {
                'city': 'León',
                'country': 'ni',
                'sku': 'AZ00002',
                'min_condition': 500,
                'max_condition': 599,
                'variation': 0.5
            },
            {
                'city': 'León',
                'country': 'ni',
                'sku': 'AZ00002',
                'min_condition': 800,
                'max_condition': 810,
                'variation': 1.5
            },
            {
                'city': 'León',
                'country': 'ni',
                'sku': 'AZ00001',
                'min_condition': 800,
                'max_condition': 810,
                'variation': 0.5
            },
            {
                'city': 'Nueva Guinea',
                'country': 'ni',
                'sku': 'AZ00001',
                'min_condition': 500,
                'max_condition': 599,
                'variation': 1.5
            },
            {
                'city': 'Nueva Guinea',
                'country': 'ni',
                'sku': 'AZ00002',
                'min_condition': 500,
                'max_condition': 599,
                'variation': 0.5
            },
        ])

```


### Aplicación
##### app.py
Nuestra aplicación estara compuesta por dos endpoint uno por el método `[GET]` y con los parametros `[city,country]` para obtener los datos desde la base de datos y otro el método `[POST]`  ambos con la  url `/active`.

#### Dependencias
Para que nuestra aplicación funcione debemos importar algunos componentes de terceros y otros que hemos creado para organizar nuestra aplicación como es el caso de los archivos `seed.py`, `config.py`, `helpers.py` y `models.py` y otros propios de de flask y del lenguage como `os` `request`, `jsonify`, `make_response`

```
import os
from flask import request, jsonify, make_response
from models import Active
from helpers import isTupla
from config import db, create_app
from seed import create_seed
```

#### Endpoint [GET]
El enpoint `/price/<sku>` debe ser accedido por el método `[GET]` con dos parámetros `[sku]` para poder obtener los datos desde la base de datos y para lograr esto creamos una ruta con el decorador `@app.route()` y le pasamos dos parámetros uno es la url y el otro es los métodos por los cuales podia ser accedido esté `endpoint` y luego en la linea de abajo escribimos la función que va ser invicada al momento de llamar aeste endpoint en nuestro caso la función se llama `price()`. 
Dentro de esta función lo primero que hace es llamar a la función que está dentro del archivo `helpers.py` que se encarga de realizar la validación de los datos llamada `retornar_precio()` y le pasamos como parámetro el `sku` en este caso la variable `sku`

``` 
@app.route('/price/<sku>', methods=['GET'])
def price(sku):
    tupla = retornar_precio(sku)
    if (tupla):
        return make_response(jsonify(json.loads(tupla)), 200)
    else:
        salida = {
            "error": True,
            "message": "No se encontro  un registro con esos datos"

        }
    return make_response(jsonify(salida), 403)
```

Podemos probar esté endpoint usando curl para proba hacer una petición get desde la consola:
```
curl -X GET  http://localhost:5001/price/AZ00001
```

#### Endpoint [POST]
El endpoint por [POST] `/quote` recibe los datos por el objeto `request` accediendo a la clave `json` y con la función `get()` y pasandole como parametro le key que `[sku,country,city]` y hacemos una validación al objeto request para determinar el método por el cual se está accediendo al endpoint 

Despues invocamos a la función calcular_precio() de nuestro archivo helpers.py para objter el resultado
de la variación de precio
```
@app.route('/quote', methods=['POST'])
def quote():
    c = request.json.get('city', '')
    p = request.json.get('country', '')
    s = request.json.get('sku', '')
    id = ow.pedir_id(c, p)

    a = calcular_precio(c, p, s, id)

    return make_response(jsonify(json.loads(a)), 200)
```

Podemos hacer una prueba del `endpoint` con `curl` de la siguiente manera:

```
curl -X POST -d '{"city":"León","country":"ni","sku":"AZ00001"}' -H "Content-Type: application/json" localhost:5001/quote
```

### Función que ejecuta nuestra aplicación 
Esta función es invocada desde el punto de entrada de nuestra imagen y se encarga de llamar a las funciones y metodos que crean las tablas y rellenan los datos dentro de la base de datos

```
def runserver():
    create_seed()
    app.app_context().push()
    app.run(host="0.0.0.0", debug=True)
```

### Aplicación completa

```
import os
from flask import request, jsonify, make_response
from config import create_app
from seed import create_seed
from helpers import find_price, calcular_precio, retornar_precio
import json
from helperRedis import RedisApp
from openwather import OpenWather

# 6a9947792be88226610360ddc0b5f041
# http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=6a9947792be88226610360ddc0b5f041

app = create_app()
rdb = RedisApp()
ow = OpenWather()


@app.before_request
def beforRequest():
    pass


@app.errorhandler(404)
def pageNoFound(e):
    salida = {"error": "true", "message": "Página no existe"}
    return make_response(jsonify(salida), 403)


@app.route('/price/<sku>', methods=['GET'])
def price(sku):
    tupla = retornar_precio(sku)
    if (tupla):
        return make_response(jsonify(json.loads(tupla)), 200)
    else:
        salida = {
            "error": True,
            "message": "No se encontro  un registro con esos datos"

        }
    return make_response(jsonify(salida), 403)


@app.route('/quote', methods=['POST'])
def quote():
    c = request.json.get('city', '')
    p = request.json.get('country', '')
    s = request.json.get('sku', '')
    id = ow.pedir_id(c, p)

    a = calcular_precio(c, p, s, id)

    return make_response(jsonify(json.loads(a)), 200)


def runserver():
    create_seed()
    app.app_context().push()
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    runserver()


```

### Dokcer Compose
El archivo docker-compose es el que se encarga de levantar nuestras instancias basadas en las imagenes previa de nuestras aplicaciones y contiene todas  las instrucciones de como deben de comportarse las imagenes.

Dentro del  cdocker-composer podemos configurar las siguientes  paramatros:

Definición de las instancias que va levantar el docker-compose en nuestro caso `nicaventasdb`
```
services:
  nicaventasdb:
```
Nombre de la imagen que utilizaremos para crear nuestro contenedor
`image: postgres:latest`

Para reiniciar nuestro contenedor en caso de error usamos el parámetro `restart:` con un valor de `always` para especificar este comportamiento.
`restart: always`

Encaso que deseemos darle un nombre a nuestro contenedor usamos el parámetro `container_name:` y despues de los dos puntos y netre comillas escrbimos el nombre en nuestro caso `"nicaventasdb"`

```
container_name: "nicaventasdb"
```

Para definir las variables de entorno que usara nuestro contenedor usamos la clave `environment:` luegos asignamos valores a las variables tal y como se muestra a continuación

```
 environment:
      - POSTGRES_DB=nicaventasdbx
      - POSTGRES_USER=postgres      
      - POSTGRES_PASSWORD=postgres 
```

Para exponer un puerto del contenedor con el anfitrión lo hacemos con la clave `ports:` y netre comillas el puerto del anfitrión seguido de dos puntos y el puerto del contenedor.

```
 ports:
      - "54320:5432"
```
Si queremos definir un punto de entrada para nuestras aplicaciones esto lo hacemos con la clave entrypoint: `["python", "app.py","runserver"]` donde `python` es el interprete, `app.py` es el archivo y `runserver` es la función que se ejecutara al levantarse la aplicación

```
entrypoint: ["python", "app.py","runserver"]
```


En nuestro caso para la aplicación estamos levantando cuatro servicios.

`nicaventasdb` Es un contenedor que se levanta a partir de una imagen de postgres.

`nicaventasapp` Es el contenedor del microservicio que sale por el puerto 5000 y que implementa los endpoint de `[GET] /active?city=esteli&country=ni` para ver
la disponibilidad de una ciudad, modifica la disponibilidad con el endpoint `[PUT] /active` que debe recibir una autorización `Authorization: Bearer 2234hj234h2kkjjh42kjj2b20asd6918`
y tiene un endpoint para agregar ciudades por el método `[POST] /active`

`weatherapp` Es el contenedor del microservicio que sale por el puerto 5001 y maneja los endpoint de 
`[POST] /quote` y `[GET] /price/<:sku>` y se conecta a una api externa que determina el clima de la ciudad.

`redis` Es el contenedor que usaremos para levantar el servicio de REDIS pues es una imangen de REDIS



```
version: '3'
services:
  nicaventasdb:
    image: postgres:latest
    restart: always
    container_name: "nicaventasdb"
    environment:
      - POSTGRES_DB=nicaventasdbx
      - POSTGRES_USER=postgres      
      - POSTGRES_PASSWORD=postgres      
    ports:
      - "54320:5432"
    volumes:
      - ./seeddb.sql:/docker-entrypoint-initdb.d/seeddb.sql
  nicaventasapp:
    depends_on:
      - nicaventasdb
    image: itihell/nicaventasapp3:latest
    #image: nicaventasapp2
    restart: always
    container_name: "nicaventasapp"
    ports:
      - "5000:5000"
    environment:
      - WAIT_HOSTS= nicaventasdb:5432
      - REDIS_PORT=6379
      - REDIS_LOCATION=redis
      - FLASK_DEBUG=1s
      - FLASK_APP=app.py
      - BEARER=2234hj234h2kkjjh42kjj2b20asd6918
      - DATABASE_PASSWORD=postgres
      - DATABASE_NAME=nicaventasdbx
      - DATABASE_USER=postgres
      - DATABASE_HOST=nicaventasdb
    entrypoint: ["python", "app.py","runserver"]
  
  weatherapp:
    depends_on:
      - nicaventasdb
    image: itihell/nicaventasapp4:latest
    #image: nicaventasapp2
    restart: always
    container_name: "weatherapp"
    ports:
      - "5001:5000"
    environment:
      - WAIT_HOSTS= nicaventasdb:5432
      - REDIS_PORT=6379
      - REDIS_LOCATION=redis
      - FLASK_DEBUG=1s
      - FLASK_APP=app.py
      - BEARER=2234hj234h2kkjjh42kjj2b20asd6918
      - DATABASE_PASSWORD=postgres
      - DATABASE_NAME=nicaventasdbx
      - DATABASE_USER=postgres
      - DATABASE_HOST=nicaventasdb
      - OPENWATHER_KEY=6a9947792be88226610360ddc0b5f041
    entrypoint: ["python", "app.py","runserver"]

  redis:
    image: redis
    expose:
      - 6379
```



