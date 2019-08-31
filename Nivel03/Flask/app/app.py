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
