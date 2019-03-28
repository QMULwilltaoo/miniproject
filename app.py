from flask import Flask, request,jsonify
from cassandra.cluster import Cluster

cluster = Cluster(['cassandra'])
session = cluster.connect()
app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name","World")
    return('<h1>Hello, {}!</h1>'.format(name))

@app.route('/spacex/<id>')
def profile(id):
    detail = session.execute( """Select * From spacex.stats where id = {}""".format(id))
    for spacex in detail:
        return('<h1>{} - {} - {} - {} - {}</h1>'.format(spacex.ship_id,spacex.ship_name,spacex.ship_type,spacex.home_port,spacex.active))

    return('<h1>Ship is not found!Pls check the ship list from id 1 to 20!</h1>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)