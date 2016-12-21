#!/usr/bin/python
import doctorsSpecializations
from bs4 import BeautifulSoup
import requests,os,json
import time

def get_doctors_main_url():
	try:
		for city_spec_urls in doctorsSpecializations.practo_url_get_doctors_details():
			requests.packages.urllib3.disable_warnings()
			city_spec_req=requests.get(city_spec_urls,verify=False)
			if city_spec_req.status_code == 200 or 201:
				doc_url_soup=BeautifulSoup(city_spec_req.text,"html.parser")
				for count_tag in doc_url_soup.find_all("h4"):
					if count_tag.text.__contains__("matches found"):
						for count in range(1,int(int(count_tag.text[:4].strip())/10)):
							req_href=requests.get(city_spec_urls+"?page="+str(count),verify=False)
							req_href_url_soup=BeautifulSoup(req_href.text,"html.parser")
							for href_links in req_href_url_soup.find_all("a",attrs={"itemprop":"url","class":"link doc-name smokeliftDoctorLink fm-target"}):
								yield href_links.get("href")
	except Exception as ex:
		print(str(ex))

def get_doctors_phone_no(doc_id):
	try:
		print(doc_id)
		no_req=requests.get(doctorsSpecializations.get_uris()['ph_no']+str(doc_id),verify=False)
		phone=json.loads(no_req.text)
		return phone['vn_phone_number']['number']
		
	except Exception as e:
		print(str(e))

def get_strings(pass_bs,element_tag,bs_class):
	try:
		str_val=''
		for m in pass_bs.find_all(element_tag,attrs={"class":bs_class}):
			for k in m.stripped_strings:
				str_val=str_val+k+','
		return str_val[:len(str_val)-1]
	except Exception as ex:
		print(str(ex))

def get_doctors_urls():
	ele_list=[]
	for elehref in get_doctors_main_url():
		ele_list.append(elehref)
	return ele_list

if __name__=="__main__":
	get_doctors_urls()