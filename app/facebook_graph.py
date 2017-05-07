#!/usr/bin/env python

###########################################
# This file only handles Facebook Graph   #
# API.                                    #
#                                         #
# Author: Saurabh Deochake                #
###########################################



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


CONFIG_FILE = "/etc/api_config"
EVENT_LIMIT = 10000
ATTENDING_LIMIT = 100000000
LOCATION = "Rutgers"
SELF_ID = "10203154386536494"

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
					#else:
					#	print "None!"
		pass_events = {"data": pass_events_names}
		return pass_events

	def get_taggable_friends(self):
		taggable = fb_call.get_connections(SELF_ID,"taggable_friends",limit=ATTENDING_LIMIT)
		for dictionary in taggable["data"]:
			friends[dictionary["name"]] = dictionary["picture"]["data"]["url"]
		return friends

	def get_event_attendance(self, event_ids):
		for id in event_ids:
			#print id
			connections = fb_call.get_connections(id, "attending",limit=ATTENDING_LIMIT,fields=[])
			if connections:
				events_name = []
				for name in connections["data"]:
					#print name["name"]
					events_name.append(name["name"])		
					events_attending[id] = events_name

		return events_attending

class Twitter_API:
	# get API instance
	def get_api(self):
		return tweepy.API(auth)#, wait_on_rate_limit=True)

	# call Twitter API
	def call_api(self, topic):
		print "\n\n\n***** TWITTER  *****"  
		api = self.get_api()
		#query = raw_input("\n\nEnter the location:")
		#event = raw_input("\nEnter the event name:")
		if len(friends) == 0:
			for friend in tweepy.Cursor(api.friends, count=200).items():
				friends.append(friend.screen_name)
			#print friends
		for data in pass_events["data"]:
			location = data["location"]
			g = geocoder.google(location)
			twitterStream = Stream(auth, Messenger())
			twitterStream.filter(locations=g.geojson['bbox'])  #Track tweets with location
			wait(5)
			

	def authenticate(self):
			
		print "Fetching authentication data..."
		parser = SafeConfigParser()
		parser.read(CONFIG_FILE)
		
		ckey = parser.get('twitter','ckey')
		csecret = parser.get('twitter','csecret')
		atoken = parser.get('twitter','atoken')
		asecret = parser.get('twitter','asecret')

		
		return ckey,csecret,atoken, asecret
	

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

	

if __name__ == '__main__':
	fb = FacebookGraph()
	ACCESS_TOKEN = fb.fetch_token()
	fb_call = fb.call_api(ACCESS_TOKEN)

	currentTime = int(time.time())
	dnow=datetime.datetime.now()
	#print str(dnow)[:-7]

	#print currentTime
	#fb.get_current_time()
	event_ids = []
	events = {}
	events_attending = {}
	pass_events = {}
	pass_events_names = []
	events_name = []
	events_info = []
	friends = {}
	data =fb_call.request("search",{ 'q' : LOCATION, 'type' : 'event', 'limit':EVENT_LIMIT, 'since_date'  :   currentTime}) #'limit' ,before since_date
	
	# fb.get_data already returns us output in json format
	info = json.loads(fb.get_data(data))
	
	events = json.loads(fb.get_event_json(info))
	
	for event in events["data"]:
		event_ids.append(event["id"])
	
	friends = fb.get_taggable_friends()	
	
	print "_________________________ FACEBOOK ___________________________"
	#print event_ids
	events_attending = fb.get_event_attendance(event_ids)
	#print events_attending
	
	pass_events = fb.find_friends_attending(events_attending, friends)
	#print pass_events

	#---------------- TWITTER STARTS ---------------------------------------------

	tObj = Twitter_API()
	
	
	ckey, csecret, atoken, asecret = tObj.authenticate()
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)
	
	print "Successfully authenticated.."
	#print events

	
	
	tObj.call_api(None)

	#print pass_events
				
