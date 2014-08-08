#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import scraper_tools
import getopt
import getpass
import atom
import gdata.contacts.data
import gdata.contacts.client
from selenium import webdriver
import time
import twitter 
import json
from urllib2 import URLError
from httplib import BadStatusLine
import scraper_tools
import MySQLdb as mdb

email, password = scraper_tools.login_credits()


gd_client = gdata.contacts.client.ContactsClient(source='GoogleInc-ContactsPythonSample-1')
gd_client.ClientLogin(email, password, gd_client)

#twitter api
def api_login():

	consumer_key,consumer_secret,access_token,access_token_secret = scraper_tools.twit_credits()
	
	auth = twitter.oauth.OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
	twitter_api = twitter.Twitter(auth=auth)
	
	return twitter_api
	
search_email = sys.argv[1]

def CreateMenu(search_email):
    """Prompts that enable a user to create a contact."""
    """name = raw_input('Enter contact\'s name: ')
    notes = raw_input('Enter notes for contact: ')
    primary_email = raw_input('Enter primary email address: ')"""

    name = 'cos'
    notes = 'details'
    primary_email = search_email

    new_contact = gdata.contacts.data.ContactEntry(name=gdata.data.Name(full_name=gdata.data.FullName(text=name)))
    new_contact.content = atom.data.Content(text=notes)
    # Create a work email address for the contact and use as primary. 
    new_contact.email.append(gdata.data.Email(address=primary_email, 
        primary='true', rel=gdata.data.WORK_REL))
    entry = gd_client.CreateContact(new_contact)

    if entry:
      print 'Creation successful!'
      print 'ID for the new contact:', entry.id.text
      return entry.id.text
    else:
      print 'Upload error.'


def DeleteContactMenu():
    selected_entry = _SelectContact()
    gd_client.Delete(selected_entry)
    #feed = gd_client.GetContacts()
    #gd_client.Delete(feed)

def _SelectContact():
    feed = gd_client.GetContacts()
    PrintFeed(feed)
    selection = 5000
    while selection > len(feed.entry)+1 or selection < 1:
      #selection = int(raw_input(
      #    'Enter the number for the contact you would like to modify: '))
       selection = int(1)
       print "[+]Contact deleted"
    return feed.entry[selection-1]

def PrintFeed(feed, ctr=0):
    """Prints out the contents of a feed to the console.
   
    Args:
      feed: A gdata.contacts.ContactsFeed instance.
      ctr: [int] The number of entries in this feed previously printed. This
          allows continuous entry numbers when paging through a feed.
    
    Returns:
      The number of entries printed, including those previously printed as
      specified in ctr. This is for passing as an argument to ctr on
      successive calls to this method.
    
    """
    if not feed.entry:
      print '\nNo entries in feed.\n'
      return 0
    for i, entry in enumerate(feed.entry):
      print '\n%s %s' % (ctr+i+1, entry.title.text)
      if entry.content:
        print '    %s' % (entry.content.text)
      for email in entry.email:
        if email.primary and email.primary == 'true':
          print '    %s' % (email.address)
      # Show the contact groups that this contact is a member of.
      for group in entry.group_membership_info:
        print '    Member of group: %s' % (group.href)
      # Display extended properties.
      for extended_property in entry.extended_property:
        if extended_property.value:
          value = extended_property.value
        else:
          value = extended_property.GetXmlBlob()
        print '    Extended Property %s: %s' % (extended_property.name, value)
    return len(feed.entry) + ctr

feed = CreateMenu(search_email)

#################
#twitter
#################

