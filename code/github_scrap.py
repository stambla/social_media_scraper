#!/usr/bin/python
from selenium import webdriver
import sys
import time
import scraper_tools
import json
import urllib2

#==================================================================================================
#Functions
#============
def find_mejl(lap):
	"""
		Takes no of page, returns username
	"""
	url='https://github.com/search?p='+str(lap)+'&q=tom+in%3Aemail&ref=searchresults&type=Users'
	br.get(url)
	users = br.find_elements_by_class_name("user-list-item")
	#lapping = True
	user_email=' ' 
	while user_email != email:
		for i in range(0, len(users)):
			user_info=users[i].text.split('\n')
			user_email = user_info[3]
			if user_email == email:
				print "[+]mejl found!", "page :", lap, "position :", i+1
				#lapping = False
				print user_info[1:]
				user_url = users[i].find_elements_by_css_selector('a')[2].get_attribute('href')
				return user_url				
			
#===========================
def scrap_user(user):
	#public contributions
	url_contr = "https://github.com/users/"+user+"/contributions_calendar_data?_=1405926448662"
	#"https://github.com/users/stambla/contributions_calendar_data?_=1405926448662"
	#repositiories
	repo_list = br.find_element_by_class_name("repo-list").find_elements_by_tag_name('a')
	len(repo_list)
	repos[0].text
	res_link = repos[0].get_attribute('href')
	download_res_url_zip =  res_link + "archive/master.zip"
#===========================
def contributions(user):
	"""
		Takes username return json of the latest user's contributions (json)
	"""
	#url = "https://github.com/users/"+user+"/contributions_calendar_data?"	
	data = json.load(urllib2.urlopen("https://github.com/users/"+user+"/contributions_calendar_data?"))
	return data

#===========================
#other shits
#picture
#https://avatars1.githubusercontent.com/u/3587873

#==================================================================================================
#Body
#==========================

username, psswd = scraper_tools.login_credits_github()
#log to github
br = webdriver.Firefox()
br.get('https://www.github.com/login')
br.find_element_by_id('login_field').send_keys(username)
br.find_element_by_id('password').send_keys(psswd)
button = br.find_element_by_class_name('button')
button.click()
print "[+]Logging to Github....."

email=sys.argv[1]
usr_email = email[:email.find('@')]

#to search for github user by email follow request must be put into search box
#"name_before_@ in:email"
#or simple request
url = 'https://github.com/search?q='+usr_email+'+in%3Aemail&type=Users'
br.get(url)

#how many user have been found
time.sleep(5)

user_list = br.find_elements_by_class_name("user-list-info")
if len(user_list) == 0:
	print "[+]User is not on github or is hidden!!!"
elif len(user_list) == 1:
	print "[+]Email ",email, " has been mapped to user :"
	print user_list[0].text
	user_url = user_list[0].find_element_by_tag_name('a').get_attribute('href')
		
else:
	print "[+]A lot of user found, has to be mapped to correct email address"

	count = br.find_elements_by_css_selector('h3')
	number=count[1].text.split(' ')
	number = int(number[2])
	print number
	laps = number//10 +1
	for lap in range(2, laps):
		user_url=str(find_mejl(lap))
		break

#time.sleep(2)
#print "oto link :", user_url
br.get(user_url)
picture = br.find_element_by_class_name("vcard-avatar").get_attribute('href')
username=user_url[user_url.find('m/')+2:]
full_name = br.find_element_by_class_name("vcard-fullname").text
details = br.find_elements_by_class_name("vcard-detail")
#details_li=['company','location', 'email', 'url','joined']
company = ''
location = ''
email = ''
url = ''
joined = ''
#=======
#stats
stats=br.find_elements_by_class_name("vcard-stat")
followers = stats[0].text.split('\n')[0]
followers_url=stats[0].get_attribute('href')
starred = stats[1].text.split('\n')[0]
starred_url=stats[1].get_attribute('href')
following = stats[2].text.split('\n')[0]
following_url=stats[2].get_attribute('href')
#==========
user_contribution= contributions(username)
if len(details)== 4:
	location = details[0].text
	email = details[1].text
	url = details[2].text
	joined = details[3].text
	
elif len(details)== 5:
	comapny = details[0].text
	location = details[1].text
	email = details[2].text
	url = details[3].text
	joined = details[4].text

print "[+]Picture :", picture,"\n[+]username :", username, "\n[+]url :",user_url, "\n[+]Comapny :", comapny,"\n[+]Location: ",location,"\n[+]email :", email,"\n[+]url :", url, "\n[+]Joined :", joined,"\n[+]Followers :", followers, "\n[+]Starred :",starred,"\n[+]Following :",following,"\n[+]Contributions :", user_contribution

