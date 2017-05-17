import storage

from flask import Flask
import flask
app = Flask(__name__)
s = storage.Storage()


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/list/')
@app.route('/list/<num>')
def list_entities(num=10):
    num = int(num)
    entities = [i for i in s.get_entities(num)]
    return flask.jsonify(entities)


@app.route('/spot/<lat>/<lng>')
def spot(lat, lng):

    meters = 1000
    coef = meters * 0.0000089
    lat = float(lat)
    lng = float(lng)
    lat_plus = lat + coef
    lat_minu = lat - coef

    lng_plus = lng + coef
    lng_minu = lng - coef
    e = [i for i in s.get_entities(filter_="location_lat lt %s and location_lat gt %s"
                                           "and location_lng lt %s and location_lng gt %s" %
                                           (lat_plus, lat_minu, lng_plus, lng_minu))]
    print(len(e))
    return flask.jsonify(e)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)


