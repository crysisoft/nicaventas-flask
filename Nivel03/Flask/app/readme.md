### Descripción
Esté es un poryecto desarrollado en python con el micro framework FLASK el cual  implementa un la llamada a un `endpoint` `"/active"` por el método  [POST] para almacenar en una base de datos y podemos acceder a estos datos almacenados usando el el mismo `endpoint` por el método `[GET]` y tambien podemos acceder al mismo endpoint por el método `[PUT]` para activar o desactivar la disponibilidad de una ciudad y esté método sera validado por una atorización `Authorization: Bearer 2234hj234h2kkjjh42kjj2b20asd6918` tambien implementaresmos un sistema de cache con `REDIS` el cual consistira en agregar la clave cache al resultado tomando el valor `"miss"` si el dato se obtiene de la base de datos y `"hit"` si los datos se obtubieron de la cache.

```
{
  "active": true,
  "city": "Managua",
  "country": "ni",
  "cache": "miss"
}
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

### Modelos
##### models.py

Los modelos son clases que se encargan de mapear nuestras tablas para interactuar con estas como si fuesen objetos con los que estamos tratando y esto se logra con la ayuda de un `ORM` en nuestro caso con `SQLAlchemy`

Para este ejercicio solo usaremos una clase llamada Active la cual nos permitira interactuar con la tabla actives de nuestra base de datos esto lo confifguramos con el parámetro `__tablename__` igualandolo al nombre de nuestra tabla. Ahora cuando queramos interactuar con nuestra tabla `actives` lo que debemos importar es la instancia de `db` y la clase `Active` de nuestro archivo de configuración `config.py`

```
from config import db


class Active(db.Model):
    __tablename__ = "actives"
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean)
    country = db.Column(db.String(2), nullable=False)
    city = db.Column(db.String(30), nullable=False)
```

### Helper para validar datos
##### helpers.py
Para ayudarnos un poco con la validacion de los datos escribimos un helpers que nos ayude a realizar algunas tareas especificas en nuestro caso este helper solo contendra una funcion llamada `isTupla` que recibe como parámetro la instancia de nuestra aplicación para manejar mas a delante el contexto de la aplicacion y comunicarnos con las base de datos tambien  agregamos una función que llamada `find_row_active()` que nos permite hacer busquedas por ciudad y país pasandole estos dos como parámetros  acontinuación detallo el codigo de dicho helpers.

Para que esté trabaje bien se debe importar el `request` de `FLASK` y la clase `Active` de de `models` 

```
from flask import request, escape
from models import Active
from helperRedis import RedisApp
import json

rdb = RedisApp()

# Función para validad el método y la busqueda de los datos
def isTupla(app):
    if request.method == 'POST' or request.method == "PUT":
        datos = {
            "city": request.json.get('city', ''),
            "country": request.json.get('country', ''),
            "active": request.json.get('active', False),
        }

        if (datos['city'] and datos['country']):
            return datos
        else:
            return False

    elif request.method == "GET":
		# Obteniendo los parámetros enviados por la URL
        acity = request.args.get('city', '')
        acountry = request.args.get('country', '')
		# Buscando datos si existen en cache
        r = rdb.validarActive(acity, acountry)
		# Si los datos existen en cache entonces que los retorne de la cache
        if r:
            return r
		# Contexto de la aplicacación
        with app.app_context():
			# Obteniendo datos de la base de datos
            datos = find_row_active(acountry,acity)
		# Si los datos fueron encontrados en la base de datos entoces 
        if (datos is not None):
			# Grabamos los datos en la cache para futuras buscaquedas
            rdb.storActive(acity, acountry, datos)
			# Creando un diccionario para dar la salida solicitada
            entrada = {
                "active": datos.active,
                "country": datos.country,
                "city": datos.city,
                "cache": "miss"
            }
			#Retornando la salida en formato json
            return json.dumps(entrada)
        else:
			# Si la busqueda no encotro nada que retorne falso
            return False

# Función para buscar una ciudad por país y ciudad.
def find_row_active(acountry, acity):
    return Active.query.filter_by(country=acountry).filter_by(city=acity).first()

