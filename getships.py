from flask import Flask, render_template, request, jsonify
import plotly.graph_objs as go
from plotly.utils import PlotlyJSONEncoder
import json
from pprint import pprint
import requests
import  requests_cache

# Hello word page!
app = Flask(__name__)
@app.route('/')
def hello():
    name = request.args.get("name","World")
    return('<h1>Hello, {}!</h1>'.format(name))

# get the data using RESTful GET method, return in json format in the web page
@app.route('/ships', methods=['GET'])
def spacex():
    # url is the external REST API where we get data 
    url = 'https://api.spacexdata.com/v3/ships'
    resp = requests.get(url)
    if resp.ok:
        ships = resp.json()
        pprint (ships)
        # categories = {categ["ship_id"]:categ["ship_name"] for categ in ships}
    else:
        print(resp.reason)
    ships_a = jsonify(ships)
    return jsonify(ships)


if __name__=="__main__":
    app.run(port=8080, debug=True)
