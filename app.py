from flask import Flask, request,jsonify
from cassandra.cluster import Cluster
# link to cassandra service
cluster = Cluster(['cassandra'])
session = cluster.connect()
app = Flask(__name__)
#hello world paage
@app.route('/')
def hello():
    name = request.args.get("name","World")
    return('<h1>Hello, {}!</h1>'.format(name))
# main function part
# input 'id'(the number of ships) which have value from 1 to 20,for example id=1 means No.1 ship
#the return value is the detail of that ship 
@app.route('/spacex/<id>')
def profile(id):
    # select the ship detail of id
    detail = session.execute( """Select * From spacex.stats where id = {}""".format(id))
    for spacex in detail:
        return jsonify(spacex)

    return('<h1>Ship is not found!Pls check the ship list from id 1 to 20!</h1>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
