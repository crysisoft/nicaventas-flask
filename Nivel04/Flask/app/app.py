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
