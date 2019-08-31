from config import rdb
import json
from flask import escape

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
