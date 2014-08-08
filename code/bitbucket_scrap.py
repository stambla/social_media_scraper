#!/usr/bin/python
import sys
from selenium import webdriver
import urllib2
import json
import time


#bit bucket allows to add friends to you project by sending them request
#simply xhr query takes username or email address, and return json

email = sys.argv[1]
url = "https://bitbucket.org/xhr/user-mention?term="+email

data = json.load(urllib2.urlopen(url))
if len(data)==0:
	print "[+]Not on bitbucket!"
else:
	data = data[0]
	print data
	username = data['username']
	br = webdriver.Firefox()
	user_url = "https://bitbucket.org/" + username
	br.get(user_url)
	#basic info
	#time.sleep(2)
	
	user_profile = br.find_element_by_id("user-profile")
	picture = user_profile.find_element_by_css_selector('img').get_attribute('src')
	#structure full_name & username > url > location > joined
	#full_name/username and joined len=2
	user_profile_text=user_profile.text.split('\n')
	full_name=user_profile_text[0][:user_profile_text[0].find('(')-1]
	username=user_profile_text[0][user_profile_text[0].find('(')+1:user_profile_text[0].find(')')]
	joined=user_profile_text[-1] #always as a last
	if len(user_profile_text)==4:
		url=user_profile_text[1]
		location=user_profile_text[2]
	else:
		if user_profile_text[1].find('http')==-1:
			location=user_profile_text[1]
		else:
			url=user_profile_text[1]
	print username, picture, full_name, joined,
