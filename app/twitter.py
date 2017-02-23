#!/usr/bin/env python

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from sys import version_info
import geocoder
#from bs4 import BeautifulSoup
import os
import time
import __future__
#import logging
import tweepy

cuskey = "#####"
cussecret = "#####"
token = "#####"
secret = "#####"

"""
Author: Saurabh Deochake (saurabh.d04@gmail.com)
Note: Before you run this script, please get your Consumer Key, Consumer Secret,
Access Token and Access Secret Keys from https://dev.twitter.com by creating your
own app
"""

class Twitter_API:
	# get API instance
	def get_api(self):
		return tweepy.API(auth)

	# call Twitter API
	def call_api(self, topic):
		print "\n\n\n***** WELCOME TO Evently Friends *****"  
		api = self.get_api()
		query = raw_input("\n\nEnter the location:")
		g = geocoder.google(query)
		twitterStream = Stream(auth, Messenger())
		twitterStream.filter(locations=g.geojson['bbox'])  #Track tweets with location
			
		
	def authenticate(self):
			
		print "Fetching authentication data..."
		ckey = cuskey
		csecret = cussecret
		atoken = token
		asecret = secret
		
		return ckey,csecret,atoken, asecret
	

class Messenger(StreamListener):
		   

	def on_data(self, data):
		try:
			
			#Take out username 
			userName = data.split(',"screen_name":"')[1].split('","location')[0]
			#Take out actual tweet
			tweet = data.split(',"text":"')[1].split('","source')[0]
			
			#Create message in format: @username: <text>
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

	
	tObj = Twitter_API()
	
	
	ckey, csecret, atoken, asecret = tObj.authenticate()
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)
	
	print "Successfully authenticated.."
	
	
tObj.call_api(None)
