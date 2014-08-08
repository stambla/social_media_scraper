#!/usr/bin/python
from selenium import webdriver
import scraper_tools
from BeautifulSoup import BeautifulSoup
import time
import sys
import os
import random
from selenium.webdriver.common.action_chains import Keys
from selenium.common.exceptions import NoSuchElementException

user_email = str(sys.argv[1])
#user = str(sys.argv[1])
br = webdriver.Firefox()
br.get('http://facebook.com/')
print "[+]Login to Facebook"
email, psswd = scraper_tools.login_credits()
scraper_tools.fb_login(br, email, psswd)
user = scraper_tools.fb_search(br, user_email)
#==============================================================
def scrolling_continue(br):
	body = br.find_element_by_tag_name('body')
	count =0
	scroll = True
	print "[+]Scrolling..."
	while scroll :
		#time.sleep(random.randrange(1, 5))
		body.send_keys(Keys.PAGE_DOWN)
		scroll = scraper_tools.is_element_present(br, "_359")
		scroll	
		#scrolling = br.find_element_by_class_name("_359")
		count += 1	
		#print "[+]Scrolling...", count, scroll
	

#==============================================================
#Photos
def get_photos(br):
	print "[+]Redirecting to :" + user + " photos"
	
	if user.isdigit():
		br.get("https://www.facebook.com/profile.php?id="+user+"&sk=photos")
	else:
		br.get("https://www.facebook.com/"+user+"/photos")	
	#br.get('https://facebook.com/'+user+'/photos')
	time.sleep(10)
	body = br.find_element_by_tag_name('body')
	count =0
	scroll = True
	print "[+]Scrolling..."
	while scroll :
		#time.sleep(random.randrange(1, 5))
		body.send_keys(Keys.PAGE_DOWN)
		scroll = scraper_tools.is_element_present(br, "_359")
		scroll	
		#scrolling = br.find_element_by_class_name("_359")
		count += 1	
		#print "[+]Scrolling...", count, scroll
	
	time.sleep(2)
	source = br.page_source
	soup = BeautifulSoup(source)
	li=[]
	for tag in soup.findAll('i',attrs={"class":"uiMediaThumbImg"}):
		li.append(tag.attrMap)
	
	#print "[+]all i frame list", li
	#pic_url = li[0]['style']
	#pic_url=pic_url[pic_url.find('(')+1:pic_url.find(')')]
	photo_list=[]
	for item in range(0, len(li)):
		pic_url=li[item]['style']
		pic_url=pic_url[pic_url.find('(')+1:pic_url.find(')')]	
		photo_list.append(pic_url)
	
	print "[+]all links ", len(photo_list)#,photo_list
	print "[+] Downloading photos"
	scraper_tools.fb_download_photos(photo_list, user)
	
#===============================================================
def scrolling(br):
	
	try:	#'a' class "_3t3" is for all "See More" cases	
		f_s_m = br.find_element_by_class_name("_3t3")# "See All" element
		f_s_m.click()
	except:
		#print "[+]Less than 8 "#,f_li[0]
		#scroll to see all friends
		count =0
		body = br.find_element_by_css_selector("body")
		scroll = True
		time.sleep(10)
		print "[+]Scrolling...."
		while scroll :
			#time.sleep(random.randrange(1, 5))
			body.send_keys(Keys.PAGE_DOWN)
			scroll = scraper_tools.is_element_present_xpath(br)
			scroll	
			#scrolling = br.find_element_by_class_name("_359")
			count += 1	
			#print "[+]Scrolling...", count, scroll
	#return None