#br = webdriver.Firefox()
br=webdriver.PhantomJS("/root/thesis/Social_Media_Scraper/dev/code/phantomjs/bin/phantomjs")
br.get('http://twitter.com')
#email, psswd = scraper_tools.login_credits()
#scraper_tools.fb_login(br, email, psswd)
print "[+]Logging to twitter"
user=br.find_element_by_id('signin-email')
user.send_keys(email)
psswd=br.find_element_by_id("signin-password")
psswd.send_keys(password)
login_bttn=br.find_element_by_xpath('//td[contains(@class, "flex-table-secondary")]/button').click()
print "[+]Logging success!"
br.get('https://twitter.com/who_to_follow/import')
gmail_bttn=br.find_element_by_xpath('//ul[contains(@id, "import-services-list")]/li/button').click()
time.sleep(10)
print "Redirecting to Google Contacts ..." 
br.switch_to_window(br.window_handles[1])
#submit credentials
gmail_email=br.find_element_by_id("Email")
gmail_email.send_keys(email)
gmail_psswd=br.find_element_by_id("Passwd")
gmail_psswd.send_keys(password)
gmail_bttn_sign=br.find_element_by_id("signIn").click()
time.sleep(7)
gmail_approve=br.find_element_by_id("submit_approve_access").click()
print "Google Contacts approved"
br.switch_to_window(br.window_handles[0])
time.sleep(5)

results_ver =  br.find_element_by_id("content-main-heading").text
if not (results_ver.find("None")==-1):
	print "User not on twitter"
else:
	account = br.find_element_by_css_selector("a.account-group")
	account_url = account.get_attribute('href')
	account_id = account.get_attribute('data-user-id')
	account_header = account.text
	account_bio=br.find_element_by_class_name("bio").text

	print "User : " + account_header
	print account_bio
	print "User id : " + str(account_id)
	print account_url

	#go to account url
	br.get(account_url)

#################
#twitter api
#################
def get_user_profile(twitter_api, screen_names=None, user_ids=None):
	# Must have either screen_name or user_id (logical xor)
	assert (screen_names != None) != (user_ids != None), \
	"Must have screen_names or user_ids, but not both"

	items_to_info = {}
	
	items = screen_names or user_ids

	while len(items) > 0:
		# Process 100 items at a time per the API specifications for /users/lookup.
	# See https://dev.twitter.com/docs/api/1.1/get/users/lookup for details.
		items_str = ','.join([str(item) for item in items[:100]])
		items = items[100:]
		if screen_names:
			response = make_twitter_request(twitter_api.users.lookup, screen_name=items_str)
		else: # user_ids
			response = make_twitter_request(twitter_api.users.lookup, user_id=items_str)
		for user_info in response:
			if screen_names:
				items_to_info[user_info['screen_name']] = user_info
			else: # user_ids
				items_to_info[user_info['id']] = user_info

	return items_to_info

def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw):
	# A nested helper function that handles common HTTPErrors. Return an updated
	# value for wait_period if the problem is a 500 level error. Block until the
	# rate limit is reset if it's a rate limiting issue (429 error). Returns None
	# for 401 and 404 errors, which requires special handling by the caller.
	def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):
		if wait_period > 3600: # Seconds
			print >> sys.stderr, 'Too many retries. Quitting.'
			raise e
		# See https://dev.twitter.com/docs/error-codes-responses for common codes
		if e.e.code == 401:
			print >> sys.stderr, 'Encountered 401 Error (Not Authorized)'
			return None
		elif e.e.code == 404:
			print >> sys.stderr, 'Encountered 404 Error (Not Found)'
			return None
		elif e.e.code == 429:
			print >> sys.stderr, 'Encountered 429 Error (Rate Limit Exceeded)'
			if sleep_when_rate_limited:
				print >> sys.stderr, "Retrying in 15 minutes...ZzZ..."
				sys.stderr.flush()
				time.sleep(60*15 + 5)
				print >> sys.stderr, '...ZzZ...Awake now and trying again.'
				return 2
			else:
				raise e # Caller must handle the rate limiting issue
		elif e.e.code in (500, 502, 503, 504):
			print >> sys.stderr, 'Encountered %i Error. Retrying in %i seconds' % \
				(e.e.code, wait_period)
			time.sleep(wait_period)
			wait_period *= 1.5
			return wait_period
		else:
			raise e
	# End of nested helper function
	wait_period = 2
	error_count = 0
	while True:
		try:
			return twitter_api_func(*args, **kw)
		except twitter.api.TwitterHTTPError, e:
			error_count = 0
			wait_period = handle_twitter_http_error(e, wait_period)
			if wait_period is None:
				return
		except URLError, e:
			error_count += 1
			print >> sys.stderr, "URLError encountered. Continuing."
			if error_count > max_errors:
				print >> sys.stderr, "Too many consecutive errors...bailing out."
				raise
		except BadStatusLine, e:
			error_count += 1
			print >> sys.stderr, "BadStatusLine encountered. Continuing."
			if error_count > max_errors:
				print >> sys.stderr, "Too many consecutive errors...bailing out."
				raise

