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