#===============================================================
#Friends
def get_friends(br):
	##friends options
	time.sleep(2)
	friends_options = br.find_elements_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[2]/div[1]/a')
	f_li = []
	for i in range(0, len(friends_options)):
		f_li.append(friends_options[i].text)
	print "[+]User ", user, " has got ", f_li 
	print '-'*10
	print friends_options[0].text
	
	#Should be clicked "See All"?
	#How many of click to "see all"?
	#times = len(br.find_elements_by_class_name("_3t3"))
	#print times
	#for time in range(0,times):

	
	#scrolling(br)	
	time.sleep(2)
	scrolling(br)
	#list of All friends
	f_list=br.find_elements_by_class_name("_698")
	print "[+]User ", user, " has got ", len(f_list),f_li[0]
	for i in range(0, len(f_list)):
		friend = f_list[i].text.split('\n')
		print "-"*10
		print "[",i+1,"]"
		username = f_list[i].find_element_by_css_selector('a').get_attribute('href')
		username = username[25:username.find('?')]
		photo = f_list[i].find_element_by_css_selector('img').get_attribute('src')
		for item in range(1, len(friend)):
			print friend[item]
		print username
		print photo
#=================================================================================	

#=================================================================================
#Music

def get_music(br):
	try:
		print "[+]Music"
		scraper_tools.scrap_sub_topics(br, "pagelet_timeline_medley_music", user)
	except:
		None
	
#=================================================================================
#Likes

def get_likes(br):
	try:
		print "[+]Likes"
		scraper_tools.scrap_sub_topics(br, "pagelet_timeline_medley_likes", user)
	except:
		None
#=================================================================================
#Movies

def get_movies(br):
	try:
		print "[+]Movies"
		scraper_tools.scrap_sub_topics(br, "pagelet_timeline_medley_movies", user)
	except:
		None
#=================================================================================
#Tv Shows
	
def get_tvshows(br):
	try:
		print "[+]Tv Shows"
		scraper_tools.scrap_sub_topics(br, "pagelet_timeline_medley_tv", user)
	except:
		None
#=================================================================================
#Groups

def get_groups(br,user):
	try:
		print "[+]Groups"
		#scraper_tools.scrap_sub_topics(br, "pagelet_timeline_medley_groups", user)
		old_school=br.find_element_by_id("pagelet_timeline_medley_groups")
		groups = old_school.find_elements_by_class_name('_1v6c')
		print "[+]",user, " has got ", len(groups), " groups"
		li_group=[]
		links = []
		for item in groups:
			group = item.text
			li = group.split('\n')
			li.remove('Join')
			li_group.append(li)
			link = item.find_elements_by_tag_name('a')
			for l in link:
				check =  l.get_attribute('href')
				if check.find(user) == -1:
					links.append(check)

		for i in range(0, len(li_group)):
			group = li_group[i]
			count = i +1
			print '-'*10
			print "[",count,"]"
			for item in group:
				print item
			print "link :", links[i]
	except:
		None
#=================================================================================
#Reviews
def get_reviews(br, user):
	try:
		print "[+]Reviews"
		#scraper_tools.scrap_sub_topics(br, "pagelet_timeline_medley_reviews", user)
		old_school=br.find_element_by_id("pagelet_timeline_medley_reviews")
		groups = old_school.find_elements_by_class_name('_1v6c')
		print "[+]",user, " has got ", len(groups), " reviews"
		li_group=[]
		links = []
		stars = []
		li_command=[]
		li_stars = []
		li_date = []
		li_activity = []
		for item in groups:
			group = item.text
			li_group.append(group)
			"""#Activity
			try:			
				activity=item.find_element_by_class_name("uiLinkSubtle")
				activity_link=activity.get_attribute('href')
				li_activity.append(activity_link)
			except:
				li_activity["Empty"]
			try:			
				activity_date = activity.find_element_by_class_name("timestamp").get_attribute("title")
				li_date.apped(activity_date)
			except:
				li_date.append("None")			
			#stars			
			stars = item.find_element_by_class_name("_559j")
			no_stars = len(stars.find_elements_by_tag_name('img'))
			li_stars.append(no_stars)
			#command
			command = item.find_element_by_class_name("_5mu1").text
			li_command.append(command)"""
			#link			
			link = item.find_elements_by_tag_name('a')
			for l in link:
				check =  l.get_attribute('href')
				if check.find(user) == -1:
					links.append(check)
		"""print "links :", links
		print "text :", li_group
		print "stars :",li_stars
		print "activity: ", li_activity
		print "commands: ", li_command
		print "date: ", li_date"""
		for review in range(0, len(li_group)):
			print '-'*10
			print "[",review+1,"]"
			print li_group[review]
			print "Link :", links[review]
			"""print "Activity :", li_activity[review]
			print "Date :", li_date[review]			
			print "Stars : ", li_stars[review]
			print "Command :", li_command[review]"""
	except:
		None
