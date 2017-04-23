#!flask/bin/python
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import anttsp


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/tourist_route', methods=['POST'])
def post_route():
	content = request.get_json()
	print("post_route")
	longitude = content['longitude']
	latitude = content['latitude']

	walk_pace = float(content["walk_pace"])
	public_transport_pace = float(content["public_transport_pace"])
	user_trip_time = float(content["user_trip_time"])
	transport_waiting_time = float(content["transport_waiting_time"])
	single_attraction_time = float(content["single_attraction_time"])
	num_iterations = float(content["num_iterations"])
	beta = float(content["beta"])
	alpha = float(content["alpha"])
	Q = float(content["Q"])
	rho = float(content["rho"])
	epsilon = float(content["epsilon"])
	minimal_samples = float(content["minimal_samples"])

	trip_list = anttsp.get_trip(walk_pace, public_transport_pace, user_trip_time, transport_waiting_time, 
		single_attraction_time,
             num_iterations, beta, alpha, Q, rho, epsilon, minimal_samples)
	trip_with_addnotations = []
	for elem in trip_list:
		trip_with_addnotations.append( {'latitude': elem[0][0], 'longitude':elem[0][1], 'description':elem[1]} )

	return jsonify(trip_with_addnotations)

if __name__ == '__main__':
    app.run(debug=True)
