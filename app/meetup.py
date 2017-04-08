#!/usr/bin/env python

###########################################
# This file only handles Meetup API. Get  #
# the events at and around a location     #
# provided                                #
#                                         #
# Author: Saurabh Deochake                #
###########################################

import meetup.api 
from ConfigParser import SafeConfigParser

class Meetup:
	def getClient():
		client = meetup.api.Client()
		parser = SafeConfigParser()
		parser.read(CONFIG_FILE)
		
		client.api_key = parser.get('meetup','apikey')
		
		print client.api_key

if __name__ == '__main__':
	mObj = Meetup()
	mObj.getClient()