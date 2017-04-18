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

	def get_event_ids(self, ids, info):
		for i in info["data"]:
			ids.append(i["id"])
		return set(ids)

	#def __unicode__(self):
	#	return unicode(self.some_field) or u''

if __name__ == '__main__':
	fb = FacebookGraph()
	ACCESS_TOKEN = fb.fetch_token()
	fb_call = fb.call_api(ACCESS_TOKEN)

	currentTime = fb.get_current_time()
	ids = []
	events = {}
	events_info = []
	data =fb_call.request("search",{ 'q' : 'Chicago', 'type' : 'event', 'limit':EVENT_LIMIT, 'since_date'  :   'currentTime'}) #'limit' ,before since_date
	
	# fb.get_data already returns us output in json format
	info = json.loads(fb.get_data(data))
	
	#print len(fb.get_event_ids(ids, info))

	for i in info["data"]:
		if "end_time" in i and "place" in i and "name" in i["place"] and "start_time" in i and "description" in i:
			d = {"id": i["id"], "name": i["name"], "description": i["description"],"start_time": i["start_time"], "end_time":i["end_time"], 
		      	"location":i["place"]["name"]}

		else:
			d = {"id": i["id"], "name": i["name"], "start_time": i["start_time"]}

		events_info.append(d)
	
	events = {"data": events_info}
	events = json.dumps(events)
	print events
	
	# Now we have to get 
	# 1. All Event IDs
	# 2. Start and End dates
	# 3. people attending events for all event IDs"""