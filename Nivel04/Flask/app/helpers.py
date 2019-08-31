from models import Active, Descripcion, Regla
from helperRedis import RedisApp

import json

rdb = RedisApp()


def find_row_active(acountry, acity):
    return Active.query.filter_by(country=acountry).filter_by(city=acity).first()


def find_price(sku):
    return Descripcion.query.filter_by(sku=sku).first()


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
