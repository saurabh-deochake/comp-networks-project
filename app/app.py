#!/usr/bin/env python
#!/Library/Python/2.7/site-packages flask
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

location = None

userData = None

events = [
	{
		'title': 'Barbeque',
		'description': 'It is a Barbeque at this place', 
		'Time': '2:00pm',
		'Duration': '3Hr',
		'Address': '255 hamilton street, new brunswick, nj'
	},
	{
		'title': 'Barbeque',
		'description': 'It is a Barbeque at this place', 
		'started': '2:00pm',
		'duration': '3Hr',
		'address': '255 hamilton street, new brunswick, nj'
	}
]

friends = [
	{
		'name':'Risham Chokshi',
		'event_name': 'Barbeque',
		'event_started': '2:00pm',
		'event_ending': '3Hr',
		'event_address': '255 hamilton street, new brunswick, nj',
		'person_leaving': '3Hr',
		'person_picture': 'http//www.google.com'
	},
	{
		'name':'Saurabh Deochake',
		'event_name': 'Barbeque',
		'event_started': '2:00pm',
		'event_ending': '3Hr',
		'event_address': '255 hamilton street, new brunswick, nj',
		'person_leaving': '3Hr',
		'person_picture': 'http//www.google.com'
	}

]

heatmap = {
	'Events': [{
		'name': 'Barbeque',
		'Posts': 100
	},
	{
		'name': 'Barbeque',
		'Posts': 20
	},
	{
		'name': 'Barbeque',
		'Posts': 25
	},
	{
		'name': 'Barbeque',
		'Posts': 100
	},
	{
		'name': 'Barbeque',
		'Posts': 75
	}],
	'max': 100
}


#get list of events using FB api
@app.route('/event_list', methods=['GET'])
def get_events():
	location = request.args.get('location')
	print(location)
	return jsonify({'events': events}) 
	#replace by list of events and all details with number of tweets

#get list of friends still at a particular event, name will be given
@app.route('/friend_list', methods=['GET'])
def get_tasks():
	return jsonify({'friends': friends}) 
	#replace with the list received

#heat map based on an event passing event and popularity
@app.route('/heatmap', methods=['GET'])
def get_heatmap():
	return jsonify(heatmap) 

#will give you credentials for the user
@app.route('/login', methods=['GET', 'OPTIONS'])
#@crossdomain(origin='*')
def post_login():
	TuserId = request.args.get('TuserId')
	FuserId = request.args.get('FuserId')
	IuserId = request.args.get('IuserId')
	print(TuserId)
	userData = {
		'instagram': IuserId,
        'facebook': FuserId,
        'twitter': TuserId
	}
	return "Welcome!"

if __name__ == '__main__':
	app.run(debug=True)
