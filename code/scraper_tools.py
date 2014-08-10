#!/usr/bin python
from selenium import webdriver
import os
import urllib
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import re

def login_credits():
	login_info = open("thesis.txt").read()
	login_info = login_info.splitlines()
	email = login_info[0]
	psswd  = login_info[1]
	return (email, psswd)

def login_credits_github():
	login_info = open("thesis.txt").read()
	login_info = login_info.splitlines()
	email = login_info[0]
	psswd = login_info[2]
	return (email, psswd)

def login_db():
	login_info = open("db.txt").read()
	login_info = login_info.splitlines()
	host = login_info[0]
	user = login_info[1]
	psswd = login_info[2]
	db = login_info[3]
	return (host, user, psswd, db)

def twit_credits():
	keys_info = open("twit_api.txt").read()
	keys_info = keys_info.splitlines()
	consumer_key = keys_info[0]
	consumer_secret = keys_info[1]
	access_token = keys_info[2]
	access_token_secret = keys_info[3]
	return (consumer_key, consumer_secret, access_token, access_token_secret)

def fb_login(webdriver, email, psswd):
	sign_in_email =  webdriver.find_element_by_id('email')
	sign_in_email.send_keys(email)
	sign_in_pas =  webdriver.find_element_by_id('pass')
	sign_in_pas.send_keys(psswd)
	sign_in_button = webdriver.find_element_by_id('u_0_n')
	sign_in_button.click()

def get_id(br):
	"""Takes webdriver and returns the user FB id from html source code"""
	source=br.page_source
	m=re.search('profile_id=(.*)&', source)
	profile_id=m.group(1)
	profile_id = profile_id[:profile_id.index('&')]
	return profile_id


def fb_name(some_str):
	"""Takes string, replace apostrophe with blank, and space with hyphen"""
	if not (some_str.find("'")==-1):
		print"[+]Dumping apostrophe"
	        some_str.replace("'", "")
         
	return some_str.replace(" ", "-")


def fb_search(br, search_email):
	email, psswd = login_credits()
	user_id = None
	name_displayed = None
	print"[+]Connecting to FaceBook"
	br = webdriver.Firefox()
	#run with phanthom js
	#br=webdriver.PhantomJS('/home/usrname/Desktop/thesis/phantomjs/bin/phantomjs')
	br.get('http://facebook.com')
	#fb_login(br, email, psswd)
	fb_login(br, email, psswd)
	#search for user with the email (fb search box)
	time.sleep(2)
	print"[+]Resolving email to username"
	fb_search = br.find_element_by_class_name('_586i')
	fb_search.send_keys(search_email)
	fb_search.send_keys(Keys.RETURN)
	#get username
	time.sleep(5)
	username = br.current_url
	if not (username.find('?')== -1):
		if not (username.find('=') == -1):
			
			#username_post = username[username.index('=')+3:username.index('&')]
			if not (username.find('%40') == -1):
				print "[+]User not on FaceBook!!!!"				
				username_post = None

			elif not (username.find('&') == -1):
				print"[+]User not got assigned username. ID used instead"
				username_post = username[username.index('=')+1:username.index('&')]
				user_id = get_id(br)
				name_displayed = fb_name(br.title)
			else:
				print"[+]User not got assigned username. ID used instead"
				username_post = username[username.index('=')+1:]
				user_id = get_id(br)
				name_displayed = fb_name(br.title)
		else:
			username_post = username[username.index('m')+2:username.index('?')]
			user_id = get_id(br)
			name_displayed = fb_name(br.title)
	else:
		username_post = username[username.index('m')+2:]
		user_id = get_id(br)
		name_displayed = fb_name(br.title)

	br.close()

	print"[+]Email ", search_email, " mapped to ", username_post, " username"
	
	return username_post , user_id, name_displayed
#========================================================================
#prepare for db insertion
def blanks_list(variable_list):
	"""takes string array returns array of blanks of the length of inputted array"""
	values_li=[]
	for i in range(0, len(variable+_list)):
		values_li.append(' ')
	return values_li

