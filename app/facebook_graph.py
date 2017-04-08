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

ACCESS_TOKEN = 'EAAFWO0sUZCjABAGqo5GUg5ybiWqN1yclbk1sX6UZARYLARmgrFWlYteaKsM4GCifOeeM8Dd6aVPNV4UlA1iZCFwC2R1O3dtSRD6D3LWaudZBaV77ovpRorSZAoqrsDhUStZAa5cnpIboPcqwXJ3NUUKnaSVwqxv6KrKCYVTZClub7w1ZALLxD5MsJg6vK2ljlygZD'

#'376287639436848|1En1eFeWVQtThrRZ-gXu5zWpNHU'

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

if __name__ == '__main__':
	fb = FacebookGraph()
	ACCESS_TOKEN = fb.fetch_token()
	fb_call = fb.call_api(ACCESS_TOKEN)

#g = facebook.GraphAPI(ACCESS_TOKEN)

	currentTime = fb.get_current_time()

	print '---------------'
	print 'Events'
	print '---------------'
	data =fb_call.request("search",{ 'q' : 'New Brunswick, NJ', 'type' : 'event', 'limit' : 5, 'since_date'  :   'currentTime'})
	fb.get_data(data)
