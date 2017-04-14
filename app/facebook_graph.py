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
from facebook import GraphAPI # pip install facebook-sdk
from ConfigParser import SafeConfigParser

CONFIG_FILE = "/etc/api_config"


class FacebookGraph:

	def call_api(self, ACCESS_TOKEN):
		return facebook.GraphAPI(ACCESS_TOKEN)

	def fetch_token(self):
		parser = SafeConfigParser()
		parser.read(CONFIG_FILE)
		USER_TOKEN = parser.get('facebook','utoken')
		return USER_TOKEN

	def get_data(self, data_request):
		print json.dumps(data_request, indent=1)

	def get_current_time(self):
		return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

	#def __unicode__(self):
	#	return unicode(self.some_field) or u''

if __name__ == '__main__':
	fb = FacebookGraph()
	ACCESS_TOKEN = fb.fetch_token()
	fb_call = fb.call_api(ACCESS_TOKEN)

#g = facebook.GraphAPI(ACCESS_TOKEN)

	currentTime = fb.get_current_time()

	print '---------------'
	print 'Events'
	print '---------------'
	data =fb_call.request("search",{ 'q' : 'New York', 'type' : 'event',  'limit' : 5, 'since_date'  :   'currentTime'}) #'limit' ,before since_date
	fb.get_data(data)
	
	#print api_data

	"""with open(api_data) as data_file:
		info = json.load(data_file)
		
	print info["data"][0][id]"""