def create_dic(frist_list, second_list):
	"""Takes two list of the same lenght,
	    Returns dictionary
	"""
	di = {}
	for i in range(0, len(variable_list)):
		di[variable_list[i]] = values_li[i]
	return di
#========================================================================
#create payload folder for FB
def create_output_dir(usr):
	new_dir = '/root/thesis/Social_Media_Scraper/dev/code/fb/'+usr	
	print "[+]Creating payload dir for " + usr	
	os.mkdir(new_dir)
	return new_dir
#========================================================================
#save file
def save_file(path, file_name, file_to_save):
	#os.chdir(nowy_dir)
	f = open(path+"/"+file_name, "wb")
	f.write(file_to_save)
	f.close()
#========================================================================
#FB photos
def fb_download_photos(url_list, user, path):
	"""nowy_dir = '/root/thesis/Social_Media_Scraper/dev/code/fb/'+user	
	#print "[+]Creating new folder"	
	os.mkdir(nowy_dir)
	os.chdir(nowy_dir)
	"""	
	count = 1
	for item in url_list:
		#os.system("wget -U firefox "+item)
		f = open(path + str(count)+".jpg", "wb")
		f.write(urllib.urlopen(item).read())
		f.close()
		count +=1

def is_element_present(br, class_name):
	try:
		br.find_element_by_class_name(class_name)
	except NoSuchElementException:
		return False
	return True

def is_element_present_xpath(br):
	try:
		br.find_element_by_xpath('//img[contains(@class, "_359 img")]')
	except NoSuchElementException:
		return False
	return True

def is_element_present_id(br, id):
	try:
		br.find_element_by_xpath(id)
	except NoSuchElementException:
		return False
	return True

def scroll_timeln(vr, web_elment):
	if web_elemnt.is_enabled() == True:
		body = br.find_element_by_css_selector('body')
		scroll = Ture
		count = 0
		while scroll:
			body.send_keys(Keys.PAGE_DOWN)
			scroll = scraper_tools.is_element_present_id(br, "u_0_1o_scroll_trigger")
			scroll
			count +=1
			print"Scrolling", count, scroll

def scroll_timeln(br, web_elemnt):
	if web_elemnt.is_enabled() == True:
		body = br.find_element_by_css_selector('body')
		scroll= True
		count = 0
		while scroll:
			body.send_keys(Keys.PAGE_DOWN)
			scroll = scraper_tools.is_element_present_id(br, "u_0_1o_scroll_trigger")
			scroll
			count +=1
			print"Scrolling", count, scroll
		
def scrap_sub_topics(br, topic_id, user):
	""" (webdriver, div_id) -> list
	
	"""
	#print "[+]Welcome in scrap topic..."
	old_school = br.find_element_by_id(topic_id)
	#print old_school.text
	#it takes image and discription of the page/element...
	#images
	imgs = old_school.find_element_by_css_selector('img') #images only "https://fbcdn-profile - ...."
	li_img=[]
	for item in imgs:
		check = item.get_attribute('src')
		if not (check.find("https://fbcdn-profile")== -1):
			li_img.append(check)
		#print li_img
		
		#description
		description = old_school.find_elements_by_class_name("_5rz")
		li_descript=[]
		for descript in description:
			li_descript.append(descript.text)

		#print "description ", li_descript

		#link
		links = old_school.find_elements_by_css_selector('a')#.get_attribute('hrer)
		li_links = []
		for link in links:
			check = link.get_attribute('href')
			if check.find(user) == -1: #only page or profiles other than user are considered
				li_links.append(check)
		#in result we get list of duplicate links
		#it must be removed with maintance of the order
		li_links_final = []
		for i in xrange(0, len(li_links),2):
			li_links_final.append(li_links[i])
		#printli_links_final)
		#print results
		for i in range(0, len(li_img)):
			print"-"*10
			print"[",i+1,"]", li_descript[i]
			print"Image: ", li_img[i]
			print"Link: ", li_links_final[i]