#=================================================================================
#Events
def get_events(br):
	try:
		print "[+]Events"
		scraper_tools.scrap_sub_topics(br, "pagelet_timeline_medley_events", user)
	except:
		None
#=================================================================================
#Sports
def get_sports(br):
	try:
		print "[+]Sports"
		scraper_tools.scrap_sub_topics(br, "pagelet_timeline_medley_sports", user)
	except:
		None
#=================================================================================
#Places
def get_places(br):
	try:
		print "[+]Places"
		scraper_tools.scrap_sub_topics(br, "pagelet_timeline_medley_map", user)
	except:
		None
#=================================================================================
#Games and Apps
def get_games_and_apps(br):
	try:
		print "[+]Games and Apps"
		scraper_tools.scrap_sub_topics(br, "pagelet_timeline_medley_games", user)
	except:
		None
#=================================================================================
#Books
def get_books(br):
	try:
		print "[+]Books"
		scraper_tools.scrap_sub_topics(br, "pagelet_timeline_medley_books", user)
	except:
		None
#=================================================================================
#Timeline
def get_timeline(br):
	print '='*20
	print "Timeline"
	if user.isdigit():
		br.get("https://www.facebook.com/profile.php?id="+user+"?fref=ts#")
	else:
		br.get("https://www.facebook.com/"+user+"?fref=ts#")
	time.sleep(10)
	scrolling_continue(br)
	time.sleep(10)
	try:
		timeln_all = br.find_element_by_id("u_0_1q_left")
	
	except:
		timeln_all = br.find_element_by_id("u_0_1s_left")

	timeln_li = timeln_all.text.split('\n')
	for item in range(0, len(timeln_li)):
		print timeln_li[item]
	#images
	img = timeln_all.find_elements_by_css_selector('img')
	print "[+]There are ",len(img)," come along with posts"
	#for i in range(0, len(img)):
	#	print img[i].get_attribute('src')
	

#=============================================================
#all pages container
def perform_action(br, value):
	if value == "Photos":
		get_photos(br)
	elif value == "Friends":
		get_friends(br)
	elif value == "Groups":
		get_groups(br, user)
	elif value == "Places":
		get_places(br)
	elif value == "Sports":
		get_sports(br)
	elif value == "Music":
		get_music(br)
	elif value == "Movies":
		get_movies(br)
	elif value == "TV Shows":
		get_tvshows(br)
	elif value == "Books":
		get_books(br)
	elif value == "Likes":
		get_likes(br)
	elif value == "Events":
		get_events(br)
	elif value == "Reviews":
		get_reviews(br, user)
	elif value == "Games and Apps":
		get_games_and_apps(br)
	elif value == "Sports":
		get_sports(br)
	elif value == "Places":
		get_places(br)

#=============================================================
#br.get("https://www.facebook.com/"+user+"/photos")
#time.sleep(10)
get_photos(br)
all = br.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[2]')
links = all.find_elements_by_css_selector('a')
#to get order of performing tasks
headers = br.find_elements_by_class_name("_51sx")
action_li = []
for i in range(1,len(headers)):
	action_li.append(headers[i].text)	
	#print headers[i].text

for value in action_li:
	try:
		print "="*10
		scrolling(br)		
		perform_action(br, value)
	except:
		None

get_timeline(br)
