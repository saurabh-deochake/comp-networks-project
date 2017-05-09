#!/usr/bin/env python
#!/Library/Python/2.7/site-packages flask
import os

import facebook
import json
import datetime
import requests
from facebook import GraphAPI # pip install facebook-sdk
from ConfigParser import SafeConfigParser
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from sys import version_info

import geocoder
#from ConfigParser import SafeConfigParser
import time
import __future__
#import logging
import tweepy


from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
global location
CONFIG_FILE = "/etc/api_config"
EVENT_LIMIT = 20
ATTENDING_LIMIT = 200
#location = "Pune"
SELF_ID = "10203154386536494"
MAX_EVENTS = 20

event_ids = []
events = {}
info = {}
events_attending = {}
pass_events = {}
pass_events_names = []
events_name = []
events_info = []
friends = {}
friends_api = {}
heatmap_api = {}
friendslist = []
heatmap = {}
twitter_friends = []
data = {}



userData = None
"""
events = [
	{
		'title': 'Barbeque',
		'description': 'It is a Barbeque at this place', 
		'started': 'Saturday, May 31 12:00PM',
		'duration': '3Hr',
		'address': '255 hamilton street, new brunswick, nj'
	},
	{
		'title': 'Barbeque',
		'description': 'It is a Barbeque at this place', 
		'started': 'Saturday, May 31 12:00PM',
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

"""

#get list of events using FB api

class FacebookGraph:

	def call_api(self, ACCESS_TOKEN):
		return facebook.GraphAPI(ACCESS_TOKEN)

	def fetch_token(self):
		parser = SafeConfigParser()
		parser.read(CONFIG_FILE)
		USER_TOKEN = parser.get('facebook','utoken')
		return USER_TOKEN

	def get_data(self, data_request):
		return json.dumps(data_request, indent=1)

	def get_current_time(self):
		return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

	def get_event_json(self, info):
		for i in info["data"]:
			if "end_time" in i and "place" in i and "name" in i["place"] and "start_time" in i and "description" in i:
				d = {"id": i["id"], "name": i["name"], "description": i["description"],"start_time": i["start_time"], "end_time":i["end_time"], 
		      	     "location":i["place"]["name"]}
			else:
				continue
			events_info.append(d)
	
		events = {"data": events_info}
		return json.dumps(events)
	
	def find_friends_attending(self, events_attending, friends):
		api = {}
		#friendslist = []
		#print events_attending
		for key in events_attending:
			#print key
			
			flag = 0
			obj = fb_call.get_object(key)

			starttime = datetime.datetime.strptime(obj["start_time"][:-5],'%Y-%m-%dT%H:%M:%S')
			endtime = datetime.datetime.strptime(obj["end_time"][:-5],'%Y-%m-%dT%H:%M:%S')
			#print starttime
			for name in events_attending[key]:
				
				if name in friends and starttime>=dnow and endtime>=dnow:
					flag += 1
					
					#print time
					if flag ==1:
						
						print "Friends attending \""+obj["name"]+"\" at "+obj["place"]["name"]+":"			
						d = {"name":obj["name"], "description": obj["description"],"start_time": obj["start_time"], "end_time":obj["end_time"], "location":obj["place"]["name"]}
						pass_events_names.append(d)
					print name + " Picture: "+friends[name]+"\n\n"
					
					api = {"name":name, "event_name": obj["name"], "event_started":str(starttime), "event_ending":str(endtime), "event_address":obj["place"]["name"], "person_leaving":str(endtime), "person_picture":friends[name]}
					friendslist.append(api)	
					#else:
					#	print "None!"
		pass_events = {"data": pass_events_names}
		#friends_api = {"data":friendslist}
		#print friendslist
		return pass_events, friendslist

	def get_taggable_friends(self):
		taggable = fb_call.get_connections(SELF_ID,"taggable_friends",limit=ATTENDING_LIMIT)
		for dictionary in taggable["data"]:
			friends[dictionary["name"]] = dictionary["picture"]["data"]["url"]
		return friends

	def get_event_attendance(self, event_ids):
		for id in event_ids:
			print "Attendance for ", id
			connections = fb_call.get_connections(id, "attending",limit=ATTENDING_LIMIT,fields=[])
			if connections:
				events_name = []
				for name in connections["data"]:
					#print name["name"]
					events_name.append(name["name"])		
				events_attending[id] = events_name
			

		return events_attending

	def create_events_api(self, events_id):
		event = {}
		events = []
		for id in event_ids:
			obj = fb_call.get_object(id)
			starttime = datetime.datetime.strptime(obj["start_time"][:-5],'%Y-%m-%dT%H:%M:%S')
			endtime = datetime.datetime.strptime(obj["end_time"][:-5],'%Y-%m-%dT%H:%M:%S')

			event = {"title":obj["name"], "description":obj["description"], "start_time":str(starttime), "end_time": str(endtime), "address": obj["name"]}
			events.append(event)

		events_api = {"events": events}
		return events_api

	def create_events_heatmap(self, events_attending):
		hm = {}
		heatmap = []
		for id in events_attending:
			obj = fb_call.get_object(id)

			#count = fb_call.get_connections(id, limit=ATTENDING_LIMIT, fields=[attending_count])
			
			count = len(events_attending[id])
			hm = {"name":obj["name"], "Posts":count}
			#hm[obj["name"]] = count
			heatmap.append(hm)
		#print max(heatmap)
		heatmap_api = {"events":heatmap, "max":ATTENDING_LIMIT}
		return heatmap_api
