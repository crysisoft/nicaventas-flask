import os
from flask import request, jsonify, make_response
from models import Active
from helpers import isTupla
from config import db, create_app
from seed import create_seed

app = create_app()


@app.before_request
def beforRequest():
    endpoint = request.endpoint
    if endpoint == 'active' and request.method == 'POST':
        tokenValido = "Bearer " + os.environ.get('BEARER')
        tokenEntrante = request.headers.get('Authorization')
        if (tokenEntrante != tokenValido):
            pass
            # salida = {"error": "true", "message": "Petición no valida"}
            # return make_response(jsonify(salida), 403)


@app.errorhandler(404)
def pageNoFound(e):
    salida = {"error": "true", "message": "Página no existe"}
    return make_response(jsonify(salida), 403)


@app.route('/active', methods=['POST', 'GET'])
def active():
    tupla = isTupla(app)
    if request.method == "GET":
        if (tupla):
            salida = {
                "active": tupla.active,
                "country": tupla.country,
                "city": tupla.city
            }
            return make_response(jsonify(salida), 200)
        else:
            salida = {
                "error": True,
                "message": "No se encontro  un registro con esos datos"

            }
            return make_response(jsonify(salida), 200)

    if request.method == 'POST':
        if (tupla):
            datos = Active(
                active=tupla['active'],
                country=tupla['country'],
                city=tupla['city']
            )
            with app.app_context():
                db.session.add(datos)
                db.session.commit()
            salida = {
                "error": True,
                "message": "El registro se grabo con éxito"
            }
        else:
            salida = {
                "error": True,
                "message": "Debe especificar mas parametros"
            }

    return make_response(jsonify(salida), 200)


def runserver():
    create_seed()
    app.app_context().push()
    app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    runserver()
