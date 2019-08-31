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
