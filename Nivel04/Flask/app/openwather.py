import os, requests, json
from flask import escape

key = os.environ.get('OPENWATHER_KEY')


class OpenWather():
    url = "http://api.openweathermap.org/data/2.5/weather?q={},{}&APPID={}"

    def armar_ruta(self, c, p):
        return self.url.format(c, p, key)

    def pedir_datos(self, c, p):
        u = self.armar_ruta(c, p)
        print(u)
        r = requests.get(u, stream=True)
        return r.json()

    def pedir_id(self, c, p):
        u = self.armar_ruta(c, p)
        print(u)
        r = requests.get(u, stream=True)
        a = r.json()
        id = a['weather'][0]['id']
        return id