# ------------------------------------------------------------------------------------------------------------------------------#


class Twitter_API:
	# get API instance
	def get_api(self):
		return tweepy.API(auth)#, wait_on_rate_limit=True)

	# call Twitter API
	def call_api(self, friendslist, events):
		try:
			g = []
			api = {}
			print "\n\n\n***** TWITTER  *****"  
			api = self.get_api()
			#query = raw_input("\n\nEnter the location:")
			#event = raw_input("\nEnter the event name:")
			if not len(twitter_friends):
				for friend in tweepy.Cursor(api.friends, count=200).items():
					twitter_friends.append(friend.screen_name)
			print twitter_friends		
		except Exception, e:
			print "Oops! Something went wrong!"
			print "Error Trace: ", e

		### DO IT FOR ALL EVENTS ---------------------------------------------------------#
		### query = event name
		### geocode = lat lang of event location using geocoder
		### ------------------------------------------------------------------------------#
		print events
		for data in events["data"][:MAX_EVENTS]:

			query = data["name"]
			area_location = data["location"]
			geo = geocoder.google(area_location)
			geocode = geo.latlng
			max_tweets = 1000
			searched_tweets = []
			last_id = -1
			obj = fb_call.get_object(data["id"])
			starttime = datetime.datetime.strptime(obj["start_time"][:-5],'%Y-%m-%dT%H:%M:%S')
			endtime = datetime.datetime.strptime(obj["end_time"][:-5],'%Y-%m-%dT%H:%M:%S')
			while len(searched_tweets) < max_tweets:
				count = max_tweets - len(searched_tweets)
				try:
					new_tweets = api.search(q=query, geocode = "%f,%f,%dkm" % (geocode[0], geocode[1], 5),count=count, max_id=str(last_id - 1))
					if not new_tweets:
						break
					searched_tweets.extend(new_tweets)
					last_id = new_tweets[-1].id
				except:
				# depending on TweepError.code, one may want to retry or wait
				# to keep things simple, we will give up on an error
					break

			#print "friends attending ", query
			for status in searched_tweets:
				for name in status.user.screen_name:
					if name in friends:
						print name, status.user.profile_image_url_https.replace("\\","")
						api = {"name":name, "event_name": obj["name"], "event_started":str(starttime), "event_ending":str(endtime), "event_address":obj["place"]["name"], "person_leaving":str(endtime), "person_picture":friends[name]}
						friendslist.append(api)
					else:
						pass
		friends_api = {"friends":friendslist}
		return friends_api
			

	def authenticate(self):
			
		print "Fetching authentication data..."
		parser = SafeConfigParser()
		parser.read(CONFIG_FILE)
		
		ckey = parser.get('twitter','ckey')
		csecret = parser.get('twitter','csecret')
		atoken = parser.get('twitter','atoken')
		asecret = parser.get('twitter','asecret')

		
		return ckey,csecret,atoken, asecret
	
