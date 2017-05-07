#!/usr/bin/env python
#!/Library/Python/2.7/site-packages flask
import os
from flask import Flask, jsonify, request, redirect, send_from_directory, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/css/style.css')
def cssStyle():
	return render_template('/css/style.css')

@app.route('/js/index.js')
def jsIndex():
	return render_template('/js/index.js')


location = None

userData = None

events = [
	{
		'title': 'Barbeque',
		'description': 'It is a Barbeque at this place', 
		'Time': '2:00pm',
		'Duration': '3Hr',
		'Posts': 100
	},
	{
		'title': 'Barbeque',
		'description': 'It is a Barbeque at this place', 
		'Time': '2:00pm',
		'Duration': '3Hr',
		'Posts': 100
	}
]


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
	event = request.args.get('event')
	return jsonify({'events': events}) 
	#replace with the list received

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