###
DeleteContactMenu()
###
twitter_api = api_login()
if not(account_header is None):
	user = account_header[account_header.index("@")+1:]
	results = get_user_profile(twitter_api, screen_names=[user])
	j_data = results
	with open('data.txt', 'a') as outfile:
    		json.dump(j_data, outfile, indent=2)
	print results

#list which helps creates dictionary for database to avoid null problem
info_check_list = ['search_email', 'u_name', 'profile_id', 'screen_name', 'name', 'location', 'description', 'profile_img', 'background_img', 'url', 'followers_count', 'friends_count', 'statuses_count', 'listed_count', 'favourites_count', 'lang', 'geo_enabled', 'notifications', 'contributors_enabled', 'protected', 'created_at']
#scrap json
#search_email
u_name = results.keys()[0]
#u_name = u_name[0]
other_keys= results[u_name].keys()
profile_id = results[u_name]['id']
background_img = results[u_name]['profile_background_image_url_https']

#other_res = results[u_name].keys()
#for key in other_res:
#	print key , ' : ' ,results[u_name][key]

profile_img = str(results[u_name]['profile_image_url_https'])
followers_count = str(results[u_name]['followers_count'])
listed_count = str(results[u_name]['listed_count'])
statuses_count= str(results[u_name]['statuses_count'])#tweets
description = str(results[u_name]['description'])
friends_count = str(results[u_name]['friends_count'])
location = str(results[u_name]['location'])
geo_enabled = str(results[u_name]['geo_enabled']) 
screen_name = results[u_name]['screen_name']
lang = results[u_name]['lang']
profile_background_tile = results[u_name]['profile_background_tile']
favourites_count = results[u_name]['favourites_count']
name = results[u_name]['name']
notifications = results[u_name]['notifications']
url = results[u_name]['url']
created_at = results[u_name]['created_at']
contributors_enabled = results[u_name]['contributors_enabled']
#time_zone = results[u_name]['time_zone']
protected = results[u_name]['protected']

li_info=[search_email, u_name, profile_id, screen_name, name, location, description, profile_img, background_img, url, followers_count, friends_count, statuses_count, listed_count, favourites_count, lang, geo_enabled, notifications, contributors_enabled, protected, created_at]
#create dictionary for Db
di={}
for i in range(0, len(info_check_list)):
	if li_info[i] is None:
		di[info_check_list[i]]='none'
	else:
		di[info_check_list[i]]= li_info[i]