```
### Helpers para Redis
##### helperRedis.py
Dentro del archivo helperRedis.py crearemos una clase que nos permita interactur con la cache de redis, apoyandonos de varios métodos ayudaran a interactuar con la base de datos dentro de estos métodos tenemos:

`def rSet(self, key, value):` Este método nos permite agregarle un valor a una clave x que deseemos agregar a la cache pasandole dos parámetros la `clave` y el `valor` que tendra la clave.

`def rGet(self, key):` Está función nos permite validar si éxiste una clave dentro de la cache y si la clave éxiste la retorna ya escapada de lo contrario retorna falso.

`def validarActive(self, city, country):` Esté método recibe como parámetro la ciudad y el país crea una clave cobinando el país y la ciudad por ejemplo `"ni:Managua"` y busca si existe en la cache de redis.

`def storActive(self, city, country, value):` El método storeActive recibe tres parámetros la ciudad, el país y el valor y tiene como funcionalidad crear un key combinando el país y la ciudad, crea un diccionario con con los valores recibidos y agrega dentro de este diccionario la `clave` de `cache:hit`y lo graba dentro de la cache usando el método rSet() de la clase.

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
from config import rdb
import json
from flask import escape


class RedisApp(object):

    def rSet(self, key, value):
        # if not rdb.exists(key):
        rdb.set(escape(key), json.dumps(value))

    def rGet(self, key):
        if rdb.exists(key):
            a = rdb.get(escape(key))
            return a
        else:
            return False

    def validarActive(self, city, country):
        key = "{}:{}".format(country, city)
        return self.rGet(key)

    def storActive(self, city, country, value):
        key = "{}:{}".format(country, city)
        entrada = {
            "active": value.active,
            "country": value.country,
            "city": value.city,
            "cache": "hit"
        }
        self.rSet(key, entrada)

    def vaciar_redis(self):
        keys = rdb.keys('*')
        for key in keys:
            rdb.delete(key)
```


### Inserción de datos iniciales con SQLAlchemy
##### seed.py
Para hacer pruebas iniciales escrimos un archivo seed que se encargue se encarga que crear la tabla y llenarla con algunos datos dummys para hacer pruebas. Esté archivo es independiente a nuestra aplicación y se ejecuta cuando iniciamos nuestra aplicación y trabaja solo si la base de datos y las tablas estan vacias, en este archivo se creo un engine para manejar la conexión a la base de datos y mapear nuestras tablas para el proceso de creado de las tablas y se agregaron  dos funciones:

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


def create_seed():
    metadata.create_all(engine)
    llenarTabla()


