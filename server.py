#!flask/bin/python
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/tourist_route', methods=['POST'])
def post_route():
	content = request.get_json()

	longitude = content['longitude']
	latitude = content['latitude']
	time = content['time']


	#Call service

	return jsonify([{'longitude': longitude+.010, 'latitude':latitude+.010, "time":0},
	 {'longitude':longitude+.10, 'latitude':latitude+.10,  "time":50}, 
	 {'longitude':longitude+.120, 'latitude':latitude+.1123,  "time":20},
	  {'longitude':longitude+.110, 'latitude':latitude+.30,  "time":50},
	  {'longitude':longitude+.610, 'latitude':latitude+.10,  "time":50}

	  ])

if __name__ == '__main__':
    app.run(debug=True)
