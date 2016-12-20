#!/usr/bin/python
import doctorsSpecializations
from bs4 import BeautifulSoup
import requests,os,json
import time
import xlsxwriter
"""
get_doctors_main_url fuction returns the final url of doctor which can be used for getting data from it

"""
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


def get_total_doc_list_count():
	try:
		resultbook=xlsxwriter.Workbook(os.getcwd()+"/"+"doctors_data"+".xlsx")
		resultsheet=resultbook.add_worksheet("results")
		heading=resultbook.add_format({'bold':True})
		resultsheet.write('A1','Name of Doctor',heading)
		resultsheet.write('B1','Total Experience',heading)
		resultsheet.write('C1','Phone Number',heading)
		resultsheet.write('D1','Services',heading)
		resultsheet.write('E1','Education',heading)
		resultsheet.write('F1','Experience',heading)
		resultsheet.write('G1','Membership',heading)
		resultsheet.write('H1','Registration',heading)
		doc_id=[]
		docname=''
		row=1
		for elehref in get_doctors_main_url():
			req=requests.get(elehref,verify=False)
			req_soup=BeautifulSoup(req.text,"html.parser")
			doc_name=req_soup.find_all("h1",attrs={"itemprop":"name"})
			for docname1 in doc_name:
				docname=docname1.get("title")
			ttl_exp=get_strings(req_soup,"h2","doctor-specialties")
			doc_id_from_html=req_soup.find_all("input",attrs={"class":"book-toggle ui-helper-hidden-accessible"})
			for doc_id1 in doc_id_from_html:
				doc_id.append(doc_id1.get("data-doctorid"))
			doc_id_final=get_doctors_phone_no(doc_id[0])
			serv=get_strings(req_soup,"div","services-block")
			edu=get_strings(req_soup,"div","doc-info-section qualifications-block")
			exp=get_strings(req_soup,"div","doc-info-section organizations-block")
			membership=get_strings(req_soup,"div","doc-info-section memberships-block")
			reg=get_strings(req_soup,"div","doc-info-section registrations-block")
			enter_data_into_excel(resultsheet,row,docname,ttl_exp,doc_id_final,serv,edu,exp,membership,reg)
			row=row+1
		resultbook.close()
		#return docname,ttl_exp,doc_id_final,serv,edu,exp,membership,reg
			

	except Exception as e:
		print(str(e))

def enter_data_into_excel(resultsheet,rowcount,doctor,totalexp,phno,service,educ,expe,membersh,regis):
	try:
		row=rowcount
		col=0
		print(row)
		resultsheet.write(row,col,doctor)
		resultsheet.write(row,col+1,totalexp)
		resultsheet.write(row,col+2,phno)
		resultsheet.write(row,col+3,service)
		resultsheet.write(row,col+4,educ)
		resultsheet.write(row,col+5,expe)
		resultsheet.write(row,col+6,membersh)
		resultsheet.write(row,col+7,regis)
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


if __name__=="__main__":
	get_doctors_main_url()