def llenarTabla():
    conn = engine.connect()
    Session = scoped_session(sessionmaker(bind=engine))
    q = Session.query(actives).count()
    if q == 0:
        conn.execute(actives.insert(), [
            {'city': 'Nueva Guinea', 'country': 'Ni', 'active': True},
            {'city': 'León', 'country': 'Ni', 'active': True},
            {'city': 'Managua', 'country': 'Ni', 'active': True},
            {'city': 'Masaya', 'country': 'Ni', 'active': True}
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
El enpoint `/active` debe ser accedido por el método `[GET]` con dos parámetros `[city,country]` para poder obtener los datos desde la base de datos y para lograr estro creamos una ruta con el decorador `@app.route()` y le pasamos dos parámetros uno es la url y el otro es los métodos por los cuales podia ser accedido esté `endpoint` y luego en la linea de abajo escribimos la función que va ser invicada al momento de llamar aeste endpoint en nuestro caso la función se llama `active()`. Dentro de esta función lo primero que hace es llamar a la función que está dentro del archivo `helpers.py` que se encarga de realizar la validación de los datos llamada `isTupla()` y le pasamos como parámetro la instancia de nuestra aplicación en este caso la variable `app`


```
@app.route('/active', methods=['POST', 'GET','PUT'])
def active():
```

Ahora con condicionales debemos validar el objeto `request` para sabe que tipo de método esta solicitando y luego hacemos otra validación para saber si se encontraron datos que coinsidan y de esa manera dar una respuesta al cliente.

```
    if request.method == "GET":
        tupla = isTupla(app)
        salida = show(tupla)
        return make_response(salida, 200)
```

La función show recibe como parámtreo el valor de la variable tupla y se encarga de retornar el resultado de la busqueda, está función es invocada desde la funcion `active()` cuando se hace una petición por el método `[GET]`.

```
def show(tupla):
    if (tupla):
        return jsonify(json.loads(tupla))
    else:
        salida = {
            "error": True,
            "message": "No se encontro  un registro con esos datos"

        }
    return jsonify(salida)
```

Podemos probar esté endpoint usando curl para proba hacer una petición get desde la consola:
```
curl -X GET 'http://localhost:5000/active?city=Managua&country=ni'
```

#### Endpoint [POST]
El endpoint por [POST] recibe los datos por el objeto `request` accediendo a la clave `json` y con la función `get()` y pasandole como parametro le key que `[city,country,active]` y hacemos una validación al objeto request para determinar el método por el cual se esta accediendo al endpoint 


```
    if request.method == 'POST':
        tupla = isTupla(app)
        return store(tupla)
```

Está función se encarga de realizar una validación de los datos, grabarlos en la base de datos  y vacia los datos existentes en la cache de `REDIS`

```
def store(tupla):
    if (tupla):
		# Validamos si éxiste el registro dentro de la base de datos
        old_row = find_row_active(tupla['country'], tupla['city'])
        if old_row:
            salida = {
                "error": True,
                "message": "El registro ya éxiste"
            }
            return salida
		# Creamos un diccionario con la clase Active para interactuar con la tabla actives de la base de datos
        datos = Active(
            active=tupla['active'],
            country=tupla['country'],
            city=tupla['city']
        )
		# Grabamos los datos dentro de la base de datos
        with app.app_context():
            db.session.add(datos)
            db.session.commit()
		# Eliminamos la cache de REDIS
        rdb.vaciar_redis()
        salida = {
            "error": True,
            "message": "El registro se grabo con éxito"
        }
    else:
        salida = {
            "error": True,
            "message": "Debe especificar mas parametros"
        }
    return salida
```

Podemos hacer una prueba del `endpoint` con `curl` de la siguiente manera:

```
curl -X POST -d '{"city":"Managua","country":"ni","active":true}' -H "Content-Type: application/json" localhost:5000/active
```

#### Endpoint [PUT]
El método put se utilizara solo para cambiar el estado de la disponibilidad de de las ciudades cambiando de verdadero o falso segun los datos enviados por la petición, para hacer esto hacemos una validación del objeto `request` y acceptamos solo las peticiones `[PUT]`, luego llamamos a la función `update()` que recibe como parametro la tupla variable que tiene la validación  de la petición.

```
if request.method == 'PUT':
     tupla = isTupla(app)
     return update(tupla)
```

Función que se encarga de hacer la modificación del estado de la disponibilidad y de la ciudad y vacia la cache de `REDIS` para evitar información incorrecta

```
def update(tupla):
    if (tupla):
        acity = request.json.get('city', '')
        acountry = request.json.get('country', '')
        aactive = request.json.get('active', False)

        old_row = find_row_active(acountry, acity)

        with app.app_context():
            old_row.active = aactive
            db.session.commit()
        rdb.vaciar_redis()
        salida = {
            "error": True,
            "message": "El registro actualizado éxito"
        }
    else:
        salida = {
            "error": True,
            "message": "Debe especificar mas parametros"
        }
    return salida


def runserver():
    create_seed()
    app.app_context().push()
    app.run(host="0.0.0.0", debug=True)
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
from models import Active
from helpers import isTupla, find_row_active
from config import db, create_app
from seed import create_seed
import json
from helperRedis import RedisApp

app = create_app()
rdb = RedisApp()


@app.before_request
def beforRequest():
    endpoint = request.endpoint
    if endpoint == 'active' and request.method == 'PUT':
        tokenValido = "Bearer " + os.environ.get('BEARER')
        tokenEntrante = request.headers.get('Authorization')
        if (tokenEntrante != tokenValido):
            salida = {"error": "true", "message": "Petición no valida"}
            return make_response(jsonify(salida), 403)


@app.errorhandler(404)
def pageNoFound(e):
    salida = {"error": "true", "message": "Página no existe"}
    return make_response(jsonify(salida), 403)


@app.route('/active', methods=['POST', 'GET', 'PUT'])
def active():
    if request.method == "GET":
        tupla = isTupla(app)
        salida = show(tupla)
        return make_response(salida, 200)

    if request.method == 'POST':
        tupla = isTupla(app)
        return store(tupla)

    if request.method == 'PUT':
        tupla = isTupla(app)
        return update(tupla)


def show(tupla):
    if (tupla):
        return jsonify(json.loads(tupla))
    else:
        salida = {
            "error": True,
            "message": "No se encontro  un registro con esos datos"

        }
    return jsonify(salida)


def store(tupla):
    if (tupla):
        old_row = find_row_active(tupla['country'], tupla['city'])
        if old_row:
            salida = {
                "error": True,
                "message": "El registro ya éxiste"
            }
            return salida

        datos = Active(
            active=tupla['active'],
            country=tupla['country'],
            city=tupla['city']
        )
        with app.app_context():
            db.session.add(datos)
            db.session.commit()
        rdb.vaciar_redis()
        salida = {
            "error": True,
            "message": "El registro se grabo con éxito"
        }
    else:
        salida = {
            "error": True,
            "message": "Debe especificar mas parametros"
        }
    return salida


def update(tupla):
    if (tupla):
        acity = request.json.get('city', '')
        acountry = request.json.get('country', '')
        aactive = request.json.get('active', False)

        old_row = find_row_active(acountry, acity)

        with app.app_context():
            old_row.active = aactive
            db.session.commit()
        rdb.vaciar_redis()
        salida = {
            "error": True,
            "message": "El registro actualizado éxito"
        }
    else:
        salida = {
            "error": True,
            "message": "Debe especificar mas parametros"
        }
    return salida


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
  nicaventasapp:
    depends_on:
      - nicaventasdb
    image: itihell/nicaventasapp3:latest
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
  redis:
    image: redis
    expose:
      - 6379

```



