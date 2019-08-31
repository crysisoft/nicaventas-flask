from flask import request
from models import Active


def isTupla(app):
    if request.method == 'POST':
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
        with app.app_context():
            datos = Active.query.filter_by(country=acountry).filter_by(city=acity).first()
        if (datos is not None):
            return datos
        else:
            return False