# ------------------------------------------------------------------------------------------------------------------------------#


class Messenger(StreamListener):
		   

	def on_data(self, data):
		try:
			
			#Take out username 
			userName = data.split(',"screen_name":"')[1].split('","location')[0]
			#Take out actual tweet
			tweet = data.split(',"text":"')[1].split('","source')[0]
			
			#Create message in format: @username: <text>
			if userName in friends:
				fetchedTweet = "@"+userName+"-"+tweet
				print fetchedTweet
				time.sleep(5)
				return True
		
		except BaseException, e:
			print 'Failed Ondata,', str(e)
			
			time.sleep(5)
		except KeyboardInterrupt, k:
			print 'Keyboard Interrupt Occured,',str(k)
			
			quit()

	def on_error(self, status):
		print status

### -------------------------------------------------------------------------

@app.route('/event_list', methods=['GET'])
def get_events():
	global location
	location = request.args.get('location')
	print(location)
	print "get events called"
	#location = "Pune"
	#data =fb_call.request("search",{ 'q' : location, 'type' : 'event', 'limit':EVENT_LIMIT, 'since_date'  :   currentTime}) #'limit' ,before since_date
	data = get_fb_data(location)
	print data
	# fb.get_data already returns us output in json format
	info = json.loads(fb.get_data(data))
	events = json.loads(fb.get_event_json(info))

	print "Events - ", events
	for event in events["data"]:
		event_ids.append(event["id"])

	events_api = fb.create_events_api(event_ids)

	#run_app()
	return jsonify(events_api) 
	#replace by list of events and all details with number of tweets

#get list of friends still at a particular event, name will be given
@app.route('/friend_list', methods=['GET'])
def get_tasks():
	#location = request.args.get('location')
	print(location)
	print "get events called"
	#location = "Pune"

	info = get_fb_data(location)
	#info = json.loads(fb.get_data(data))
	events = json.loads(fb.get_event_json(info))
	friends = fb.get_taggable_friends()
	#print "Events - ", events
	event_ids = get_event_ids(events)
	#for event in events["data"]:
	#	event_ids.append(event["id"])

	print "_________________________ FACEBOOK ___________________________"
	#print event_ids
	events_attending = fb.get_event_attendance(event_ids[:MAX_EVENTS])
	#print events_attending

	pass_events, friendslist= fb.find_friends_attending(events_attending, friends)
	print friendslist
	friends_api = tObj.call_api(friendslist, events)
	print friends_api


	return jsonify(friends_api) 
	#replace with the list received

#heat map based on an event passing event and popularity
@app.route('/heatmap', methods=['GET'])
def get_heatmap():
	print "inside heatmap_api"

	#location = "Pune"
	#location = request.args.get('location')


	info = get_fb_data(location)
	#info = json.loads(fb.get_data(data))
	events = json.loads(fb.get_event_json(info))
	friends = fb.get_taggable_friends()
	print "Events - ", events
	event_ids = get_event_ids(events)
	#for event in events["data"]:
	#	event_ids.append(event["id"])

	#print "_________________________ FACEBOOK ___________________________"
	#print event_ids
	events_attending = fb.get_event_attendance(event_ids)
	heatmap_api = fb.create_events_heatmap(events_attending)
	print heatmap_api
	return jsonify(heatmap_api) 

#will give you credentials for the user
@app.route('/login', methods=['GET', 'OPTIONS'])
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

def get_fb_data(location):
	data =fb_call.request("search",{ 'q' : location, 'type' : 'event', 'limit':EVENT_LIMIT, 'since_date'  :   currentTime}) #'limit' ,before since_date
	info = json.loads(fb.get_data(data))
	return info

