#!/usr/bin/python
#
# Copyright (C) 2014
#
#Social Media Scraper
#author Karolina Stamblewska
#
#Resolving Skype's username to the IP and IPGeo Location

__author__ = 'Karolina Stamblewska'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ErrorInResponseException
import time
import sys

class Skype2IP(object):
	"""Skype2IP object resolves Skype username to IP"""
	
	def __init__(self, skype_username, webdriver):
		"""
			Init .............		
		"""	
		self.br = webdriver
		self.skype_user=skype_username		
		#self.br=webdriver.Firefox()
		#skype.skype_user_to_ip(br, skype_user)
		#skype.ip_target_resolve(br, skype_ip)
	
	def skype_user_to_ip(self, webdriver, skype_user):
		"""
			(str) -> str
	
			skype user to IP resolve with hfreesolver (command: not free anymore api wise)
		"""
		self.br.get('http://hfresolver.com/ ')
		time.sleep(5)
		print self.br.current_url
		self.br.get('http://hfresolver.com/ ')
		time.sleep(5)
		self.br.get('http://hfresolver.com/ ')
		time.sleep(5)
		terminal=self.br.find_element_by_class_name('terminal')
		terminal.send_keys(skype_user)
		terminal.send_keys(Keys.RETURN)
		print "[+]Resolving skype username to IP"
	
		#sample output
		"""	terminal.text
			u"Welcome to my 100% Skype Resolver!\nThis tool will resolve a Skype username's
			latest IP Address!\nType a Skype username and press Enter.\nSkype Resolver > sst
			amblewski\nTrying To Resolve Username...\n Latest IP Address: 77.65.109.178\nCac
			hed Result\nSkype Resolver >  "
		"""
		time.sleep(60)		
		res=str(terminal.text)
	
		if not (res.find('ss: ')==-1):
			if res.find('API')==-1:
				skype_ip = res[res.find('ss: ')+4:res.find('Cached')-1]
				print "[+]User " + skype_user + "has got IP address: " + skype_ip	
				return skype_ip
			elif not(res.find('Error')==-1):
				print "No IP addres for this user"	
				return None
			else:
				skype_ip = res[res.find('ss: ')+4:res.find('API')-1]
				print "[+]User " + skype_user + "has got IP address: " + skype_ip	
				return skype_ip
					
		
	def ip_target_resolve(self, webdriver, ip_add):
		"""
			(str)->str #in future list of list
			
			>>>ip_target_resolve()
			>>>'IP Address: 77.65.109.178\nHostname: d109-178.icpnet.pl\nIP Blacklist Check: N
			ot Blacklisted\nIP Lookup Location For IP Address: 77.65.109.178\nContinent: Eur
			ope (EU)\nCountry: Poland    (PL)\nCapital: Warsaw\nState: Wielkopolskie\nCity L
			ocation: Konin\nISP: Inea\nOrganization: INEA Network\nIP Weather Station: Konin
			\nSky: scattered clouds\nTemp: 19.6 \xbaC (max 19.6 \xbaC / min 19.6 \xbaC)\nWin
			d Speed: 5.3 m/s\nWind Direction: 285.0\xb0\nHumidity: 57%\nCloudiness: 36%\nAtm
			ospheric pressure: 1017.31 kPa\nTime Zone: Europe/Warsaw\nLocal Time: 18:10:03\n
			Timezone GMT offset: 7200\nSunrise / Sunset: 04:30 / 21:11\nExtra IP Lookup Find
			er Info for IP Address: 77.65.109.178\nContinent Lat/Lon: 48.69083 / 9.1405\nCou
			ntry Lat/Lon: 52 / 20\nCity Lat/Lon: (52.2086) / (18.2541)\nIP Language: Polish\
			nIP Address Speed: Unknown Internet Speed\n[ Check Internet Speed]\nIP Currency:
			Zloty (PLN)\nIDD Code: +48'
		"""
		#get geolocation with www.ip-target.org
		if ip_add is None:
			print "[+] No IP address assigned to user"
		else:
			url = 'http://www.ip-tracker.org/locator/ip-lookup.php?ip='+ ip_add	
			"""br.get('http://www.ip-tracker.org/')	
			>>> input_ip=br.find_element_by_id('txtOne')
			>>> input_ip.clear()
			>>> input_ip.send_keys(usr_ip)
			>>> enter=br.find_element_by_class_name('inputinyext').click()
			"""
		
			self.br.get(url)
			time.sleep(10)
			target_ip=self.br.find_element_by_class_name('myipaddress')
			return target_ip.text
	
def main():
	"""Run that shit"""
	skype_user=sys.argv[1]
	br=webdriver.Firefox()	
	try:
    		skype = Skype2IP(skype_user,br)
  	except ErrorInResponseException:
		print 'Invalid user credentials given.'
		return

	skype_ip = skype.skype_user_to_ip(br, skype_user)
	location_info = skype.ip_target_resolve(br, skype_ip)
	print "[+]IPGeo Location info: ",location_info
	br.close()
if __name__ == '__main__':
  main()
