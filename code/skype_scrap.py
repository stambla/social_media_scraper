#!/usr/bin/python
#from Skype4Py import *
import Skype4Py
import sys
import os
#import skype_usr_2_ip
import thread
import time

email=sys.argv[1]
#skype=Skype4Py.Skype()

def start_skype():
	os.system('skype')

def parse_email_to_user(email):
	#wait until Skype launched process is finished	
	time.sleep(30)
	email=email
	skype=Skype4Py.Skype()
	#skype = skype_instance
	user = skype.SearchForUsers(email)
	if len(user)==0:
		print "[+]There is no Skype user assigned to ", email
	else:
		print "[+]There is ", len(user), " users append to the ", email, "email address"
		info_commands = ['About', 'Aliases', 'Birthday', 'BuddyStatus', 'CanLeaveVoicemail', 'City', 'Country', 'CountryCode', 'DisplayName', 'FullName', 'Handle', 'HasCallEquipment', 'Homepage', 'IsAuthorized', 'IsBlocked', 'IsCallForwardActive', 'IsSkypeOutContact', 'IsVideoCapable', 'IsVoicemailCapable', 'Language', 'LanguageCode', 'LastOnline', 'LastOnlineDatetime', 'MoodText', 'NumberOfAuthBuddies', 'OnlineStatus', 'PhoneHome', 'PhoneMobile', 'PhoneOffice', 'Province', 'ReceivedAuthRequest', 'RichMoodText', 'Sex', 'SpeedDial', 'Timezone']
		for usr in range(0, len(user)):	
			panda = user[usr]
			print '-' * 50
			print "[+]User ", usr + 1	
			for comm in range(0,len(info_commands)):
				info_req= "panda."+ info_commands[comm]
				if not (eval(info_req) is None):
					print '-' * 20
					print info_commands[comm],' : ' ,eval(info_req)
					#print '-' * 20


try:
	Thread_1 = thread.start_new_thread( start_skype, () )
   	Thread_2 = thread.start_new_thread( parse_email_to_user, (email,) )
	#time.sleep(120)
	#Thread_1.exit
	#Thread_2.exit	
except:
	print "Error: unable to start thread"
while 1:
	pass


