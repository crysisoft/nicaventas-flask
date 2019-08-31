### Descripción
Esté es un poryecto desarrollado en python con el micro framework FLASK el cual  implementa un la llamada a un endpoint "/active" por el método  [GET] con una respuesta dummy fija tal y como se muestra acontinuación.
```
{
  "active": true,
  "country": "ni",
  "city": "Leon"
}
```
### Inicio del proyecto
Para iniciar el proyecto creamos un directorio llama Nivel1 dentro de este directorio creamos nuestro entorno con el comando `$  virtualenv venv --python=python3.7
` luego activamos el entorno de python con el comando `$ source venv/bin/activate` ahora ya con nuestro entorno activado iniciamos con la instalación de flask con el comando  `$  pip install flask ` 

### Creeación del archivo requirements.txt
Para crear el archivo requirements lo hacemos con el comando 

`$ pip freeze >> requirements.txt  ` 

### Direcctorio de del proyecto


```
Nivel1
	|_ venv
	|
	|_ main.py
	|
	|_ requirements.txt
	|
	|_ readme.md
```

### El archivo main.py
El archivo main.py es nuestra aplicación principal en la cual escribiremos todo nuestro codigo **python** con **flask** 

### Creación de una instancia de flask
Nuestra primer linea de código debe ser la importacion de la flask en nuestro proyecto luego debemos crear una instancia de flask a la cual debemos pasarle como parametro el nombre del archivo.

```
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)
```

### Creando un endpoint 
Para crear un endpoint con python y flask lo hacemos usando un decorador de enrutamiento el cual lo podemos configurar haciendo uso de @app.route y luego entre parentesis colocamos nuestro endpoint dentro de los parentesis tambien podemos colocar el metodo por el cual se accedera a los endpoint pero en este caso no lo usaremos porque por defecto los endpoit creados usan el metodo "GET". Una vez que tenemos definido nuestro endpoint en la linea siguiente demos especificar la función que respondera a la peticiones de los clientes para una mejor ilustración podemos ver las linesas de abajo.


```
@app.route('/active')
def active():
```

### Recibiendo los parametros 
Para recibir los parametros densde la url lo primero que debemos hacer es importas de FLASK un paquete llamado "request" para poder acceder a los parametros lo hacemos de la siguientes manera:

`city = request.args.get('city')`

Donde `city` es una variable, `request` es el paquete de flask y `get` es la funcionalidad que nos permite extraer el valor que nosotros escribamos dentro de los parentesis y comillas en este caso `city`.

### Creación de un diccionario
Para crear un diccionario en python lo hacemos igualando una variable cualquiera y dentro de llaves armamos la estructura que queremos que tenga nuestro diccionario tal y como se muestra en las lineas siguientes:


```
salida = (
        {
            "active": "true",
            "country": country,
            "city": city
        }
    )
```

### Salida en formato Json
Para dar la salida en formato `JSON` debemos importar dos paquetes de flask la primera es `jsonify` que permite converit nuestro diccionario en formato `JSON` y la segunda es `make_response` este otro paquete nos permite debolver rederiado nuestro `JSON` con un estado de la petición 


### Aplicación completa


```
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)


@app.route('/active')
def active():
    city = request.args.get('city')
    country = request.args.get('country')
    salida = (
        {
            "active": "true",
            "country": country,
            "city": city
        }
    )
    return make_response(jsonify(salida), 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000', debug=True)
```

### CURLS a la aplicación 

curl 'http://localhost:8000/active?city=Managua&country=Ni'


### Creación de imagen docker
Para crear una imange de dokcer debemos crear primero un archivo `Dockerfile` en el cual debemos escribir la configuración que tendra nuestra imagen de docker:

En la primer linea escribimos la imagen de la cual va depender nuestra imagen y eso lo hacemos con la palabra reservada `FROM` en nuesro caso la imagen que tomaremos sera una de python, tal y como se muestra en las lineas de abajo.

```
FROM python
```
Despues de esto debemos especificar 

```
FROM python

MAINTAINER Itihell itihell.mejia@gmail.com

COPY Nivel1 /Nivel1
RUN pip install -r /Nivel1/requirements.txt

WORKDIR Nivel1

EXPOSE 8000

CMD ["python", "main.py"]
```
