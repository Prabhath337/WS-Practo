#!/usr/bin/python
import requests
import json
from sys import argv


"""get_uris function returns a dictionary of URI and headers used for corresponding requests."""

def get_uris():
	try:
		prac_uris={
		'referrer':'https://www.practo.com/',
		'listofcities':'https://www.practo.com/health/api/countrycities.json',
		'doc_spec_city':'https://www.practo.com/health/api/cityinformations/',
		'brain':'{"Accept":"application/json, text/javascript","Accept-Encoding":"gzip, deflate, sdch","Referer":"https://www.practo.com/"}',
		'ph_no':'https://www.practo.com/health/api/vn/vnpractice?practice_doctor_id='
		}
		return prac_uris
	except Exception as e:
		print(str(e))
	
# get_cities_generator yields city names supported by Practo.
def get_cities_generator():
	try:
		requests.packages.urllib3.disable_warnings()
		city_resp=requests.get(url=get_uris()['listofcities'],headers=json.loads(get_uris()['brain']),verify=False)
		if city_resp.status_code ==(200 or 201):
			cities_val=json.loads(city_resp.text)
			for le in range(0,len(cities_val)):
				ci_val=cities_val[le]['cities']
				yield ci_val
	except Exception as e:
		print(str(e))

#get_final_citites_generator yields iterable generators
def get_final_cities_generator():
	try:
		for knife_li in get_cities_generator():
			for kn_li in knife_li:
				replace_val=kn_li.replace(" ","-")
				low_val=replace_val.lower()
				yield low_val
	except Exception as e:
		print(str(e))

# replaces spaces,slashed with hypen and returns specialization required.
def replaces_spaces_slashes_withhypen(value):
	val=value.strip()
	if ' ' in val or '/ ' in val or '/' in val:
		if ' ' in val or '/' in val:
			re_val=val.replace(' ','-')
			if '/' in re_val:
				replaced_val=re_val.replace('/','-')
				return replaced_val
			else:
				return re_val
		elif ' ' in val or '/ ' in val:
			re_val1=val.replace(' ','-')
			if '/ ' in re_val1:
				replaced_val1=re_val1.replace('/ ','-')
				return replaced_val1
			else:
				return re_val
		elif '/' in val or '/ ' in val:
			re_val2=val.replace('/','-')
			if '/ ' in re_val2:
				replaced_val3=re_val2.replace('/ ','-')
				return replaced_val3
			else:
				return re_val2
	else:
		return val

# get_doc_specialization function return dictionary with city and its corresponding doctor's specializations.
def get_doc_specialization():
	try:
		doc_dict={}
		for clen in get_final_cities_generator():
			url_country=get_uris()['doc_spec_city']+clen+'.json'
			requests.packages.urllib3.disable_warnings()
			specialization=requests.get(url=url_country,headers=json.loads(get_uris()['brain']),verify=False)
			spec=json.loads(specialization.text)
			doc_dict[clen]=spec['specializations']
		return dict(doc_dict)

	except Exception as e:
		print(str(e))
   
""" practo_url_get_doctors_details function returns URL's  which is used for getting details of doctors w.r.t specializations and Total URL Counts."""

def practo_url_get_doctors_details():
	try:
		dict_city_spec=get_doc_specialization()
		for keys in dict_city_spec:
			for key in get_final_cities_generator():
				if key in keys:
					for list_val in range(len(dict_city_spec[key])):
						val=dict_city_spec[key][list_val]
						re_val=replaces_spaces_slashes_withhypen(val)
						doctors_urls=get_uris()['referrer']+str(key)+'/'+str(re_val)
						yield doctors_urls
	except Exception as e:
		print(str(e))


	