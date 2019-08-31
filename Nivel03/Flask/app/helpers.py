from flask import request, escape
from models import Active
from helperRedis import RedisApp
import json

rdb = RedisApp()


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
        acity = request.args.get('city', '')
        acountry = request.args.get('country', '')

        r = rdb.validarActive(acity, acountry)
        if r:
            return r

        with app.app_context():
            datos = Active.query.filter_by(country=acountry).filter_by(city=acity).first()
        if (datos is not None):
            rdb.storActive(acity, acountry, datos)
            entrada = {
                "active": datos.active,
                "country": datos.country,
                "city": datos.city,
                "cache": "miss"
            }
            return json.dumps(entrada)
        else:
            return False


def find_row_active(acountry, acity):
    return Active.query.filter_by(country=acountry).filter_by(city=acity).first()