#database
try:
	
	host, user, psswd, db = scraper_tools.login_db()
	con = mdb.connect(host, user, psswd, db);
	print "[+]DB connected"
	cur = con.cursor()

	"""add_info = ("INSERT INTO twitter_scrap_general "
		    "(email, username, profile_id, screen_name, name, location, description, profile_img, background_img, url, followers_count, friends_count, statuses_count, listed_count, favourites_count, lang, geo_enabled, notifications, contributors_enabled, protected, created_at)"
		    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")"""
	add_info = ("INSERT INTO twitter_scrap_general "
		    "(email, username, profile_id, screen_name, name, location, description, profile_img, background_img, url, followers_count, friends_count, statuses_count, listed_count, favourites_count, lang, geo_enabled, notifications, contributors_enabled, protected, created_at)"
		    "VALUES (%(search_email)s,%(u_name)s,%(profile_id)s,%(screen_name)s,%(name)s,%(location)s,%(description)s,%(profile_img)s,%(background_img)s,%(url)s,%(followers_count)s,%(friends_count)s,%(statuses_count)s,%(listed_count)s,%(favourites_count)s,%(lang)s,%(geo_enabled)s,%(notifications)s,%(contributors_enabled)s,%(protected)s,%(created_at)s)")
	
	"""add_info = ("INSERT INTO twitter_scrap_general "
		    "(username, profile_id, screen_name, name, location, description, profile_img, background_img, url, followers_count, friends_count, statuses_count, listed_count, favourites_count, lang, geo_enabled, notifications, contributors_enabled, protected, created_at)"
		    "VALUES (%(u_name)s,%(profile_id)s,%(screen_name)s,%(name)s,%(location)s,%(description)s,%(profile_img)s,%(background_img)s,%(url)s,%(followers_count)s,%(friends_count)s,%(statuses_count)s,%(listed_count)s,%(favourites_count)s,%(lang)s,%(geo_enabled)s,%(notifications)s,%(contributors_enabled)s,%(protected)s,%(created_at)s)")
	"""
	cur.execute(add_info, di)
	con.commit()
	print "[+] Data added"
    
except mdb.Error, e:
  
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
    
finally:    
        
	if con:    
		con.close()


#tweets
"""
status = results[u_name]['status'].keys()
>>> for key in status:
...     print key , ' : ' ,results[u_name]['status'][key]
... 
contributors  :  None
truncated  :  False
text  :  #LoughTay #GuinnessLake #TheSallyGap #Wicklow @DiscoverIreland  #Vikings Kattegat Village ?, roll on Season 3 ;D http://t.co/SVZLyH2KNH
in_reply_to_status_id  :  None
id  :  487679545081073664
favorite_count  :  1
source  :  <a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>
retweeted  :  False
coordinates  :  None
entities  :  {u'symbols': [], u'user_mentions': [{u'id': 15255537, u'indices': [46, 62], u'id_str': u'15255537', u'screen_name': u'DiscoverIreland', u'name': u'Discover Ireland'}], u'hashtags': [{u'indices': [0, 9], u'text': u'LoughTay'}, {u'indices': [10, 23], u'text': u'GuinnessLake'}, {u'indices': [24, 36], u'text': u'TheSallyGap'}, {u'indices': [37, 45], u'text': u'Wicklow'}, {u'indices': [64, 72], u'text': u'Vikings'}], u'urls': [], u'media': [{u'expanded_url': u'http://twitter.com/WildAnglePro/status/487679545081073664/photo/1', u'display_url': u'pic.twitter.com/SVZLyH2KNH', u'url': u'http://t.co/SVZLyH2KNH', u'media_url_https': u'https://pbs.twimg.com/media/BsSV9OVIUAAKKC2.jpg', u'id_str': u'487679538714136576', u'sizes': {u'large': {u'h': 683, u'resize': u'fit', u'w': 1024}, u'small': {u'h': 227, u'resize': u'fit', u'w': 340}, u'medium': {u'h': 400, u'resize': u'fit', u'w': 600}, u'thumb': {u'h': 150, u'resize': u'crop', u'w': 150}}, u'indices': [113, 135], u'type': u'photo', u'id': 487679538714136576L, u'media_url': u'http://pbs.twimg.com/media/BsSV9OVIUAAKKC2.jpg'}]}
in_reply_to_screen_name  :  None
id_str  :  487679545081073664
retweet_count  :  0
in_reply_to_user_id  :  None
favorited  :  False
geo  :  None
in_reply_to_user_id_str  :  None
possibly_sensitive  :  False
lang  :  en
created_at  :  Fri Jul 11 19:27:18 +0000 2014
in_reply_to_status_id_str  :  None
place  :  None
"""