def get_event_ids(events):
	for event in events["data"]:
		event_ids.append(event["id"])

	return event_ids

fb = FacebookGraph()
ACCESS_TOKEN = fb.fetch_token()
fb_call = fb.call_api(ACCESS_TOKEN)

currentTime = int(time.time())
dnow=datetime.datetime.now()
#print str(dnow)[:-7]

#print currentTime
#fb.get_current_time()
"""
event_ids = []
events = {}
events_attending = {}
pass_events = {}
pass_events_names = []
events_name = []
events_info = []
friends = {}
friends_api = {}
heatmap_api = {}
friendslist = []"""
#data =fb_call.request("search",{ 'q' : location, 'type' : 'event', 'limit':EVENT_LIMIT, 'since_date'  :   currentTime}) #'limit' ,before since_date

# fb.get_data already returns us output in json format
#info = json.loads(fb.get_data(data))

#events = json.loads(fb.get_event_json(info))

#for event in events["data"]:
#	event_ids.append(event["id"])

#print events["data"][0]

###friends = fb.get_taggable_friends()	

###print "_________________________ FACEBOOK ___________________________"
#print event_ids
###events_attending = fb.get_event_attendance(event_ids)
#print events_attending

###pass_events, friends_api= fb.find_friends_attending(events_attending, friends)

#print friends_api

## --------------------- EVENTS API -------------------------------------

#events_api = fb.create_events_api(event_ids)
#print "\n\n\n\n"
#print json.dumps(events_api)

## --------------------- HEATMAP API -------------------------------------
# heatmap_api = fb.create_events_heatmap(events_attending)

#---------------- TWITTER STARTS ---------------------------------------------

tObj = Twitter_API()


ckey, csecret, atoken, asecret = tObj.authenticate()
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

print "Successfully authenticated.."
#print events



### friends_api = tObj.call_api(friendslist)
print friends_api

if __name__ == '__main__':
	app.run(debug=True)
	#run_app()
	"""

	fb = FacebookGraph()
	ACCESS_TOKEN = fb.fetch_token()
	fb_call = fb.call_api(ACCESS_TOKEN)

	currentTime = int(time.time())
	dnow=datetime.datetime.now()
	#print str(dnow)[:-7]

	#print currentTime
	#fb.get_current_time()"""
	"""
	event_ids = []
	events = {}
	events_attending = {}
	pass_events = {}
	pass_events_names = []
	events_name = []
	events_info = []
	friends = {}
	friends_api = {}
	heatmap_api = {}
	friendslist = []""""""
	data =fb_call.request("search",{ 'q' : location, 'type' : 'event', 'limit':EVENT_LIMIT, 'since_date'  :   currentTime}) #'limit' ,before since_date
	
	# fb.get_data already returns us output in json format
	info = json.loads(fb.get_data(data))
	
	events = json.loads(fb.get_event_json(info))
	
	for event in events["data"]:
		event_ids.append(event["id"])

	#print events["data"][0]
	
	friends = fb.get_taggable_friends()	
	
	print "_________________________ FACEBOOK ___________________________"
	#print event_ids
	events_attending = fb.get_event_attendance(event_ids)
	#print events_attending
	
	pass_events, friends_api= fb.find_friends_attending(events_attending, friends)

	print friends_api

	## --------------------- EVENTS API -------------------------------------
	
	events_api = fb.create_events_api(event_ids)
	print "\n\n\n\n"
	print json.dumps(events_api)

	## --------------------- HEATMAP API -------------------------------------
	heatmap_api = fb.create_events_heatmap(events_attending)

	#---------------- TWITTER STARTS ---------------------------------------------

	tObj = Twitter_API()
	
	
	ckey, csecret, atoken, asecret = tObj.authenticate()
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)
	
	print "Successfully authenticated.."
	#print events

	
	
	friends_api = tObj.call_api(friendslist)
	print friends_api"""
"""
friends = friends_api
print friends
events = events_api
print events
heatmap = heatmap_api
print heatmap
"""

