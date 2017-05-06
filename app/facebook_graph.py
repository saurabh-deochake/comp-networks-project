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

CONFIG_FILE = "/etc/api_config"
EVENT_LIMIT = 10000
ATTENDING_LIMIT = 100000000
LOCATION = "New Brunswick"
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
		flag = 0
		#print events_attending
		for key in events_attending:
			#print key
			for name in events_attending[key]:
				if name in friends:
					flag += 1
					if flag == 1:
						print "Friends attending \""+fb_call.get_object(key)["name"]+"\" at "+fb_call.get_object(key)["place"]["name"]+":"	
						print "inside here"
					print name + " Picture: "+friends[name]

	def get_taggable_friends(self):
		taggable = fb_call.get_connections(SELF_ID,"taggable_friends",limit=ATTENDING_LIMIT)
		for dictionary in taggable["data"]:
			friends[dictionary["name"]] = dictionary["picture"]["data"]["url"]
		return friends

	def get_event_attendance(self, event_ids):
		for id in event_ids:
			#print id
			connections = fb_call.get_connections(id, "attending",limit=ATTENDING_LIMIT,fields=[])
			events_name = []
			for name in connections["data"]:
				#print name["name"]
				events_name.append(name["name"])		
				events_attending[id] = events_name

		return events_attending

		
	

if __name__ == '__main__':
	fb = FacebookGraph()
	ACCESS_TOKEN = fb.fetch_token()
	fb_call = fb.call_api(ACCESS_TOKEN)

	currentTime = fb.get_current_time()
	event_ids = []
	events = {}
	events_attending = {}
	events_name = []
	events_info = []
	friends = {}
	data =fb_call.request("search",{ 'q' : LOCATION, 'type' : 'event', 'limit':EVENT_LIMIT, 'since_date'  :   'currentTime'}) #'limit' ,before since_date
	
	# fb.get_data already returns us output in json format
	info = json.loads(fb.get_data(data))
	
	events = json.loads(fb.get_event_json(info))
	
	for event in events["data"]:
		event_ids.append(event["id"])
	
	friends = fb.get_taggable_friends()	
	
	print "______________________________________________________"
	print event_ids
	events_attending = fb.get_event_attendance(event_ids)
	
	fb.find_friends_attending(events_attending, friends)
				
